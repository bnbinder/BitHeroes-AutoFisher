import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con

def get_screen_size():
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height

def click(x, y):
    win32api.SetCursorPos((int(x), int(y)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def get_pixel_in_window(window_title, x_offset_percentage, y_offset_percentage):
    # Find the window by title
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        raise ValueError("No window found with the title: " + window_title)
    
    # Get the first window that matches the title
    window = windows[0]
    
    # Get window coordinates and size
    left, top, width, height = window.left, window.top, window.width, window.height
    
    # Ensure percentages are within valid range
    if not (0 <= x_offset_percentage <= 100 and 0 <= y_offset_percentage <= 100):
        raise ValueError("Percentages must be between 0 and 100.")
    
    # Calculate the offset in pixels based on percentages
    x_offset = int(x_offset_percentage / 100 * width)
    y_offset = int(y_offset_percentage / 100 * height)
    
    # Calculate the absolute pixel position relative to the screen
    screen_x = left + x_offset
    screen_y = top + y_offset
    
    # Capture only the window area to get the pixel color
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    pixel_color = screenshot.getpixel((x_offset, y_offset))
    
    return pixel_color, screen_x, screen_y


# Example usage
window_title = "Bit Heroes"  # Replace with your window title
x_offset = 300  # X offset within the window
y_offset = 300  # Y offset within the window

window_title = "Bit Heroes"  # Replace with your window title
x_offset_percentage = 25  # 25% from the left
y_offset_percentage = 50  # 50% from the top

try:
    color, screen_x, screen_y = get_pixel_in_window(window_title, x_offset_percentage, y_offset_percentage)
    print(f"Color of pixel at ({x_offset_percentage}%, {y_offset_percentage}%) in the window: {color}")
    click(screen_x, screen_y)
except ValueError as e:
    print(e)
