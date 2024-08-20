# from flask import Flask, render_template, jsonify
# import speech_recognition as sr

# app = Flask(__name__)

# # Initialize the recognizer
# recognizer = sr.Recognizer()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/listen_command', methods=['GET'])
# def listen_command():
#     """Listen for commands like 'pause recording', 'resume', and 'end recording'."""
#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         print("Listening for command...")
#         audio = recognizer.listen(source)
#         try:
#             command = recognizer.recognize_google(audio).lower()
#             print(f"Command: {command}")
#             return jsonify({'command': command})
#         except sr.UnknownValueError:
#             return jsonify({'error': 'Could not understand the command.'}), 400
#         except sr.RequestError as e:
#             return jsonify({'error': f'Could not request results from Google Speech Recognition service; {e}'}), 500

# @app.route('/speech_to_text', methods=['GET'])
# def speech_to_text():
#     """Continuously listen to speech until 'end recording' is spoken."""
#     print("Say 'pause recording' to pause, 'resume' to continue, or 'end recording' to stop.")
#     recording = True
    
#     while recording:
#         if recording:
#             print("Adjusting for ambient noise... Please wait.")
#             with sr.Microphone() as source:
#                 recognizer.adjust_for_ambient_noise(source)
#                 print("Listening...")
#                 audio = recognizer.listen(source)
                
#                 try:
#                     text = recognizer.recognize_google(audio).lower()
#                     print(f"You said: {text}")
                    
#                     if "end recording" in text:
#                         print("End recording command recognized. Stopping...")
#                         return jsonify({'message': 'End recording command recognized. Stopping...', 'text': text})
#                     elif "pause recording" in text:
#                         print("Pausing. Say 'resume' to continue...")
#                         while True:
#                             command = listen_command()
#                             if command == "resume":
#                                 print("Resuming...")
#                                 break
#                             elif command == "end recording":
#                                 print("End recording command recognized. Stopping...")
#                                 return jsonify({'message': 'End recording command recognized. Stopping...', 'text': text})
#                             else:
#                                 print("Say 'resume' to continue or 'end recording' to stop.")
                
#                 except sr.UnknownValueError:
#                     return jsonify({'error': "Google Speech Recognition could not understand audio"}), 400
#                 except sr.RequestError as e:
#                     return jsonify({'error': f"Could not request results from Google Speech Recognition service; {e}"}), 500

# if __name__ == "__main__":
#     app.run(debug=True)








from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import speech_recognition as sr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Initialize the recognizer
recognizer = sr.Recognizer()
recording = False
paused = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_recording')
def start_recording():
    global recording
    recording = True
    socketio.start_background_task(target=record_speech)

def record_speech():
    global recording, paused
    while recording:
        if not paused:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = recognizer.listen(source)
                
                try:
                    text = recognizer.recognize_google(audio).lower()
                    print(f"You said: {text}")
                    socketio.emit('update_text', {'text': text})

                    if "terminate" in text:
                        recording = False
                        socketio.emit('update_status', {'status': 'End recording command recognized. Stopping...'})
                    elif "pause recording" in text:
                        paused = True
                        socketio.emit('update_status', {'status': 'Pausing. Say "resume" to continue...'})
                    elif "resume recording" in text:
                        paused = False
                        socketio.emit('update_status', {'status': 'Resuming...'})

                except sr.UnknownValueError:
                    socketio.emit('update_status', {'status': "7thSense could not understand audio"})
                except sr.RequestError as e:
                    socketio.emit('update_status', {'status': f"Could not request results from 7thSense service; {e}"})

if __name__ == "__main__":
    socketio.run(app, debug=True)
