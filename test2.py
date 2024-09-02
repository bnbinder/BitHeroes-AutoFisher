import mss
import easyocr
from PIL import Image
import numpy as np
import cv2

def capture_screen():
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader for English

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Use monitor[1] for the primary screen

        while True:
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            img_np = np.array(img)
            
            # Perform OCR using EasyOCR
            results = reader.readtext(img_np)
            
            # Extract and print text
            for result in results:
                print(result[1])
            
            # Display the image
            #cv2.imshow('Screen Capture', img_np)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

capture_screen()
