from datetime import datetime
import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con
from deprecated import deprecated
from enum import Enum
import sys

class Event(Enum):
    findStartButtonAndClick = 1
    waitUntilGreenAndFish = 2
    waitUntilPercentThenReelIn = 3
    reapRewards = 4

startButtonValues = {
    "xPercent": 40,
    "yPercent": 90,
    "xScreen": 0,
    "yScreen": 0,
    "thresholdGreen": 200
}

fishBar = {
    "xPercent": 30,
    "yPercent": 70
}

percentFish = {
    "xPercent": 83,
    "yPercent": 75
}

windowTitle = "Bit Heroes" 
stepper = 3
event = Event.findStartButtonAndClick

def log_message(task):
    current_time = datetime.now().strftime('%H:%M:%S')
    log_text = f"[{current_time}] {task}"
    print(log_text)
    
def log_time():
    current_time = datetime.now().strftime('%H:%M:%S')
    log_text = f"[{current_time}]"
    print(log_text, end="")

def getScreenSize():
    screenWidth, screenHeight = pyautogui.size()
    log_message("getScreenSize done")
    return screenWidth, screenHeight

def moveTo(x, y):
    win32api.SetCursorPos((int(x), int(y)))
    log_message("moveTo done")

def quitGame():
    if win32api.GetAsyncKeyState(0x51):
        log_message("Q pressed, exiting loop.")
        sys.exit()

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    log_message("click done")

def space():
    win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
    log_message("space done")

def getPixelInWindow(xOffsetPercentage, yOffsetPercentage):
    windows = gw.getWindowsWithTitle(windowTitle)
    if not windows:
        raise ValueError("No window found with the title: " + windowTitle)
    
    window = windows[0]
    
    left, top, width, height = window.left, window.top, window.width, window.height
    
    if not (0 <= xOffsetPercentage <= 100 and 0 <= yOffsetPercentage <= 100):
        raise ValueError("Percentages must be between 0 and 100.")
    
    xOffset = int(xOffsetPercentage / 100 * width)
    yOffset = int(yOffsetPercentage / 100 * height)

    screenX = left + xOffset
    screenY = top + yOffset

    return screenX, screenY

def getPixelInWindowColor(xOffsetPercentage, yOffsetPercentage):
    windows = gw.getWindowsWithTitle(windowTitle)
    if not windows:
        raise ValueError("No window found with the title: " + windowTitle)
    
    window = windows[0]
    
    left, top, width, height = window.left, window.top, window.width, window.height
    
    if not (0 <= xOffsetPercentage <= 100 and 0 <= yOffsetPercentage <= 100):
        raise ValueError("Percentages must be between 0 and 100.")
    
    xOffset = int(xOffsetPercentage / 100 * width)
    yOffset = int(yOffsetPercentage / 100 * height)
    
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    pixelColor = screenshot.getpixel((xOffset, yOffset))
    return pixelColor

def getPixelInWindowCANDS(xOffsetPercentage, yOffsetPercentage):
    windows = gw.getWindowsWithTitle(windowTitle)
    if not windows:
        raise ValueError("No window found with the title: " + windowTitle)
    
    window = windows[0]
    
    left, top, width, height = window.left, window.top, window.width, window.height
    
    if not (0 <= xOffsetPercentage <= 100 and 0 <= yOffsetPercentage <= 100):
        raise ValueError("Percentages must be between 0 and 100.")
    
    xOffset = int(xOffsetPercentage / 100 * width)
    yOffset = int(yOffsetPercentage / 100 * height)

    screenX = left + xOffset
    screenY = top + yOffset

    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    pixelColor = screenshot.getpixel((xOffset, yOffset))

    return pixelColor, screenX, screenY


def findStartButtonAndClick():
    global event
    color, screenX, screenY = getPixelInWindowCANDS(startButtonValues["xPercent"], startButtonValues["yPercent"])
    green = color[1]
    startButtonValues["xScreen"] = screenX
    startButtonValues["yScreen"] = screenY
    moveTo(screenX,screenY)
    log_message("move cursor to button")
    if(green > startButtonValues["thresholdGreen"]):
        click()
        log_message("found and clicked start button, findStartButtonAndClick done")
        event = Event.waitUntilGreenAndFish
    log_message("could not find button, findStartButtonAndClick unsuccessfull")

def waitUntilGreenAndFish():
    global event
    color = getPixelInWindowColor(fishBar["xPercent"], fishBar["yPercent"])
    green = color[1]
    if(green > startButtonValues["thresholdGreen"]):
        moveTo(startButtonValues["xScreen"], startButtonValues["yScreen"])
        click()
        log_message("the bar is green, casting line, waitUntilGreenAndFish done")
        event = Event.waitUntilPercentThenReelIn
    log_message("could not find green, waitUntilGreenAndFish unsuccessfull")

def waitUntilPercentThenReelIn():
    global event
    windows = gw.getWindowsWithTitle(windowTitle)
    if not windows:
        raise ValueError(f"No window found with the title: {windowTitle}")
    
    window = windows[0]
    left, top, width, height = window.left, window.top, window.width, window.height

    if not (0 <= percentFish["xPercent"] <= 100 and 0 <= percentFish["yPercent"] <= 100):
        raise ValueError("Percentages must be between 0 and 100.")
    
    xOffset = int(percentFish["xPercent"] / 100 * width)
    yOffset = int(percentFish["yPercent"] / 100 * height)
    
    screenX, screenY = left + xOffset, top + yOffset

    duration = 26
    startTime = time.time()

    for i in range(screenX, int(screenX + (2 / 100 * width)), stepper):
        moveTo(i, screenY)
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        color = screenshot.getpixel((i - left, yOffset))
        green, red = color[1], color[0]
        log_message(f"Green: {green}")
        if green > startButtonValues["thresholdGreen"] and red < 200:
            moveTo(startButtonValues["xScreen"], startButtonValues["yScreen"])
            click()
            log_message("100%, reeling in line, forSearchPattern done")
            event =  Event.reapRewards
            return
        if time.time() - startTime > duration:
            log_message("this is trash, skipping")
            event =  Event.reapRewards
            return

try:
    while True:
        match event:
            case Event.findStartButtonAndClick:
                time.sleep(0.5)
                findStartButtonAndClick()
            case Event.waitUntilGreenAndFish:
                waitUntilGreenAndFish()
            case Event.waitUntilPercentThenReelIn:
                waitUntilPercentThenReelIn()
            case Event.reapRewards:
                time.sleep(3)
                space()
                time.sleep(1)
                space()
                log_message("iteration over, fishing again")
                event = Event.findStartButtonAndClick
        quitGame()
    
except ValueError as e:
    print("error has occured: " + e)