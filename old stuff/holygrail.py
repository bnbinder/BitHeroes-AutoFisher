from datetime import datetime
import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con
from deprecated import deprecated

startColorThresh = 200
hoverOverColorThresh = 230
xOne = 40
yOne = 90
xTwo = 30
yTwo = 70
scanX = 82
scanY = 75
submitCoord = [0,0]
windowTitle = "Bit Heroes"  
trash = False

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

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    log_message("click done")

def space():
    win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)

def getPixelInWindow(windowTitle, xOffsetPercentage, yOffsetPercentage):
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

    log_message("getPixelInWindow Done")
    
    return pixelColor, screenX, screenY

def proceed(windowsTitle):
    global submitCoord
    color, screenX, screenY = getPixelInWindow(windowsTitle, xOne, yOne)
    green = color[1]
    submitCoord = [screenX,screenY]
    moveTo(screenX,screenY)
    log_message("move cursor to button")
    if(green > startColorThresh):
        click()
        log_message("found and clicked start button, proceed done")
        return True
    log_message("could not find button, proceed done unsuccessfully")
    return False

def waitUntilGreen(windowsTitle):
    while True:
        color = getPixelInWindow(windowsTitle, xTwo, yTwo)
        green = color[0][1]
        if(green > startColorThresh):
            moveTo(submitCoord[0], submitCoord[1])
            click()
            break
    log_message("the bar is green, casting line, waitUntilGreen done")
    return True

@deprecated(version='1.0.0', reason="Use forSearchPattern instead")
def searchForMatch(windowsTitle):
    while True:
        color = getPixelInWindow(windowsTitle, scanX, scanY)
        green = color[0][1]
        if(green > startColorThresh):
            print("it green")
            moveTo(submitCoord[0], submitCoord[1])
            click()
            break
    return True

@deprecated(version='1.0.0', reason="no need for this lol")
def getPixelInWindowRaw(windowTitle, xOffset, yOffset):
    windows = gw.getWindowsWithTitle(windowTitle)
    if not windows:
        raise ValueError("No window found with the title: " + windowTitle)
    
    window = windows[0]
    
    left, top, width, height = window.left, window.top, window.width, window.height
    
    if not (0 <= xOffset <= width and 0 <= yOffset <= height):
        raise ValueError("Offsets must be within the window's dimensions.")
    
    screenX = left + xOffset
    screenY = top + yOffset
    
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    pixelColor = screenshot.getpixel((xOffset, yOffset))

    log_message("getPixelInWindowRaw Done")

    return pixelColor, screenX, screenY

@deprecated(version='1.0.0', reason="split up into subfunctions")
def forSearchPatternOld():
    xOffsetPercentage = 83
    yOffsetPercentage = 75
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

    """
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    pixelColor = screenshot.getpixel((left-submitCoord[0],top-submitCoord[1]))
    time.sleep(3)
    if pixelColor[1] < 10:
        return 0
    """
    #grid sweep the screen for the time before you are playing the game to see if screen is black
    #make sure grid sweep does not touch white letters or image

    while True:
        for i in range(screenX,int(screenX+(2 / 100 * width)), 3):
            moveTo(i,screenY)
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            pixelColor = screenshot.getpixel((i-left, yOffset))
            color = pixelColor
            green = color[1]
            log_message("grreen: " + str(green))
            red = color[0]
            if green > startColorThresh and red < 200:
                moveTo(submitCoord[0], submitCoord[1])
                click()
                log_message("100%, reeling in line, forSearchPattern done")
                return 0
            if win32api.GetAsyncKeyState(0x51):
                print("Q pressed, exiting loop.")
                return 0
            
def getScreenValues(xOffsetPercentage, yOffsetPercentage):
    windows = gw.getWindowsWithTitle(windowTitle)
    if not windows:
        raise ValueError(f"No window found with the title: {windowTitle}")
    
    window = windows[0]
    left, top, width, height = window.left, window.top, window.width, window.height

    validatePercentages(xOffsetPercentage, yOffsetPercentage)
    
    xOffset, yOffset = calculateOffsets(xOffsetPercentage, yOffsetPercentage, width, height)
    screenX, screenY = left + xOffset, top + yOffset
    return screenX, screenY, width, left, top, height, xOffset, yOffset
            
def forSearchPattern():
    screenX, screenY, width, left, top, height, xOffset, yOffset = getScreenValues(83, 75)
    scanForColor(screenX, screenY, width, left, top, height, yOffset)
    
def validatePercentages(xOffsetPercentage, yOffsetPercentage):
    if not (0 <= xOffsetPercentage <= 100 and 0 <= yOffsetPercentage <= 100):
        raise ValueError("Percentages must be between 0 and 100.")

def calculateOffsets(xOffsetPercentage, yOffsetPercentage, width, height):
    xOffset = int(xOffsetPercentage / 100 * width)
    yOffset = int(yOffsetPercentage / 100 * height)
    return xOffset, yOffset

def scanForColor(screenX, screenY, width, left, top, height, yOffset):
    global trash
    duration = 25
    startTime = time.time()
    while True:
        for i in range(screenX, int(screenX + (2 / 100 * width)), 3):
            moveTo(i, screenY)
            pixelColor = capturePixelColor(i, left, top, width, height, yOffset)
            if time.time() - startTime > duration:
                trash = True
                log_message("this is trash, skipping")
                return
            if isStartColor(pixelColor):
                triggerAction()
                return
            if checkExitKey():
                return

def capturePixelColor(i, left, top, width, height, yOffset):
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    return screenshot.getpixel((i - left, yOffset))

def isStartColor(color):
    green, red = color[1], color[0]
    log_message(f"Green: {green}")
    return green > startColorThresh and red < 200

def isBlack(color, blackThresh):
    r,g,b = color[0], color[1], color[2]
    log_message(f"Red: {r}, Green: {g}, Blue {b}")
    return r < blackThresh and g < blackThresh and b < blackThresh

def triggerAction():
    moveTo(submitCoord[0], submitCoord[1])
    click()
    log_message("100%, reeling in line, forSearchPattern done")

def checkExitKey():
    if win32api.GetAsyncKeyState(0x51):  # Q key
        print("Q pressed, exiting loop.")
        return True
    return False


def gridSweep(): 
    gridX = [10, 20, 30, 60, 70, 80]    
    gridY = [20, 40]
    colors = [0] * 12 
    black = True
    avgColor = [0,0,0]
    for x in range(0, 6):
        for y in range (0,2):
            screenX, screenY, width, left, top, height, xOffset, yOffset = getScreenValues(gridX[x], gridY[y])
            pixelColor = capturePixelColor(screenX, left, top, width, height, yOffset)
            moveTo(screenX, screenY)
            colors[x * 2 + y] = pixelColor
    for i in range(0,12):
        for j in range(0,3):
            avgColor[j] = colors[i][j]  
    r = avgColor[0]
    g = avgColor[1]
    b = avgColor[2]
    if not isBlack(pixelColor, 10):
        black = False
    log_message(f"avgRed: {r}, avgGreen: {g}, avgBlue {b}")
    log_message(f"is black: {black}")


#start

try:
    #pyautogui.displayMousePosition()
    #color, screenX, screenY = getPixelInWindow(windowTitle,scanX, scanY)
    #moveTo(screenX, screenY)
    #print(f"Color of pixel at ({xOne}%, {yOne}%) in the window: {color}")
    
    while True:
        foundIt = False
        clickedIt = False
        foundIt = proceed(windowTitle)
        if foundIt:
            log_message("found it true")
            clickedIt = waitUntilGreen(windowTitle)
        if clickedIt: 
            log_message("clicked it true")
            #searchForMatch(windowTitle)
            forSearchPattern()
            log_message("for search pattern done")
            time.sleep(3)
            log_message("space done")
            space()
            time.sleep(1)
            log_message("second space done")
            space()
            time.sleep(1)
            print("wedone")
        if win32api.GetAsyncKeyState(0x51):
            print("Q pressed, exiting loop.")
            break
    
    #proceed(xOffsetPercentage,yOffsetPercentage,windowTitle)
    #click(screenX, screenY)
except ValueError as e:
    print(e)
