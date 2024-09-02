import pyautogui
import time

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
 
x, y= pyautogui.locateCenterOnScreen("fishing2.png")
pyautogui.moveTo(x, y, duration = 1)
pyautogui.leftClick()