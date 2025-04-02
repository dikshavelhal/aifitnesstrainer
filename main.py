from flask import Flask, render_template, Response, request
import cv2
import mediapipe as mp
import numpy as np
import listofexercises
from playsound import playsound 
import threading
import pygame
import time



app = Flask(__name__)

# Global variable to control the running state of exercise streams
running_stream = None
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise1')
def exercise1():
    return render_template('exercise1.html')

@app.route('/bmi')
def bmi():
    return render_template('bmi.html')
@app.route('/calorie')
def calorie():
    return render_template('calorie.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/stop')
def stop():
    global running_stream
    running_stream = None
    cv2.destroyAllWindows()
    return "Stopped"

def generate_frames(exercise_type):
    for frame in workout(exercise_type):
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/start_exercise')
def exerciseestimator():
    global running_stream
    exercise_type = int(request.args.get('type'))
    
    if exercise_type in range(1,12):
        running_stream = exercise_type
    else:
        return "Invalid exercise type", 400
    
    return Response(generate_frames(exercise_type), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_frame_for_exercise(exercise_type):
    return next(workout(exercise_type))

pygame.mixer.init()

def play_sound(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait for music to finish playing
        continue

def up():
    audio_file = "audiofiles/up.mp3"
    threading.Thread(target=lambda: play_sound(audio_file)).start()
def down():
    audio_file = "audiofiles/down.mp3"
    threading.Thread(target=lambda: play_sound(audio_file)).start()
def buzzer():
    audio_file = "audiofiles/buzzer.mp3"
    threading.Thread(target=lambda: play_sound(audio_file)).start()

def workout(exercise_type):
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    target_width = 1080 # Set desired width
    target_height = 620
    cap = cv2.VideoCapture(0)
   
    counter = 0 
    stage = None
    last_updated = time.time()
    
    if exercise_type == 1:
        exercise = 'bicep_curl_right'
    elif exercise_type == 2:
        exercise = 'bicep_curl_left'
    elif exercise_type == 3:
        exercise = 'shoulder_press'
    elif exercise_type == 4:
        exercise = 'pushup'
    elif exercise_type == 5:
        exercise = 'squats'
    elif exercise_type == 6:
        exercise = 'lungesleft'
    elif exercise_type == 7:
        exercise = 'lungesright'
    elif exercise_type == 8:
        exercise = 'jumping_jack'
    elif exercise_type == 9:
        exercise = 'high_knees'
    elif exercise_type == 10:
        exercise = 'situps'
    elif exercise_type == 11:
        exercise = 'plank'
    elif exercise_type == 12:
        exercise = 'frog_press'
    else:
        raise ValueError("Invalid exercise type")
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and running_stream == exercise_type:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (target_width, target_height))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                angle=0
                b=0
                distance_hand=0
                distance_feet=0
                verify=True
                if exercise_type == 1:
                    angle,b = listofexercises.bicep_curl_right(results, mp_pose)   #highknees (same code for squat)
                elif exercise_type == 2:
                    angle,b = listofexercises.bicep_curl_left(results, mp_pose)
                elif exercise_type == 3:
                    angle,b = listofexercises.shoulder_press(results, mp_pose)
                elif exercise_type == 4:
                    angle,b = listofexercises.pushup(results, mp_pose)
                elif exercise_type == 5:
                    angle, b = listofexercises.squats(results, mp_pose)
                elif exercise_type == 6:
                    angle, b = listofexercises.lungesleft(results, mp_pose)
                elif exercise_type == 7:
                    angle, b = listofexercises.lungesright(results, mp_pose)
                elif exercise_type == 8:
                    angle, b = listofexercises.jumping_jack(results, mp_pose)
                elif exercise_type == 9:
                    angle, b = listofexercises.high_knees(results, mp_pose)
                elif exercise_type == 10:
                    angle, b = listofexercises.situps(results, mp_pose)
                elif exercise_type == 11:
                    angle, b = listofexercises.plank(results, mp_pose)
                elif exercise_type == 12:
                    angle, b = listofexercises.frog_press(results, mp_pose)
                cv2.putText(image, str(angle), 
                            tuple(np.multiply(b, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
            except Exception as e:
                pass
            
            def disply(stage,counter):
              
                cv2.rectangle(image, (0, 0), (300, 73), (245, 117, 16), -1)
                cv2.putText(image, 'REPS', (15, 12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter), 
                            (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, 'STAGE', (65, 12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, stage, 
                            (80, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 ) 
                
                if time.time() - last_updated > 10:
                    
                    cv2.rectangle(image, (0, 75), (300, 120), (0, 0, 255), -1)
                    cv2.putText(image, "You haven't moved for 10 seconds!", 
                                (10, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                    buzzer()
            if exercise_type == 1:  #bicepcurlright
                if angle > 160:
                    stage = "down"
                    down()
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                    up()
                    last_updated = time.time()
                disply(stage,counter)
                
            elif exercise_type == 2:   #bicepcurlleft
                if angle > 160:
                    stage = "down"
                    down()
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                    up()
                    last_updated = time.time()
                disply(stage,counter)
            elif exercise_type == 3: #shoulderpress
                if angle > 160:
                    stage = "up"
                    
                if angle < 50 and stage == 'up':
                    stage = "down"
                    counter += 11
                    down()
                    last_updated = time.time()
                # if int(counter)>0 and int(counter)%5==0:
                #     keepmoving()
                
                disply(stage,counter)
            elif exercise_type == 4:       #pushup
                if angle > 160:
                    stage = "up"
                if angle < 70 and stage =='up':
                    stage="down"
                    counter +=1
                    down()
                    last_updated = time.time()
                disply(stage,counter)

            elif exercise_type == 5:       #squats
                if angle > 160:
                    stage = "up"
                if angle < 90 and stage == 'up':
                    stage = "down"
                    counter += 1
                    down()
                    last_updated = time.time()
                disply(stage,counter)

            elif exercise_type == 6:     #lungesleft
                if angle > 160:
                    stage = "up"
                if angle < 90 and stage == 'up':
                    stage = "down"
                    counter += 1
                    down()
                    last_updated = time.time()
                disply(stage,counter)
            elif exercise_type == 7:     #lungesright
                if angle > 160:
                    stage = "up"
                if angle < 90 and stage == 'up':
                    stage = "down"
                    counter += 1
                    down()
                    last_updated = time.time()
                disply(stage,counter)
            elif exercise_type == 8:     #jumping_jacks
                if angle <= 150 and b >= 150:
                    stage="up"
                if angle > 150 and b < 150 and stage =='up':
                    stage="down"
                    counter += 1
                    last_updated = time.time()
                disply(stage,counter)

            elif exercise_type == 9:     #high_knees
                if angle > 160:
                    stage = "down"
                if angle < 90 and stage == 'down':
                    stage = "up"
                    counter += 1
                    up()
                    last_updated = time.time()
                disply(stage,counter)

            elif exercise_type == 10:    #situps
                if angle > 160:
                    stage = "down"
                if angle < 100 and stage == 'down':
                    stage = "up"
                    counter += 1
                    up()
                    last_updated = time.time()
                disply(stage,counter)

            elif exercise_type == 11:   #plank
                if angle > 160:
                    stage = "up"
                if angle < 70 and stage =='up':
                    stage="down"
                    counter +=1
                    down()
                    last_updated = time.time()
                disply(stage,counter)

            elif exercise_type == 12:    #frogpress
                if angle > 160 and stage == "down":
                    stage = "up"
                    counter += 1
                if angle < 70:
                    stage = "down"
                    down()
                    last_updated = time.time()
                disply(stage,counter)
            
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield frame

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


