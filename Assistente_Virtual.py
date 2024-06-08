import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import playsound
import pyjokes
import wikipedia
import pyaudio
import webbrowser
import winshell
from pygame import mixer

# função para captar e transcrever áudio em texto
def get_audio():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        rec.pause_threshold = 1
        # filtrar ruidos captados no audio
        rec.adjust_for_ambient_noise(source, duration=1)
        audio = rec.listen(source)
        said = ""
        try:
            said = rec.recognize_google(audio)
            print(said)
        except sr.UnknownValueError:
            speak("Desculpe, não foi possivel realizar essa ação.")
        except sr.RequestError:
            speak("Desculpe, serviço indisponível no momento!")
    return said.lower()

# função para converter texto para audio
def speak(text):
    tts = gTTS(text=text, lang='pt')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

# Função para executar os comandos mencionados
def respond(text):
    print("Convertedno áudio em texto:  " + text)
    # acessar o yutube
    if 'youtube' in text:
        # informar item de pesquisa
        speak("O quevocê deseja pesquisar?")
        keyword = get_audio()
        if keyword!= '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.get().open(url)
            speak(f"Esse foi o resultado da pesquisa por {keyword} no youtube")
    # fazer pesquisa no wikipedia
    elif 'search' in text:
    # informar tema de pesquisa
        speak("O que você deseja pesquisar")
        query = get_audio()
        if query !='':
            result = wikipedia.summary(query, sentences=3)
            speak("Pesquisando no wikipedia")
            print(result)
            speak(result)

    elif 'piada' in text:
        speak(pyjokes.get_joke())
    elif 'Esvaziar lixeira' in text:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Lixeira esvaziada!")
    # Informar a hora e a data
    elif 'qual hora' in text:
        strTime = datetime.today().strftime("%H:%M %p")
        print(strTime)
        speak(strTime)
    # tocar música
    elif 'acessar musica' in text or 'tocar musica' in text:
        speak("Executando agora...")
        music_dir = "C:\\Users\\UserName\\Downloads\\Music\\" #Substituir pelo caminho do diretório de músicas..
        songs = os.listdir(music_dir)
        #counter = 0
        print(songs)
        playmusic(music_dir + "\\" + songs[0])
    # parar música
    elif 'parar musica' in text:
        speak("Interrompendo musica.")
        stopmusic()
    # sair do sistema
    elif 'exit' in text:
        speak("Obrigado por usar nossos serviços, até a próxima!")
        exit()

# função para tocar a múscia
def playmusic(song):
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()

# função para parar a música
def stopmusic():
    mixer.music.stop()

# Iniciando assistente
while True:
    print("I am listening...")
    text = get_audio()
    respond(text)