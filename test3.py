from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
import mss

def get_screen_region(screen_width, screen_height, capture_width=600, capture_height=600):
    left = (screen_width - capture_width) // 2
    top = (screen_height - capture_height) // 2
    return {"top": top, "left": left, "width": capture_width, "height": capture_height}

def compare_images(image1, image2):
    # Convert images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM
    score, diff = ssim(gray_image1, gray_image2, full=True)
    
    # Convert difference image to uint8 for display
    diff = (diff * 255).astype(np.uint8)
    
    # Display the difference image
    cv2.imshow("Difference", diff)
    
    # Threshold SSIM score to determine similarity
    print(score)
    if score > 0.95:  # Adjust the threshold as needed
        print("Images are similar")
        return True
    else:
        print("Images are different")
        return False

def main():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screen_width = monitor['width']
        screen_height = monitor['height']
        
        capture_width = 1920
        capture_height = 300
        region = get_screen_region(1700, 1700, int(capture_width/4),  int(capture_height/4))
        
        # Load reference image
        reference_image = cv2.imread('fishing2.png')
        if reference_image is None:
            print("Error loading reference image")
            return

        while True:
            # Capture the screen
            img = sct.grab(region)
            img_np = np.array(img)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # Resize the captured image to match the reference image size if needed
            img_resized = cv2.resize(img_bgr, (reference_image.shape[1], reference_image.shape[0]))

            # Compare the images
            if compare_images(img_resized, reference_image):
                break

            # Display captured image (optional)
            cv2.imshow("Screen Capture", img_bgr)

            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
