import json
import speech_recognition as sr
import requests
import time
import vlc
import RPi.GPIO as GPIO
import os


#from playsound import playsound

KAKAO_APP_KEY = "48995414c941eef20bfff6ad9c023947"
doDefault = False
doPlay = False
touch = False
playChecker = False

touch_pin = 37
GPIO.setmode(GPIO.BOARD)

GPIO.setup(touch_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)


### Collecting voice from mic
def get_speech():
    # Voice extraction from the microphone.
    recognizer = sr.Recognizer()

    # Mic setting
    microphone = sr.Microphone(sample_rate=16000)
    


    # Reflecting the noise level of the microphone noise.
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("미유가 소음 수치 반영하여 음성을 청취합니다. {}".format(
            recognizer.energy_threshold))

    # Collecting voice
    with microphone as source:
        print("미유가 듣고 있습니다. 말씀하세요!")
        result = recognizer.listen(source)
        audio = result.get_raw_data()

    return audio

### Speech-to-Text
def kakao_stt(app_key, stype, data):
    if stype == 'stream':
        audio = data
    headers = {
        "Content-Type": "application/octet-stream",
        "Authorization": "KakaoAK " + app_key,
    }

    # Kakao speech url
    kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

    # Requeat Kakao speech API
    res = requests.post(kakao_speech_url, headers=headers, data=audio)

    # If fail,
    if res.status_code != 200:
        text = ""
        print("Error! because ",  res.json())
    else:  # If success,
        #print("음성인식 결과 : ", res.text)
        #print("시작위치 : ", res.text.index('{"type":"finalResult"'))
        #print("종료위치 : ", res.text.rindex('}')+1)
        #print("추출한 정보 : ", res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1])
        try:
            result = res.text[res.text.index(
                '{"type":"finalResult"'):res.text.rindex('}')+1]
            text = json.loads(result).get('value')
        except:
            text = "다시 말씀해주세요."

    return text


### Repeat Video play
def start(player):
    player.set_fullscreen(True)
    em = player.event_manager()
    em.event_attach(vlc.EventType.MediaPlayerEndReached, onEnd)
    player.play()

def onEnd(event):
    global doDefault
    if event.type == vlc.EventType.MediaPlayerEndReached:
        doDefault = True

def back(player):
    player.set_media(player.get_media())
    player.play()
    
### Repeat Video play
def startPlay(player):
    player.set_fullscreen(True)
    emPlay = player.event_manager()
    emPlay.event_attach(vlc.EventType.MediaPlayerEndReached, onEnd)
    player.play()

def onEndPlay(event):
    global doDefault
    if event.type == vlc.EventType.MediaPlayerEndReached:
        doPlay = True

def backPlay(player):
    player.set_media(player.get_media())
    player.play()
    


### Main Code
if __name__ == "__main__":
    ### Set for Audio
    instance = vlc.Instance('--aout=alsa')
    music = instance.media_player_new()
    musicFile = instance.media_new('/home/pi/Desktop/AICP/speech/code/sound/music.mp3')
    musicStartFile = instance.media_new('/home/pi/Desktop/AICP/speech/code/sound/musicStart.mp3')
    musicEndFile = instance.media_new('/home/pi/Desktop/AICP/speech/code/sound/musicEnd.mp3')
    nameFile = instance.media_new('/home/pi/Desktop/AICP/speech/code/sound/name.mp3')
    bornFile = instance.media_new('/home/pi/Desktop/AICP/speech/code/sound/born.mp3')

    
    ### Set for Video
    #player = vlc.MediaPlayer()
    #player.set_fullscreen(True)
    default = vlc.MediaPlayer('/home/pi/Desktop/AICP/speech/code/default.mp4')
    answering = vlc.MediaPlayer('/home/pi/Desktop/AICP/speech/code/answering.mp4')
    lovely = vlc.MediaPlayer('/home/pi/Desktop/AICP/speech/code/music.mp4')
    petting = vlc.MediaPlayer('/home/pi/Desktop/AICP/speech/code/petting.mp4')
    start(default)
    
    while(1):
        ### Default Video Play
        if doDefault:
            back(default)
            doDefault = False
        
        if touch:
            start(petting)
            time.sleep(4)
            petting.stop()
            touch = False
        
        print(touch)
        try:
            if(GPIO.input(touch_pin)) and touch == False:
                touch = True
                print(touch)
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
        
        ### speech recognition
        audio = get_speech()
        text = kakao_stt(KAKAO_APP_KEY, "stream", audio)
        print("Result : " + text)

        
        if "노래" and "꺼" in text:
            music.stop()
            music.set_media(musicEndFile)
            music.play()
            volume = 100
            vlc.libvlc_audio_set_volume(music, volume)
            #music.stop()
            start(answering)
            time.sleep(4)
            answering.stop()
        elif "노래" and "틀어" in text:
            music.stop()
            music.set_media(musicStartFile)
            music.play()
            volume = 100
            vlc.libvlc_audio_set_volume(music, volume)
            #time.sleep(3)
            startPlay(lovely)
            time.sleep(4)
            music.set_media(musicFile)
            music.play()
            volume = 100
            vlc.libvlc_audio_set_volume(music, volume)
            lovely.stop()
        elif "이름" in text:
            music.stop()
            music.set_media(nameFile)
            music.play()
            volume = 100
            vlc.libvlc_audio_set_volume(music, volume)
            start(answering)
            time.sleep(4)
            answering.stop()
        elif "어디" and "태어" in text:
            music.stop()
            music.set_media(bornFile)
            music.play()
            volume = 100
            vlc.libvlc_audio_set_volume(music, volume)
            start(answering)
            time.sleep(4)
            answering.stop()
