import os

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "images")

STOP_TOKEN = "$CLH_STE_ST$"

FILE_STOP_TOKEN = "$CLH_STE_F$"

VALID_IMAGE_FILE_TYPE = {"PNG": ".png", "JPG": ".jpg", "JPEG": ".jpeg"}

STEGANOGRAPHY_METHODS = ["LSB", "LSBM", "LSBMR", "EA-LSBMR", "PVD"]

LSB_AMOUNT = 2

ENCODE_DATA_TYPE = {"text": "Text", "file": "File"}
