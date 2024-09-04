import pygetwindow as gw
import pyautogui
import time
import win32api
import win32con

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

def getScreenSize():
    screenWidth, screenHeight = pyautogui.size()
    return screenWidth, screenHeight

def moveTo(x, y):
    win32api.SetCursorPos((int(x), int(y)))

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

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
    
    return pixelColor, screenX, screenY

def proceed(windowsTitle):
    global submitCoord
    color, screenX, screenY = getPixelInWindow(windowsTitle, xOne, yOne)
    green = color[1]
    print(green)
    submitCoord = [screenX,screenY]
    moveTo(screenX,screenY)
    if(green > startColorThresh):
        click()
        print("found it")
        return True
    print("not there")
    return False

def waitUntilGreen(windowsTitle):
    while True:
        color = getPixelInWindow(windowsTitle, xTwo, yTwo)
        green = color[0][1]
        if(green > startColorThresh):
            print("it green")
            moveTo(submitCoord[0], submitCoord[1])
            click()
            break
    return True

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
    
    return pixelColor, screenX, screenY

def forSearchPattern():
    xOffsetPercentage = 82
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
    while True:
        for i in range(screenX,int(screenX+(2 / 100 * width))):
            moveTo(i,screenY)
            color = getPixelInWindowRaw(windowTitle,i-left,screenY-top)
            green = color[0][1]
            red = color[0][0]
            if green > startColorThresh and red < 200:
                print("it green")
                moveTo(submitCoord[0], submitCoord[1])
                click()
                return 0
            if win32api.GetAsyncKeyState(0x51):
                print("Q pressed, exiting loop.")
                return 0

        
    

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
            clickedIt = waitUntilGreen(windowTitle)
        if clickedIt: 
            #searchForMatch(windowTitle)
            forSearchPattern()

        time.sleep(2)
        click()
        time.sleep(1)
        win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)
        time.sleep(0.05)  # Add a short delay to simulate key press duration
        # Release the space bar
        win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(1)
        print("wedone")
        if win32api.GetAsyncKeyState(0x51):
            print("Q pressed, exiting loop.")
            break
    
    #proceed(xOffsetPercentage,yOffsetPercentage,windowTitle)
    #click(screenX, screenY)
except ValueError as e:
    print(e)
