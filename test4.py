import cv2
import numpy as np
import mss

def get_screen_region(screen_width, screen_height):
    # Capture the entire screen
    return {"top": 0, "left": 0, "width": screen_width, "height": screen_height}

def main():
    # Load the reference image (template) and convert to grayscale
    template = cv2.imread('fishing.png')
    if template is None:
        print("Error loading reference image")
        return
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template_height, template_width = template_gray.shape

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screen_width = monitor['width']
        screen_height = monitor['height']
        
        # Define capture region to cover the entire screen
        region = get_screen_region(screen_width, screen_height)

        while True:
            # Capture the screen
            img = sct.grab(region)
            img_np = np.array(img)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # Convert screen capture to grayscale
            img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

            # Perform template matching
            result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Define a threshold for detecting the presence of the template
            threshold = 0.39  # Adjust this value as needed
            print(max_val)
            if max_val >= threshold:
                print("Template found on screen")
                # Draw rectangle around the detected region
                top_left = max_loc
                bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
                cv2.rectangle(img_bgr, top_left, bottom_right, (0, 255, 0), 2)
                cv2.imshow("Detected", img_bgr)
                cv2.waitKey(0)
                break

            # Display the captured screen
            cv2.imshow("Screen Capture", img_bgr)

            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
