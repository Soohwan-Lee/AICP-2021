import json
import speech_recognition as sr
import requests
from playsound import playsound
import cv2
import mediapipe as mp
import pickle
import numpy as np
import time

### Collecting void from mic
def get_speech():
    # Voice extraction from the microphone.
    recognizer = sr.Recognizer()

    # Mic setting
    microphone = sr.Microphone(sample_rate=16000)

    # Reflecting the noise level of the microphone noise.
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("미유가 소음 수치 반영하여 음성을 청취합니다. {}".format(recognizer.energy_threshold))

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
        text=""
        print("Error! because ",  res.json())
    # If success,
    else:
    	  #print("음성인식 결과 : ", res.text)
          #print("시작위치 : ", res.text.index('{"type":"finalResult"'))
          #print("종료위치 : ", res.text.rindex('}')+1)
          #print("추출한 정보 : ", res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1])
        try:
            result = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
            text = json.loads(result).get('value')
        except:
            text = "speak again"

    return text

### Merge speech part
def speech():
    #################### Speech Part ####################
    # ------------------------------------------------- #
    audio = get_speech()
    text = kakao_stt(KAKAO_APP_KEY, "stream", audio)
    print("미유의 음성 인식 결과 : " + text)

    if "노래" in text:
        playsound("./speech/code/1.mp3")
    # ------------------------------------------------- #


### Loading face model
def loadModel():
    path_model = ".//merge//model"
    face_model = "//210924face.pkl"
    with open(path_model + face_model, 'rb') as f:
        face_model = pickle.load(f)
    return face_model

### Get average data in real-time
def cumulativeAverage(prevAvgArray, newArray, listLength):
    if listLength > 0:
        oldWeight = (listLength - 1) / listLength
        newWeight = 1 / listLength
        avg = (prevAvgArray * oldWeight) + (newArray * newWeight)
    return avg


### Main Code
if __name__ == "__main__":
    # Kakao app key
    KAKAO_APP_KEY = "48995414c941eef20bfff6ad9c023947"
    
    # MediaPipe
    mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
    mp_holistic = mp.solutions.holistic  # Mediapipe Solutions

    # Load face model
    face_model = loadModel()

    # Variables for reading face
    read_face = True
    beginTime_face = 0
    listLength_face = 0
    face_class = 0
    threshold_face = 0.8
    timeInterval = 0.2

    # Video Capture for window & Set the frame size
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # speech part
            speech()

            # Flip Image
            image = cv2.flip(frame, 1)
            image.flags.writeable = False

            num_face_coords = 467

            # Make Detectionsq
            results = holistic.process(image)

            # Recolor image back to BGR for rendering
            image.flags.writeable = True
            # # convert color BRG to RGB
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # timer for 2 sec
            if read_face:
                beginTime_face = time.time()
                listLength_face = 0
                read_face = False

            # # Draw face landmark
            # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS, 
            #                         mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
            #                         mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
            #                         )

            try:
                # Extract Face landmarks
                face = results.face_landmarks.landmark
                face_row = np.array([[face[i].x - face[0].x, face[i].y - face[0].y]
                                                    for i in range(1,num_face_coords+1)]).flatten()

                # Average data
                listLength_face = listLength_face + 1
                if listLength_face == 1:
                    face_row_avg = face_row
                elif listLength_face > 1:
                    face_row_avg = cumulativeAverage(face_row_avg, face_row, listLength_face)

                # Make prediction for "timeInterval" sec
                duration = time.time() - beginTime_face
                if duration > timeInterval:
                    # print("face")
                    list(face_row_avg)
                    face_class = face_model.predict([face_row])[0]
                    face_prob = face_model.predict_proba([face_row])[0]
                    read_face = True
                    if float(face_prob[np.argmax(face_prob)]) < threshold_face:
                            face_class = 0
                    pause = False
                
                # # Add png image
                # if face_class != 0:
                #     pause = True
                #     if face_class == _face_class:
                #         pilim = Image.fromarray(image)
                #         pilim.paste(face_imgs[face_class], box=(1040, 40), mask=face_imgs[face_class])
                #         image = np.array(pilim)
                
                # Get status box
                cv2.rectangle(image, (250,0), (500, 60), (245, 117, 16), -1)
                
                # Display Class
                cv2.putText(image, 'CLASS'
                            , (345,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(face_class)
                            , (340,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Display Probability
                cv2.putText(image, 'PROB'
                            , (265,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(round(face_prob[np.argmax(face_prob)],2))
                            , (260,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass


            # show video with pop-up screen
            cv2.imshow('2021 AICP Pilot Demo', image)

            # Press 'q' to quit
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break