from tkinter import messagebox

import customtkinter

from src.constants import STEGANOGRAPHY_METHODS
from src.steganography import Steganography
from src.widgets.image_preview import ImagePreview


class Decode(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.image_preview = ImagePreview(self, {"PNG": ".png"})
        self.image_preview.grid(row=0, column=0, sticky="nsew")

        self.action_frame = customtkinter.CTkFrame(
            self,
            width=300,
            corner_radius=0,
            border_width=1,
            border_color=("grey75", "grey25"),
        )
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(2, weight=1)
        self.action_frame.grid(row=0, column=1, sticky="nsew")
        self.action_frame.grid_propagate(0)

        self.method_label = customtkinter.CTkLabel(
            self.action_frame,
            text="Method",
            anchor="w",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.method_label.grid(row=0, column=0, padx=20, pady=10, sticky="we")

        self.method_optionmenu = customtkinter.CTkOptionMenu(
            self.action_frame,
            values=STEGANOGRAPHY_METHODS,
            command=self.change_method_event,
        )
        self.method_optionmenu.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="we")

        self.encode_button = customtkinter.CTkButton(
            self.action_frame, text="Decode", command=self.decode_event
        )
        self.encode_button.grid(row=3, column=0, padx=20, pady=10, sticky="we")

    def change_method_event(self, new_method):
        self.ste_method = new_method

    def decode_event(self):
        if self.image_preview.image is None:
            messagebox.showerror("Error", "Please select the main image.")
            return

        secret_token = customtkinter.CTkInputDialog(
            text="Input a secret word", title="Secret Word"
        ).get_input()
        if secret_token == "":
            messagebox.showerror("Error", "Secret word is required.")
            return

        ste = Steganography(self.image_preview.image)
        if self.method_optionmenu.get() == "LSB":
            ste.lsb_decode(secret_token)
