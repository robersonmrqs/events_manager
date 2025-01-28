import json
import numpy as np
import os
import sounddevice as sd
import vosk
import wave
from config import RESOURCES_DIR
from controllers.convert_audio import convert_to_wav, validate_wav
from tkinter import messagebox

def transcribe_audio(file_path):
    """
    Transcreve o áudio do arquivo fornecido. Converte para WAV se necessário.

    Args:
        file_path (str): Caminho do arquivo de áudio.

    Returns:
        str: Texto transcrito do áudio.
    """
    model_path = os.path.join(RESOURCES_DIR, "models", "vosk-model-small-pt-0.3")
    if not os.path.exists(model_path):
        messagebox.showerror("Erro", "Modelo de transcrição não encontrado. Baixe o modelo e configure o caminho corretamente.")
        return ""

    # Variável para controlar se o arquivo foi convertido
    converted_file = False
    original_file_path = file_path  # Para referência futura

    # Verifica e converte o arquivo para WAV, se necessário
    if not file_path.lower().endswith(".wav") or not validate_wav(file_path):
        output_path = os.path.splitext(file_path)[0] + "_converted.wav"
        file_path = convert_to_wav(file_path, output_path)
        converted_file = True  # Marca que o arquivo foi convertido
        if not file_path:
            return ""  # Retorna vazio caso a conversão falhe

    try:
        # Abre o arquivo WAV para leitura
        with wave.open(file_path, "rb") as wf:
            model = vosk.Model(model_path)
            recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

            transcription = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    transcription += result.get("text", "") + " "

            final_result = json.loads(recognizer.FinalResult())
            transcription += final_result.get("text", "")
            return transcription.strip()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante a transcrição: {e}")
        return ""
    finally:
        # Tenta remover o arquivo convertido, se aplicável
        if converted_file:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)  # Remove o arquivo após garantir que ele está fechado
                    print(f"Arquivo convertido removido: {file_path}")
                else:
                    print(f"Arquivo convertido já não existe: {file_path}")
            except Exception as e:
                print(f"Erro ao tentar remover o arquivo convertido: {file_path}. Erro: {e}")
                messagebox.showwarning("Aviso", f"Não foi possível apagar o arquivo convertido: {file_path}")

# Função para transcrição de áudio ao vivo (microfone)
def transcribe_live_audio():
    model_path = os.path.join(RESOURCES_DIR, "models", "vosk-model-small-pt-0.3")  # Baixe e configure o modelo antes de usar
    if not os.path.exists(model_path):
        messagebox.showerror("Erro", "Modelo de transcrição não encontrado. Baixe o modelo e configure o caminho corretamente.")
        return ""

    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    transcription = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        # Convertendo dados para bytes corretamente com numpy
        audio_data = np.frombuffer(indata, dtype=np.int16).tobytes()
        if recognizer.AcceptWaveform(audio_data):
            result = json.loads(recognizer.Result())
            transcription.append(result.get("text", ""))

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            messagebox.showinfo("Transcrição ao Vivo", "Fale no microfone. Pressione OK para terminar.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao capturar áudio: {e}")
        return ""

    final_result = recognizer.FinalResult()
    transcription.append(json.loads(final_result).get("text", ""))

    return " ".join(transcription).strip()