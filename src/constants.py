import os

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "images")

VALID_IMAGE_FILE_TYPE = {"PNG": ".png", "JPG": ".jpg", "JPEG": ".jpeg"}

STEGANOGRAPHY_METHODS = ["LSB", "LSBM", "LSBMR", "EA-LSBMR", "PVD"]

LSB_AMOUNT = 2

ENCODE_DATA_TYPE = {"text": "Text", "file": "File"}
