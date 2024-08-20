import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

def listen_command():
    """Listen for commands like 'pause recording', 'resume', and 'end recording'."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Command: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the command.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def speech_to_text():
    """Continuously listen to speech until 'end recording' is spoken."""
    print("Say 'pause recording' to pause, 'resume' to continue, or 'end recording' to stop.")
    recording = True
    
    while recording:
        if recording:
            print("Adjusting for ambient noise... Please wait.")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = recognizer.listen(source)
                
                try:
                    text = recognizer.recognize_google(audio).lower()
                    print(f"You said: {text}")
                    
                    if "end recording" in text:
                        print("End recording command recognized. Stopping...")
                        recording = False
                    elif "pause recording" in text:
                        print("Pausing. Say 'resume' to continue...")
                        while True:
                            command = listen_command()
                            if command == "resume":
                                print("Resuming...")
                                break
                            elif command == "end recording":
                                print("End recording command recognized. Stopping...")
                                recording = False
                                break
                            else:
                                print("Say 'resume' to continue or 'end recording' to stop.")
                
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    speech_to_text()
