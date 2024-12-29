##################################################
##################################################
"""               NGUYEN CONG HUY              """
####    ##################   #####    ####    ####
####    ##################   ######   ####    ####
####          ######         #### ##  ####    ####
####          ######         ####  ## ####    ####
####          ######         ####   ######    ####
####          ######         ####   ######    ####
####                TOFU NGUYEN               ####
##################################################
##################################################

###########################################################################
#### Programe's name: Mary Assistant - New way to control your laptop  ####
#### Programmer: Nguyen Cong Huy (Nickname: Tofu Nguyen)               ####
#### Finished date: Sunday, December 29, 2024                          ####
###########################################################################


"""
This program is programmed by Tofu Nguyen.
Some lines are used from open-source libraries.
"""

# Initialize modules that are created by Tofu Nguyen
from Modules.ControlComputer import *
from Modules.MathSolving import basicOperations
from Modules.Greeting import *
from Modules.DateAndTime import DateTime

# Open-source libraries of Python
import os
import time
import struct
import pyaudio
import win32api
import playsound
import wikipedia
import webbrowser
import pvporcupine
import customtkinter
from PIL import Image
from gtts import gTTS
from random import choice
from threading import Thread
import speech_recognition as sr
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

"""
Adjusting the volume of the computer speakers.
These funcstions are used to auto-control the volume of the computer speaker.
When the user or the assistant start talking, other applications' speaker's volumes is reduced.
After finishing talking or listening, the volume is returned to the original state.
"""
# Container Dictinary
volume_map = {}
# Retrieve the default audio output device (speakers)
def get_audio_endpoint_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

# Get the current master volume level
def get_current_volume(volume):
    # Retrieve the current master volume level.
    return volume.GetMasterVolumeLevelScalar() # Returns a scalar value between 0.0 and 1.0

# Adjust and store other applications' volumes
def adjust_volume(volume_map):
    # Lower the volume of all applications except the current one
    current_process_id = os.getpid() # Get the current process ID
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        try:
            process = session.Process
            if process and process.pid != current_process_id:
                audio_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                original_volume = audio_interface.GetMasterVolume() # Get current volume
                volume_map[process.pid] = original_volume # Store orginal volume
                audio_interface.SetMasterVolume(0.2, None) # Lower volume to 20%
                print(f"Lowered volume for: {process.name()} (PID: {process.pid})")
            elif process is None:
                print("Skipping system sound session.")
        except Exception as e:
            print(f"Error adjusting volume for {process.name()}: {str(e)}")

# Revert other applications' volumes to their original levels
def revert_volume(volume_map):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        try:
            process = session.Process
            if process and process.pid != volume_map:
                audio_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                original_volume = volume_map[process.pid]
                audio_interface.SetMasterVolume(original_volume, None)
                print(f"Restored volume for: {process.name()} (PID: {process.pid})")
            elif process is None:
                print("Skipping system sound session.")
        except Exception as e:
            print(f"Failed to restore volume for {process.name()}: {str(e)}")

"""
These two functions are used to analyze the question to determine if it's asking about the current date or time.
Using a dictionary to save the keywords that indicate the question is asking about the current date or time,
these two function help to determine the type of question and return the corresponding answer.
"""
# Analyzing the question to determine if it's asking about the current date
def is_asking_current_date(question):
    # The list of keywords that indicate the question is asking about the current date
    patterns = [
        r"\bhôm nay\b.*\bngày mấy\b",
        r"\bhôm nay\b.*\bngày bao nhiêu\b",
        r"\bngày hôm nay\b.*\bngày gì\b",
        r"\bhôm nay\b.*\bthứ mấy\b",
        r"\bngày hôm nay\b.*\bngày bao nhiêu\b",
        r"\bngày\b.*\bhôm nay\b.*\bthứ mấy\b",
        r"\bhôm nay\b.*\bngày là bao nhiêu\b",
        r"\bhôm nay\b.*\bngày nào\b"
    ]
    # Transform the question into lowercase to make the search case-insensitive
    question = question.lower()
    # Check if any of the patterns match the question
    for pattern in patterns:
        if re.search(pattern, question):
            return True
    return False

# Analyzing the question to determine if it's asking about the current time
def is_asking_current_time(question):
    # The list of keywords that indicate the question is asking about the current time
    patterns = [
        r"\bsáng\b.*\bmấy giờ\b",
        r"\bmấy giờ\b.*\bsáng\b",
        r"\btrưa\b.*\bmấy giờ\b",
        r"\bmấy giờ\b.*\btrưa\b",
        r"\bchiều\b.*\bmấy giờ\b",
        r"\bmấy giờ\b.*\bchiều\b",
        r"\btối\b.*\bmấy giờ\b",
        r"\bmấy giờ\b.*\btối\b",
        r"\bmấy giờ\b",
        r"\bgọi điện\b.*\bmấy giờ\b",
        r"\bgọi cho tôi\b.*\bmấy giờ\b",
        r"\bmấy giờ rồi\b",
        r"\bđồng hồ\b.*\bmấy giờ\b",
        r"\bcho tôi biết\b.*\bmấy giờ\b"
    ]
    # Transform the question into lowercase to make the search case-insensitive
    question = question.lower()
    # Check if any of the patterns match the question
    for pattern in patterns:
        if re.search(pattern, question):
            return True
    return False

"""
This function is built to check if the question contains the keyword in that list.
If it does, return True, else return False. This function is really important.
"""
# Keywords checking function
def isContain(text, list):
    return any(word in text for word in list)

"""
This function is used to handle the function called "Assistant Calling".
It contains a model of the keyword "mary mary".
When the users start the programe, it will be called and wait. 
If the user call "mary mary", it will detect the keyword return it to the main function.
Then the "hear()" function will start working to listen the commands from the users.
"""
receive = True # Stop Flag - Used when the user wants to stop the assistant
# Assistant's name calling function
def callMary():
    global receive
    # Access key of Picovoice service
    access_key = "/91nRu+Qi2UYHIP1FKRVpwJKMBSjQFL2KrYLWcQrs/vVmRINrD0HBw=="
    # Initialize the "mary mary" keyword model
    porcupine = pvporcupine.create (
        access_key=access_key,
        keyword_paths=["Assets/mary-mary_en_windows_v3_0_0.ppn"]
    )
    # Initialize the recorder and its attributes
    pa = pyaudio.PyAudio()
    audio_stream = pa.open (
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    wake_word = "mary" # Temporary variable used to contain the keyword "mary"
    # Keyword checking from the recorder
    try:
        while receive:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            if porcupine.process(pcm) >= 0:
                print("Wake word detected!")
                break
    except:
        # print("Stopping...")
        pass
    finally:
        # Close all recorders
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        porcupine.delete()
    # If the stop-flag is still active, return the keyword
    if receive:
        return wake_word

# Listening command from user
# Initialize the recorder
r = sr.Recognizer()
def hear():
    # Initialize the microphone as a source
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1) # Handling with ambient noise
        activate_microphone() # Transform the icon on the GUI.
        playsound.playsound("Assets/Sounds/StartListening.wav")# Ready sound playing
        adjust_volume(volume_map) # Handling with other apps' volume
        audio = r.listen(source, phrase_time_limit=5) # Start recording
    revert_volume(volume_map) # Revert the volumes of other applications
    deactivate_microphone() # Transform the icon on the GUI.
    playsound.playsound("Assets/Sounds/StopListening.wav") # Stop sound playing
    
    # Try to recognize the command
    try:
        text = r.recognize_google(audio, language="vi-VN") # Recognize the command using Google STT API
        # Transform the result (command in text) to lowercase
        text = text.lower()
        # Send the result to the keyword comparing function
        Thread(target=Processing, args=(text, )).start()
        return text # Return the command recognised
    # If cannot send the request to the server, return nothing
    except:
        # Speak out the announcement.
        playsound.playsound("Assets/Sounds/Failed.wav")
        return ""

# Voice operating function
def voiceMedia():
    global receive # Use stop-flags to recognize when it works or stop
    while receive:
        # Try to recognize the keyword "mary mary" from user voice
        try:
            heard = callMary()
            if isContain(heard, ["mary"]):  # Call the keyword comparing function
                print(hear()) # Print the recognize result for testing
        # If it can recognize the keyword, then pass
        except:
            pass

"""
This function is used to speak out the responses using Google Text-to-speech API.
It will get the "input", then send it to Google Translte Server, 
then get the result and using "playsound" library to speak it out.
"""
def speak(input):
    tts = gTTS(input, lang="vi", slow=False) # Sending requests
    tts.save("Assets/Sounds/output.mp3") # Save the result
    adjust_volume(volume_map) # Adjust volume of other applications
    playsound.playsound("Assets/Sounds/output.mp3") # Speak out the result
    revert_volume(volume_map) # Revert the volumes of other applications
    os.remove("Assets/Sounds/output.mp3") # Delete the result.

# Speak this out when the users open the assistant
speak("Xin chào! Hôm nay tôi có thể giúp gì cho bạn?")

"""
This function can be called as a main brain of the assistant.
In this function, all the command from the "hear()" function will be transported to,
then using the "isContain()" function to compare with the keyword.
If the keyword is found, then the corresponding function will be called.
"""
def Processing(text):
    # Call functional classes in "ControlComputer"
    system = SystemOptions()
    tab = tabWorking()
    window = WindowWorking()

    # Transform the command into lower case
    text = text.lower()

    # Greeting and communicating
    if isContain(text, ["chào"]):
        speak(choice(greeting))
    elif isContain(text, ["biệt"]):
        speak("Tạm biệt! Hẹn gặp lại")
    
    # Current time and date handling
    elif is_asking_current_date(text):
        speak(DateTime().currentDate())
    elif is_asking_current_time(text):
        speak(DateTime().currentTime())
    
    # Opening applications or webpages (each per time)
    elif isContain(text, ["mở"]):
        if isContain(text, ["tab", "trang"]):
            tab.newTab()
            speak("Đã thêm trang web")
        else:
            appName = text.replace("mở", "").strip()
            if not appName == "":
                system.openApp(appName)
                speak("Đã mở " + appName)
    
    # Interacting with webpages
    elif isContain(text, ["thêm", "mới"]):
        if isContain(text, ["trang", "tab"]):
            tab.newTab()
            speak("Đã thêm tab mới!")
        else:
            pass
    elif isContain(text, ["chuyển"]):
        if isContain(text, ["trang", "tab"]):
            tab.switchTab()
            speak("Đã chuyển trang web")
        else:
            pass
    
    # Closing applications or webpages (each per time)
    elif isContain(text, ["đóng"]):
        if isContain(text, ["tab", "trang"]):
            tab.closeTab()
            speak("Đã đóng trang web")
        else:
            appName = text.replace("đóng", "").strip()
            if not appName == "":
                system.closeApp(appName)
                speak("Đã đóng " + appName)
    
    # Capturing and screen shooting
    elif isContain(text, ["chụp"]):
        if isContain(text, ["ảnh"]):
            speak("Sẵn sàng nhé!")
            window.clickPhoto()
        elif isContain(text, ["màn hình"]):
            window.takeScreenshot02()
            speak("Tôi đã chụp màn hình!")
        else:
            pass
    
    # Show users' captured images
    elif isContain(text, ["xem hình"]):
        window.viewLatestScreenshot()
    elif isContain(text, ["xem ảnh"]):
        window.viewPhoto()
        speak("Đây là ảnh của bạn!")
    
    # Video controlling on YouTube
    elif isContain(text, ["dừng"]):
        window.stopVideo()
        speak("Đã dừng!")
    elif isContain(text, ["phát", "tiếp tục"]):
        window.playVideo()
        speak("Xem vui nhé!")
    elif isContain(text, ["toàn màn hình"]):
        window.controlFullscreenMode()
        speak("Vâng!")
    elif isContain(text, ["phụ đề"]):
        window.controlSubtitleMode()
        if "bật" in text:
            speak("Đã bật phụ đề!")
        elif "tắt" in text:
            speak("Đã tắt phụ đề!")
    elif isContain(text, ["rạp chiếu"]):
        window.controlCinemaMode()
        if "bật" in text:
            speak("Đã bật rạp chiếu!")
        elif "tắt" in text:
            speak("Đã tắt rạp chiếu!")
    
    # Math Operations
    elif isContain(text, ["+", "-", "*", "/", ":", "cộng", "trừ", "nhân", "chia"]):
        speak(basicOperations(text))
    
    # Laptop Controlling
    elif isContain(text, ["tắt máy", "shutdown"]):
        speak("Đang tắt máy tính. Tạm biệt")
        time.sleep(2)
        os.system("shutdown /s /t 0")
    elif isContain(text, ["khởi động lại", "restart"]):
        speak("Đang chuẩn bị khởi động lại máy tính")
        time.sleep(2)
        os.system("shutdown /r /t 0")
    elif isContain(text, ["ngủ"]):
        speak("Máy tính đang vào chế độ ngủ đông!")
        time.sleep(2)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0, 1, 0")
    
    # Searching on Google, YouTube, WWikipedia
    elif isContain(text, ["tìm kiếm"]):
        if "google" in text:
            speak("Bạn đang muốn tìm gì trên Google?")
            text = hear()
            url = f"https://www.google.com/search?q={text}"
            webbrowser.open(url)
            speak("Đây là kết quả tôi tìm được trên Google!")
        elif "youtube" in text:
            speak("Bạn muốn xem gì trên YouTube?")
            text = hear()
            url = f"https:/www.youtube.com/results?search_query={text}"
            webbrowser.open(url)
            speak("Đây là kết quả tôi tìm được trên YouTube")
        elif "wikipedia" in text:
            speak("Bạn muốn tìm hiểu về gì?")
            text = hear()
            resultPages = wikipedia.search(text)
            if resultPages:
                page = wikipedia.page(resultPages[0])
                speak(page.summary)
    
    # Volume controlling
    elif isContain(text, ["tăng", "giảm"]):
        speak(window.controlVolum(text))
    
    # Exceptional cases
    else:
        pass

"""
This function is used to quit window.
When the user click to the quit button, this function will be called.
"""
def quitWindow():
    global receive
    receive = False # This flag is used to stop the thread
    window.destroy() # Destroy the main window
    listening.join() # Stop the thread

"""
These three functions are used to change the icon of the microphone when listening and stop.
"""
# Stop-flag-02
isListening = False # This flag is used to stop the microphone usage
# Active microphone icon
def activate_microphone():
    global isListening
    isListening = True
    threeDots = customtkinter.CTkImage(light_image=Image.open("Assets/Images/threeDots.png"), dark_image=Image.open("Assets/Images/threeDots.png"), size=(40, 40))
    MicrophoneButton.configure(image = threeDots)

# Deactive microphone icon
def deactivate_microphone():
    global isListening
    isListening = False
    micIconImage = customtkinter.CTkImage(light_image=Image.open("Assets/Images/MicrophoneIcon.png"), dark_image=Image.open("Assets/Images/MicrophoneIcon.png"), size=(40, 40))
    MicrophoneButton.configure(image = micIconImage)

# Total function
def transfer():
    global isListening
    if not isListening:
        activate_microphone()
        MicrophoneButton.update()
        hearing = Thread(target=hear)
        hearing.start()
    else:
        deactivate_microphone()

"""
This function is used to open ".pdf" guider file
"""
def openGuider():
    os.system(f"start {'Assets/Guider/Guider.pdf'}")

"""
THIS IS THE MAIN BODY OF THE PROGRAM
- In this place, the User Interface is coded.
"""
if __name__ == "__main__":
    listening = Thread(target=voiceMedia, daemon=True)
    listening.start()

    # Initialize the appearance of the app
    customtkinter.set_appearance_mode("System")
    window = customtkinter.CTk()

    # Appearance setting up.
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    desired_x = (screen_width - window_width) // 2
    desired_y = screen_height - window_height - 10
    window.geometry(f"+{desired_x - 50}+{desired_y}")
    window.overrideredirect(True)

    # Initialize the buttons
    voiceInput = customtkinter.CTkFrame(window, corner_radius=5)
    voiceInput.pack(padx=5, pady=5)
    voiceInput.grid_columnconfigure(0, weight=0)
    voiceInput.grid_columnconfigure(1, weight=1)
    voiceInput.grid_columnconfigure(2, weight=0)

    # Guider button
    guiderImage = customtkinter.CTkImage(light_image=Image.open("Assets/Images/GuiderIconDark.png"), dark_image=Image.open("Assets/Images/GuiderIconDark.png"), size=(40, 40))
    guiderButton = customtkinter.CTkButton(voiceInput, text="", width=25, height=25, corner_radius=5, bg_color="transparent", fg_color="transparent", hover=False, image=guiderImage, command=lambda: [openGuider()])
    guiderButton.grid(row=0, column=0, padx=5, pady=5)

    # Microphone button
    MicrophoneImage = customtkinter.CTkImage(light_image=Image.open("Assets/Images/MicrophoneIcon.png"), dark_image=Image.open("Assets/Images/MicrophoneIcon.png"), size=(40, 40))
    MicrophoneButton = customtkinter.CTkButton(voiceInput, text="", width=50, height=50, corner_radius=5, image=MicrophoneImage, command=lambda: [transfer()])
    MicrophoneButton.grid(row=0, column=1, padx=5, pady=5)

    # Quit button
    quitImage = customtkinter.CTkImage(light_image=Image.open("Assets/Images/QuitIconDark.png"), dark_image=Image.open("Assets/Images/QuitIconLight.png"), size=(20, 20))
    quitButton = customtkinter.CTkButton(voiceInput, text="", width=50, height=50, corner_radius=5, image=quitImage, bg_color="transparent", fg_color="transparent", hover=False, command=lambda: [quitWindow()])
    quitButton.grid(row=0, column=2, padx=5, pady=5)

    # Program's main loop
    window.protocol("WM_DELETE_WINDOW", quitWindow)
    window.mainloop()

###########################################################################
####                                                                   ####
####                © 2024 Mary Assistant | Tofu Nguyen                ####
####                                                                   ####
###########################################################################