from pyautogui import *
import pyautogui
import time
import time
import keyboard
import random
import win32api, win32con

# for clicking start Mouse Position: (1523, 1338) | RGB Color: (202, 240, 99)
# for clicking edge of bar Mouse Position: (1033, 1193) | RGB Color: (91, 237, 29)

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

isStartClicked = False
time.sleep(2)
while keyboard.is_pressed("q") == False:
    if pyautogui.pixel(1523, 1338)[1] >= 230:
        click(1523,1338)

"""
try:
    while True:
        # Get the current mouse position
        x, y = pyautogui.position()
        
        # Capture the screen at the mouse position
        screenshot = pyautogui.screenshot()
        
        # Get the color of the pixel at the mouse position
        rgb_color = screenshot.getpixel((x, y))
        
        # Print the mouse position and RGB color
        print(f"Mouse Position: ({x}, {y}) | RGB Color: {rgb_color}")
        
        # Wait for a short interval before updating the position
except KeyboardInterrupt:
    print("\nScript stopped by user.")
"""