import cv2

def load_image(path: str):
    """Load image from disk using OpenCV."""
    image = cv2.imread(path)
    return image

def to_rgb(image):
    """Convert BGR (OpenCV) image to RGB."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
