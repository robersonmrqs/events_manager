import wave
from pydub import AudioSegment
from tkinter import messagebox


def convert_to_wav(input_path, output_path):
    """
    Converte um arquivo de áudio para o formato WAV com taxa de amostragem de 16k, mono.
    """
    try:
        # Converte para WAV usando pydub
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(output_path, format="wav")
        return output_path
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter o arquivo de áudio: {e}")
        return None

def validate_wav(file_path):
    """
    Valida se o arquivo WAV atende aos requisitos (canal único, taxa de amostragem adequada).
    """
    try:
        with wave.open(file_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
                return False
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao validar o arquivo WAV: {e}")
        return False