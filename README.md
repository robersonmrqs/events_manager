Descrição do Projeto
O Gerenciador de Eventos é uma aplicação desktop que permite organizar eventos de forma eficiente. Ele permite que os usuários cadastrem, pesquisem, excluam e gerenciem eventos, além de gerar relatórios em formatos como Excel e PDF. A aplicação se destaca por utilizar inteligência artificial de transcrição de áudio baseada no modelo Vosk. Esse modelo é usado para converter gravações de voz em texto, facilitando o cadastro rápido de eventos sem a necessidade de digitação manual.

Funcionalidades Principais
Cadastro de Eventos:
Informar título, data, resumo e horas dispendidas.
Suporte à transcrição de áudio para o campo de resumo.
Busca de Eventos:
Busca por palavras-chave no título ou resumo.
Exclusão de Eventos:
Remoção de eventos específicos.
Relatórios:
Exportação de dados para Excel e PDF.
Transcrição de Áudio:
Suporte a arquivos de áudio em vários formatos.
Transcrição ao vivo via microfone utilizando o modelo Vosk.

Por que usar o modelo Vosk?
Reconhecimento de Voz Offline: O modelo Vosk é leve e pode ser usado sem conexão à internet.
Suporte Multilíngue: Inclui suporte para o português.
Precisão e Desempenho: Ótimo desempenho em transcrição de áudio, mesmo em dispositivos de hardware modesto.

Passo a Passo para Utilização
Iniciar a Aplicação:
Execute o arquivo GerenciadorDeEventos.exe ou inicie o projeto no Python (python main.py).
Cadastrar um Evento:
Na tela principal, insira uma data e clique em Selecionar Data.
Preencha as informações ou utilize a transcrição de áudio para gerar o resumo.
Clique em Salvar Evento para registrar o evento.
Buscar Eventos:
Use a barra de pesquisa para localizar eventos pelo título ou resumo.
Gerar Relatórios:
Clique em Gerar Relatório para exportar os dados em Excel ou PDF.
Excluir um Evento:
Na busca ou relatório, selecione o evento desejado e clique em Excluir.

Pré-requisitos
Ambiente de Execução:
Python 3.10+ (se estiver rodando via código-fonte).
Executável gerado (não requer instalação de Python).

Dependências:
Certifique-se de que o ffmpeg está instalado e configurado no PATH para conversão de áudio.

Com essa aplicação, você pode gerenciar eventos de forma prática e inteligente, economizando tempo com o poder da inteligência artificial!
