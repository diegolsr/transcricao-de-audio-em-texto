import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import subprocess

# Função para converter arquivos .opus para .wav usando ffmpeg
def convert_opus_to_wav(input_file):
    output_file = os.path.splitext(input_file)[0] + ".wav"
    subprocess.run(["ffmpeg", "-i", input_file, output_file])
    return output_file

# Nome do arquivo original
# input_file = "PTT-20230913-WA0004.opus"
input_file = "WhatsApp Ptt 2023-09-13 at 09.35.15.ogg"

# Converte o arquivo .opus para .wav
converted_file = convert_opus_to_wav(input_file)

# Carregar o arquivo wav convertido
audio = AudioSegment.from_wav(converted_file)

# Tamanho do chunk
size = 180000  # 3 minutos em milissegundos

# Divide o áudio em chunks
chunks = make_chunks(audio, size)

for i, chunk in enumerate(chunks):
    # Nome do chunk
    chunk_name = os.path.splitext(input_file)[0] + "_chunk{0}.wav".format(i)
    
    # Salva o chunk como .wav
    chunk.export(chunk_name, format="wav")
    file_audio = sr.AudioFile(chunk_name)
    
    # Usa o arquivo de áudio como fonte e reconhece o texto
    r = sr.Recognizer()
    with file_audio as source:
        audio_text = r.record(source)
        try:
            text = r.recognize_google(audio_text, language='pt-BR')
        except sr.UnknownValueError:
            text = "Não foi possível reconhecer o áudio"
        
        # Salva o texto reconhecido em um arquivo .txt
        with open(chunk_name.replace('.wav', '') + '.txt', 'w') as arq:
            arq.write(text)
