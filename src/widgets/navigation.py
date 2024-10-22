import os

import customtkinter
from PIL import Image

from src.constants import IMAGE_PATH


class Navigation(customtkinter.CTkFrame):
    def __init__(
        self, parent, on_encode_command, on_decode_command, on_compare_command
    ):
        super().__init__(master=parent, corner_radius=0)
        self.grid(row=0, column=0, sticky="nsew")

        self.on_encode_command = on_encode_command
        self.on_decode_command = on_decode_command
        self.on_compare_command = on_compare_command

        self.title = customtkinter.CTkLabel(
            self,
            text="Digital Image Steganography",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.title.grid(row=0, column=0, padx=20, pady=10)

        self.encode_img = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(IMAGE_PATH, "download.png")),
            dark_image=Image.open(os.path.join(IMAGE_PATH, "download.png")),
            size=(30, 30),
        )
        self.encode_btn = customtkinter.CTkButton(
            self,
            corner_radius=0,
            height=40,
            border_spacing=20,
            text="Encode",
            fg_color="transparent",
            text_color=("grey10", "grey90"),
            hover_color=("grey70", "grey30"),
            image=self.encode_img,
            anchor="w",
            command=self.encode_btn_event,
        )
        self.encode_btn.grid(row=1, column=0, sticky="ew")

        self.decode_img = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(IMAGE_PATH, "upload.png")),
            dark_image=Image.open(os.path.join(IMAGE_PATH, "upload.png")),
            size=(30, 30),
        )
        self.decode_btn = customtkinter.CTkButton(
            self,
            corner_radius=0,
            height=40,
            border_spacing=20,
            text="Decode",
            fg_color="transparent",
            text_color=("grey10", "grey90"),
            hover_color=("grey70", "grey30"),
            image=self.decode_img,
            anchor="w",
            command=self.decode_btn_event,
        )
        self.decode_btn.grid(row=2, column=0, sticky="ew")

        self.compare_img = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(IMAGE_PATH, "compare.png")),
            dark_image=Image.open(os.path.join(IMAGE_PATH, "compare.png")),
            size=(30, 30),
        )
        self.compare_btn = customtkinter.CTkButton(
            self,
            corner_radius=0,
            height=40,
            border_spacing=20,
            text="Compare Images",
            fg_color="transparent",
            text_color=("grey10", "grey90"),
            hover_color=("grey70", "grey30"),
            image=self.compare_img,
            anchor="w",
            command=self.compare_btn_event,
        )
        self.compare_btn.grid(row=3, column=0, sticky="ew")

    def select_frame_by_name(self, name):
        self.encode_btn.configure(
            fg_color=("grey75", "grey25") if name == "encode" else "transparent"
        )
        self.decode_btn.configure(
            fg_color=("grey75", "grey25") if name == "decode" else "transparent"
        )
        self.compare_btn.configure(
            fg_color=("grey75", "grey25") if name == "compare" else "transparent"
        )

    def encode_btn_event(self):
        self.select_frame_by_name("encode")
        self.on_encode_command()

    def decode_btn_event(self):
        self.select_frame_by_name("decode")
        self.on_decode_command()

    def compare_btn_event(self):
        self.select_frame_by_name("compare")
        self.on_compare_command()
