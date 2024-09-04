import pyautogui
import pygetwindow as gw
import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con

def click_in_relative_position(window_title, rel_x, rel_y):
    # Get the window
    window = gw.getWindowsWithTitle(window_title)[0]
    
    # Calculate the absolute coordinates
    abs_x = window.left + int(rel_x * window.width)
    abs_y = window.top + int(rel_y * window.height)
    
    # Perform the click
    win32api.SetCursorPos((int(abs_x), int(abs_y)))

# Example usage
window_title = "Bit Heroes"  # Replace with your window title
relative_x = 0.5  # 50% of the window width
relative_y = 0.5  # 50% of the window height
click_in_relative_position(window_title, relative_x, relative_y)
