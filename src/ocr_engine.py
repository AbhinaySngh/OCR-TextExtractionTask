import cv2
import pytesseract
from pytesseract import Output

from .preprocessing import to_rgb

def correct_orientation(image):
    """
    Use Tesseract OSD to detect orientation and rotate image if needed.
    """
    try:
        rgb = to_rgb(image)
        results = pytesseract.image_to_osd(
            rgb,
            output_type=Output.DICT
        )  # orientation + rotate info[web:37][web:36][web:39]

        angle = results.get("rotate", 0)
        if angle != 0:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, -angle, 1.0)
            rotated = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_LINEAR,
                borderMode=cv2.BORDER_REPLICATE
            )
            return rotated
    except Exception as e:
        print("Orientation detection failed:", e)

    return image


def run_ocr(image):
    """
    Run OCR on an (optionally oriented) image and return pytesseract data dict.
    """
    rgb_img = to_rgb(image)
    data = pytesseract.image_to_data(
        rgb_img,
        output_type=Output.DICT
    )  # text, conf, block_num, par_num, line_num, etc.[web:4][web:22]

    return data
