import base64
from io import BytesIO
import time
from tkinter import filedialog, messagebox
from typing import Any

import numpy as np
from PIL import Image, ImageFile

from src.constants import LSB_AMOUNT, ENCODE_DATA_TYPE, STOP_TOKEN, FILE_STOP_TOKEN
from src.utils.aes_cipher import AESCipher


class Steganography:
    def __init__(self, image: ImageFile.ImageFile):
        self.image = image

        self.image_width, self.image_height = image.size
        self.image_arr: np.ndarray[Any] = np.array(list(self.image.getdata()))

        self.image_channel = 4 if image.mode == "RGBA" else 3
        print(self.image_channel)
        self.image_pixel = self.image_arr.size // self.image_channel
        print(self.image_pixel)
        self.stop_token = STOP_TOKEN
        self.file_stop_token = FILE_STOP_TOKEN

    def ask_for_file_path(self, filename: str, filetypes: list[tuple[str, str]]) -> str:
        filename_without_extension = filename[: filename.rindex(".")]
        current_timestamp = int(time.time())
        path = filedialog.asksaveasfilename(
            initialfile=f"{filename_without_extension}-ste-{current_timestamp}",
            filetypes=filetypes,
            defaultextension=filetypes[0][1],
        )
        return path

    def lsb_encode(
        self, message: str, password: str, encoded_file_name: str, data_type: str
    ) -> str:
        enc_message = AESCipher().encrypt(message, password)
        enc_message += (
            self.stop_token
            if data_type == ENCODE_DATA_TYPE.get("text")
            else self.file_stop_token
        )
        byte_message = "".join(f"{ord(c):08b}" for c in enc_message)
        bit = len(byte_message)

        if bit > self.image_pixel * LSB_AMOUNT:
            messagebox.showerror("Error", "Not enough space to encode.")
            return "fail"

        index = 0
        for i in range(self.image_pixel):
            for j in range(0, 3):
                if index < bit:
                    self.image_arr[i][j] = int(
                        bin(self.image_arr[i][j])[2:-LSB_AMOUNT]
                        + byte_message[index : index + LSB_AMOUNT],
                        2,
                    )
                    index += LSB_AMOUNT

        self.image_arr = self.image_arr.reshape(
            self.image_height, self.image_width, self.image_channel
        )
        result = Image.fromarray(self.image_arr.astype("uint8"), mode=self.image.mode)

        save_path = self.ask_for_file_path(encoded_file_name, [("PNG", ".png")])
        if save_path == "":
            return "fail"

        result.save(save_path)
        return "success"

    def lsb_decode(self, password: str) -> str:
        secret_bit = [
            bin(self.image_arr[i][j])[2:].zfill(8)[-LSB_AMOUNT:]
            for i in range(self.image_pixel)
            for j in range(0, 3)
        ]
        secret_bit = "".join(secret_bit)
        secret_bit = [secret_bit[i : i + 8] for i in range(0, len(secret_bit), 8)]
        enc_message = "".join([chr(int(i, 2)) for i in secret_bit])
        is_file = False

        if self.stop_token in enc_message:
            enc_message = enc_message[: enc_message.index(self.stop_token)]
        elif self.file_stop_token in enc_message:
            is_file = True
            enc_message = enc_message[: enc_message.index(self.file_stop_token)]
        else:
            messagebox.showerror("Error", "No message found.")
            return "fail"

        try:
            message = AESCipher().decrypt(enc_message, password)
        except Exception:
            messagebox.showerror("Error", "Incorrect secret word.")
            return "fail"

        if not is_file:
            save_path = self.ask_for_file_path("text.txt", [("Text file", ".txt")])

            if save_path == "":
                return "fail"

            f = open(save_path, "w")
            f.write(message)
            f.close()
        else:
            save_path = self.ask_for_file_path("image.png", [("PNG", ".png")])

            if save_path == "":
                return "fail"

            image = Image.open(BytesIO(base64.b64decode(message)))
            image.save(save_path)

        return "success"
