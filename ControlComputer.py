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
#### Module's name: Computer Controller                                ####
#### Programmer: Nguyen Cong Huy (Nickname: Tofu Nguyen)               ####
#### Finished date: Sunday, December 29, 2024                          ####
###########################################################################

# Import necessary libraries
import os
import re
import cv2
import psutil
import pyautogui
import playsound
import subprocess
from pathlib import Path
from datetime import datetime
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from AppOpener import open, close
from pynput.keyboard import Controller
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Getting audio endpoint volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate (IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.SetMasterVolumeLevelScalar(0.5, None)

"""
This function checks if the provided text contains any of the keywords in the list.
Returns True if any keyword is found, otherwise False.
"""
# Keywords checking function
def isContain(text, list):
    return any(word in text for word in list)

"""
This SystemOptions class is designed to handle system-related tasks. 
It can open and close applications based on their name and check the system for Chrome execuatable files.
"""
class SystemOptions:
    def __init__(self):
        # Initialize a keyword controller to simulate key presses
        self.keyboard = Controller()
    
    """
    This function searches all system drives for the Google Chrome executable.
    It returns the path of the first Chrome executable found or None if no executable is found.
    """
    def find_chrome(self):
        # List of keywords to find files related to Google Chrome
        search_keywords = ["chrome", "google", "browser", "chrome_launcher"]
        # Automatically detect all drives on the system
        search_paths = [disk.device for disk in psutil.disk_partitions() if disk.fstype]
        
        # Browse through all the drives
        for path in search_paths:
            try:
                for root, _, files in os.walk(path):
                    # Browse through all the files in the current folder
                    for file in files:
                        # Check if the file name contains one of the search keywords
                        if any(keyword.lower() in file.lower() for keyword in search_keywords):
                            # Check if the file is an executable file ".exe"
                            if file.lower().endswith(".exe"):
                                # Returns the file path
                                return os.path.join(root, file)
            except PermissionError:
                # Skip paths that raise permission errors
                continue
        # If no file is found, return None
        return None

    """
    Opens an application based on the given name.
    If the app is Chrome, it finds its executable and runs it.
    For Word, it uses the open method from AppOpener to launch it.
    """
    def openApp(self, appName):
        if "google" in appName:
            chromepath = self.find_chrome()
            subprocess.run([chromepath])
        elif "word" in appName or "văn bản" in appName:
            open("word")
        else:
            open(appName, throw_error=True, match_closest=True, output=False)
    
    """
    Closes an application based on the given name.
    Recognizes specific names like Google Chrome, Word, Excel, and PowerPoint, then closes them.
    """
    def closeApp(self, appName):
        if appName == "google":
            close("chrome")
        elif "word" in appName or "văn bản" in appName:
            close("winword")
        elif "excel" in appName or "trang tính" in appName:
            close("excel")
        elif "powerpoint" in appName or "phần mềm trình chiếu" in appName:
            close("powerpnt")
        else:
            close(appName, throw_error=True, match_closest=True, output=False)

"""
This tabWorking class is designed to handle tasks that interact with browser tabs.
It can switch, close, and open new tabs in a browser using simulated keyboard presses.
"""
class tabWorking:
    def __init__(self):
        self.keyboard = Controller()
    
    """
    Switches to the next tab in the browser.
    This simulates the keyboard shortcut 'Ctrl + Tab'.
    """
    def switchTab(self):
        pyautogui.hotkey("ctrl", "tab")
    
    """
    Closes the current tab in the browser.
    This simulates the keyboard shortcut 'Ctrl + W'.
    """
    def closeTab(self):
        pyautogui.hotkey("ctrl", "w")
        
    """
    Opens a new tab in the browser.
    This simulates the keyboard shortcut 'Ctrl + T'.
    """
    def newTab(self):
        pyautogui.hotkey("ctrl", "t")

"""
The WindowWorking class is responsible for tasks related to window management,
such as taking screenshots, capturing images, and controlling video playback.
"""
class WindowWorking:
    def __init__(self):
        self.keyboard = Controller()
        self.imagePath = None

    """
    Gets the path to the default screenshot folder.
    If the folder doesn't exist, it creates it.
    """
    def getScreenShot(self):
        pictureFolder = Path.home() / "Pictures"
        pictureFolder.mkdir(parents=True, exist_ok=True)
        screenshotFolder = pictureFolder / "Screenshots"
        screenshotFolder.mkdir(parents=True, exist_ok=True)
        return screenshotFolder
    
    """
    Takes a screenshot and saves it to the default screenshot folder.
    The filename includes the current date and time.
    """
    def takeScreenshot(self, filename = "Screenshot_"+str(datetime.now())[:19].replace(":", "_")+".png"):
        screenshotFolder = self.getScreenShot()
        filePath = os.path.join(screenshotFolder, filename)
        screenShot = pyautogui.screenshot()
        screenShot.save(filePath)
    
    """
    Takes a screenshot and saves it to the default folder using the 'Win + PrintScreen' shortcut.
    """
    def takeScreenshot02(self):
        pyautogui.hotkey("win", "printscreen")

    """
    Opens the most recent screenshot saved in the 'Pictures/Screenshots' folder.
    """
    def viewLatestScreenshot(self):
        screenshots_folder = Path.home() / "Pictures" / "Screenshots"
        
        if not screenshots_folder.exists():
            print("Thư mục chứa ảnh chụp màn hình không tồn tại.")
            return

        screenshot_files = list(screenshots_folder.glob("*.png"))
        if not screenshot_files:
            print("Không tìm thấy ảnh chụp màn hình nào.")
            return
        
        latest_screenshot = max(screenshot_files, key=os.path.getctime)
        
        # Open Images
        try:
            os.startfile(latest_screenshot)  # Can only be used on Windows OS
            print(f"Đã mở ảnh chụp màn hình: {latest_screenshot}")
        except Exception as e:
            print(f"Lỗi khi mở ảnh chụp màn hình: {e}")
    
    """
    Opens a specific image file after checking if it exists.
    """
    def viewPhoto(self, imagePath):
        if os.path.exists(imagePath):
            try:
                os.startfile(imagePath)
            except Exception as e:
                print(f"Lỗi khi mở ảnh {e}")
        else:
            print("Ảnh không tồn tại")

    """
    Captures a photo using the system's camera and saves it to 'C:\\Camera'.
    The camera is initialized, and the image is saved with the current timestamp in the filename.
    """
    def clickPhoto(self):
        saveFolder = "C:\\Camera"
        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)
        # Initialize the camera
        camera = cv2.VideoCapture(0)

        # Set the resolution (width, height).
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # Set width to 1920 (HD)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Set height to 1080 (HD)

        ret, frame = camera.read()
        if ret:
            playsound.playsound("Assets/Sounds/ClickPhoto.mp3")
            self.imagePath = os.path.join(saveFolder, "Camera_" + str(datetime.now())[:19].replace(':', '_') + '.png')
            cv2.imwrite(self.imagePath, frame)
            self.viewPhoto(imagePath=self.imagePath)
        else:
            pass
        camera.release()
        cv2.destroyAllWindows()
    
    """
    Plays or stops a video that is being played on YouTube.
    This simulates the 'K' key, which is the shortcut for play/pause on YouTube.
    """
    def playVideo(self):
        pyautogui.hotkey("k")

    """
    Stops the video being played on YouTube.
    This simulates the 'K' key, which is the shortcut for play/pause on YouTube.
    """
    def stopVideo(self):
        pyautogui.hotkey("k")

    """
    Maximizes or minimizes a YouTube video by simulating the 'F' key press.
    This key toggles fullscreen mode.
    """
    def controlFullscreenMode(self):
        pyautogui.hotkey("f")

    """
    Toggles subtitles on or off on YouTube by simulating the 'C' key press.
    """
    def controlSubtitleMode(self):
        pyautogui.press("c")

    """
    Toggles cinema mode on YouTube by simulating the 'T' key press.
    """
    def controlCinemaMode(self):
        pyautogui.press("t")

    """
    Extracts numbers from the provided text.
    This function looks for numeric patterns using regular expressions.
    """
    def extractNumbers(self, text):
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0
    
    """
    Controls the volume of the computer.
    This function accesses the system and use pycaw to control the volume.
    """
    def controlVolum(self, text):
        number = self.extractNumbers(text) / 100
        if isContain(text, ["tăng"]):
            if number == 0:
                currentVolumeDb = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(min(currentVolumeDb + 0,1, 1), None)
                currentVolume = volume.GetMasterVolumeLevelScalar() * 100
                return f"Tôi đã tăng âm lượng. Âm lượng hiện tại là {round(currentVolume)}%"
            else:
                volume.SetMasterVolumeLevelScalar(min(number, 1), None)
                return (f"Tôi đã tăng âm lượng lên {min(number, 1) * 100}%")
            
        if isContain(text, ["giảm"]):
            if number == 0:
                currentVolumeDb = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(max(currentVolumeDb - 0.1, 0), None)
                currentVolume = volume.GetMasterVolumeLevelScalar() * 100
                return f"Tôi đã giảm âm lượng. Âm lượng hiện tại là {round(currentVolume)}%"
            else:
                volume.SetMasterVolumeLevelScalar(max(number, 0), None)
                return f"Tôi đã giảm âm lượng còn {max(number, 0) * 100}%"

###########################################################################
####                                                                   ####
####                © 2024 Mary Assistant | Tofu Nguyen                ####
####                                                                   ####
###########################################################################