import time
from tkinter import filedialog, messagebox
from typing import Any

import numpy as np
from PIL import Image, ImageFile


class Steganography:
    def __init__(self, image: ImageFile.ImageFile):
        self.image = image

        self.image_width, self.image_height = image.size
        self.image_arr: np.ndarray[Any] = np.array(list(self.image.getdata()))

        self.image_channel = 4 if image.mode == "RGBA" else 3
        self.image_pixel = self.image_arr.size // self.image_channel

    def __ask_for_file_path(self, filename: str) -> str:
        filename_without_extension = filename[: filename.rindex(".")]
        current_timestamp = int(time.time())
        path = filedialog.asksaveasfilename(
            initialfile=f"{filename_without_extension}-ste-de-{current_timestamp}",
            filetypes=[("PNG", ".png")],
        )
        return path

    def lsb_encode(self, message: str, stop_token: str, encoded_file_name: str) -> str:
        message += f"${stop_token}$"
        byte_message = "".join(f"{ord(c):08b}" for c in message)
        bit = len(byte_message)

        if bit > self.image_pixel * 2:
            messagebox.showerror("Error", "Not enough space to encode.")
            return "fail"

        index = 0
        for i in range(self.image_pixel):
            for j in range(0, 3):
                if index < bit:
                    self.image_arr[i][j] = int(
                        bin(self.image_arr[i][j])[2:-2]
                        + byte_message[index : index + 2],
                        2,
                    )
                    index += 2

        self.image_arr = self.image_arr.reshape(
            self.image_height, self.image_width, self.image_channel
        )
        result = Image.fromarray(self.image_arr.astype("uint8"), mode=self.image.mode)

        save_path = self.__ask_for_file_path(encoded_file_name)
        if save_path == "":
            return "fail"

        result.save(save_path)
        return "success"

    def lsb_decode(self, stop_token: str):
        secret_bit = [
            bin(self.image_arr[i][j])[2:].zfill(8)[-2:]
            for i in range(self.image_pixel)
            for j in range(0, 3)
        ]
        secret_bit = "".join(secret_bit)
        secret_bit = [secret_bit[i : i + 8] for i in range(0, len(secret_bit), 8)]
        secret_message = "".join([chr(int(i, 2)) for i in secret_bit])

        if f"${stop_token}$" in secret_message:
            print(secret_message[: secret_message.index(f"${stop_token}$")])
        else:
            messagebox.showerror("Error", "No message found.")
