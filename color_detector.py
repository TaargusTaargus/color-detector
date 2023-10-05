import cv2
import numpy as np
import threading
try:
    from PIL import ImageGrab
except ImportError:
    from pyscreenshot import ImageGrab

def simple_ping():
    print( '\a' )
    #duration = 100  # milliseconds
    #frequency = 1000  # Hz (adjust for higher or lower pitch)
    #winsound.Beep(frequency, duration)


def detect_color_in_screenshot(target_color, image_path=None, tolerance=30):
    """
    Detects a given color in an image and returns a list of coordinates where the color is found.

    Parameters:
        target_color (tuple): The target color in RGB format (e.g., (R, G, B)).
        tolerance (int, optional): Tolerance for color similarity. Lower value means stricter matching. Default is 30.

    Returns:
        list: A list of tuples containing the (x, y) coordinates of the detected color in the image.
    """

    img = None

    # check if we've got a file path, if not then take a screenshot
    if image_path:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    else:
        screenshot = ImageGrab.grab()  # Take the screenshot
        # Convert the screenshot to a NumPy array (BGR format) readable by OpenCV
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

    # Define lower and upper bounds of the target color within the specified tolerance
    lower_bound = np.array([max(0, c - tolerance) for c in target_color], dtype=np.uint8)
    upper_bound = np.array([min(255, c + tolerance) for c in target_color], dtype=np.uint8)

    # Create a mask based on the target color range
    mask = cv2.inRange(img, lower_bound, upper_bound)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get the coordinates of the detected color
    detected_coordinates = []
    for contour in contours:
        moments = cv2.moments(contour)
        if moments["m00"]:
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
            detected_coordinates.append((cX, cY))

    return detected_coordinates

def hex_to_rgb(hex_color):
    """
    Convert a hexadecimal color code to an RGB tuple.

    Parameters:
        hex_color (str): The hexadecimal color code (e.g., "#RRGGBB" or "RRGGBB").

    Returns:
        tuple: A tuple containing the RGB values as integers in the range 0-255 (e.g., (R, G, B)).
    """
    hex_color = hex_color.strip("#")
    if len(hex_color) != 6:
        raise ValueError("Invalid hexadecimal color code. It should be in the format '#RRGGBB'.")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)


    
    

