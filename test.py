import pyautogui
import time
import cv2

def switch_to_next_desktop():
    # Press Win + Ctrl + Right Arrow
    pyautogui.hotkey('win', 'ctrl', 'right')
    time.sleep(2)  # Allow time for the switch to occur

def switch_to_previous_desktop():
    # Press Win + Ctrl + Left Arrow
    pyautogui.hotkey('win', 'ctrl', 'left')
    time.sleep(2)  # Allow time for the switch to occur

# Switch to the next desktop
switch_to_next_desktop()

# Wait a bit before running the auto_fish function


# Your auto_fish function here
def auto_fish():
    foundbutton = False
    foundPerfect = False
    foundPerfectPerfect = False
    fishing_button = None
    while True:
        # Capture screen or check for specific image
        if foundbutton == False:
            fishing_button = pyautogui.locateCenterOnScreen('fishing2.png',  confidence=0.8)
        if foundbutton == True:
            fishing_button = pyautogui.locateCenterOnScreen('fishing2.png',  confidence=0.6)
        
        if fishing_button and foundbutton == False:
            # Click on the fishing button
            pyautogui.click(fishing_button)
            print("Fishing button clicked!")
            foundbutton = True
            fishing_button = None
            time.sleep(0.3)

        if fishing_button:
            # Click on the fishing button
            pyautogui.click(fishing_button)
            print("Fishing found found clicked!")
            foundPerfect = True

        
        # Wait before next check
        time.sleep(10)

auto_fish()



switch_to_previous_desktop()
#Mouse clicked at (1425, 1452)

"""
from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")

# Set up the listener for mouse events
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
"""
