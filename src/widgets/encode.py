import base64
import os
from tkinter import filedialog, messagebox

import customtkinter

from src.constants import (
    VALID_IMAGE_FILE_TYPE,
    ENCODE_DATA_TYPE,
)
from src.utils.steganography import Steganography
from src.widgets.image_preview import ImagePreview


class Encode(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.image_preview = ImagePreview(self)
        self.image_preview.grid(row=0, column=0, sticky="nsew")

        self.action_frame = customtkinter.CTkFrame(
            self,
            width=300,
            corner_radius=0,
            border_width=1,
            border_color=("grey75", "grey25"),
        )
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(7, weight=1)
        self.action_frame.grid(row=0, column=1, sticky="nsew")
        self.action_frame.grid_propagate(0)

        # self.method_label = customtkinter.CTkLabel(
        #     self.action_frame,
        #     text="Method",
        #     anchor="w",
        #     font=customtkinter.CTkFont(size=14, weight="bold"),
        # )
        # self.method_label.grid(row=0, column=0, padx=20, pady=10, sticky="we")

        # self.method_optionmenu = customtkinter.CTkOptionMenu(
        #     self.action_frame,
        #     values=STEGANOGRAPHY_METHODS,
        #     command=self.change_method_event,
        # )
        # self.method_optionmenu.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="we")
        # self.new_method = STEGANOGRAPHY_METHODS[0]

        self.data_type_label = customtkinter.CTkLabel(
            self.action_frame,
            text="Data Type",
            anchor="w",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.data_type_label.grid(row=2, column=0, padx=20, pady=10, sticky="we")

        self.data_type_optionmenu = customtkinter.CTkOptionMenu(
            self.action_frame,
            values=list(ENCODE_DATA_TYPE.values()),
            command=self.change_data_type_event,
        )
        self.data_type_optionmenu.grid(
            row=3, column=0, padx=20, pady=(0, 10), sticky="we"
        )
        self.data_type = ENCODE_DATA_TYPE.get("text")

        self.data_label = customtkinter.CTkLabel(
            self.action_frame,
            text="Data to Encode",
            anchor="w",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        self.data_label.grid(row=4, column=0, padx=20, pady=10, sticky="we")

        self.text_entry = customtkinter.CTkTextbox(
            self.action_frame, border_color=("grey75", "grey25"), border_width=1
        )
        self.text_entry.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="we")

        self.filename = ""
        self.file = None
        self.import_file_button = customtkinter.CTkButton(
            self.action_frame, text="Import File", command=self.import_file_event
        )
        self.filename_label = customtkinter.CTkLabel(
            self.action_frame, text=self.filename, anchor="w"
        )

        self.encode_button = customtkinter.CTkButton(
            self.action_frame, text="Encode", command=self.encode_event
        )
        self.encode_button.grid(row=8, column=0, padx=20, pady=10, sticky="we")

    def change_data_type_event(self, new_type):
        self.data_type = new_type
        if new_type == ENCODE_DATA_TYPE.get("text"):
            self.import_file_button.grid_forget()
            self.filename_label.grid_forget()
            self.text_entry.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="we")
        else:
            self.text_entry.grid_forget()
            self.import_file_button.grid(
                row=5, column=0, padx=20, pady=(0, 10), sticky="we"
            )
            self.filename_label.grid(
                row=6, column=0, padx=20, pady=(0, 20), sticky="we"
            )

    def change_method_event(self, new_method):
        self.ste_method = new_method

    def import_file_event(self):
        path = filedialog.askopenfile(
            filetypes=[(k, v) for k, v in VALID_IMAGE_FILE_TYPE.items()]
        )
        if path is None:
            return
        self.filename = path.name
        self.filename_label.configure(text=os.path.basename(self.filename))
        is_valid_file_type = any(
            self.filename.endswith(t) for t in list(VALID_IMAGE_FILE_TYPE.values())
        )
        if not is_valid_file_type:
            return

    def encode_event(self):
        if self.image_preview.image is None:
            messagebox.showerror("Error", "Please select the main image.")
            return

        secret_data = ""

        if self.data_type == ENCODE_DATA_TYPE.get("text"):
            if self.text_entry.get("1.0", "end-1c") == "":
                messagebox.showerror("Error", "Please enter data to encode.")
                return
            else:
                secret_data = self.text_entry.get("1.0", "end-1c")
        else:
            if self.filename == "":
                messagebox.showerror("Error", "Please select a file to encode.")
                return
            else:
                file = open(self.filename, "rb")
                data = base64.b64encode(file.read())
                secret_data = data.decode()

        if secret_data == "":
            return

        secret_token = customtkinter.CTkInputDialog(
            text="Input a secret word", title="Secret Word"
        ).get_input()
        if secret_token == "":
            messagebox.showerror("Error", "Secret word is required.")
            return

        ste = Steganography(self.image_preview.image)
        # ste_status = ""
        # if self.method_optionmenu.get() == "LSB":
        ste_status = ste.lsb_encode(
            secret_data,
            secret_token,
            self.image_preview.main_image_filename,
            self.data_type,
        )

        if ste_status == "fail":
            return

        self.image_preview.reset_image()
        # self.method_optionmenu.set(STEGANOGRAPHY_METHODS[0])
        # self.change_method_event(STEGANOGRAPHY_METHODS[0])
        self.data_type_optionmenu.set(ENCODE_DATA_TYPE.get("text"))
        self.change_data_type_event(ENCODE_DATA_TYPE.get("text"))
        self.file = None
        self.text_entry.delete(0.0, "end")
