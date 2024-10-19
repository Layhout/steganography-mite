import os
from tkinter import Canvas, filedialog, messagebox

import customtkinter
from PIL import Image, ImageTk

from src.constants import IMAGE_PATH, VALID_IMAGE_FILE_TYPE


class ImagePreview(customtkinter.CTkFrame):
    def __init__(self, parent, valid_file_type: object = VALID_IMAGE_FILE_TYPE):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.image_placeholder = ImagePlaceholder(self, self.set_image)
        self.image_placeholder.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.valid_file_type = valid_file_type

        self.image = None

    def set_image(self):
        path = filedialog.askopenfile(
            filetypes=[(k, v) for k, v in self.valid_file_type.items()]
        )
        if path is None:
            return
        self.main_image_file_path = path.name
        is_valid_file_type = any(
            self.main_image_file_path.endswith(t)
            for t in list(self.valid_file_type.values())
        )
        if not is_valid_file_type:
            return
        file = open(self.main_image_file_path, "rb")
        image = Image.open(file, "r")
        if image == "P":
            messagebox.showerror(
                "Invalid Image", "Color channel of the image is not supported."
            )
            return
        self.main_image_filename = os.path.basename(self.main_image_file_path)
        self.image_placeholder.grid_forget()
        self.image = image
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_display = ImageDisplay(self, self.resize_image)
        self.image_display.grid(row=0, column=0, sticky="nsew")
        self.image_preview_footer = ImagePreviewFooter(
            self, self.main_image_filename, self.set_image
        )
        self.image_preview_footer.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def resize_image(self, event):
        canvas_ratio = event.width / event.height

        if canvas_ratio > self.image_ratio:
            image_height = event.height
            image_width = image_height * self.image_ratio
        else:
            image_width = event.width
            image_height = image_width / self.image_ratio

        self.image_display.delete("all")
        resized_image = self.image.resize((int(image_width), int(image_height)))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_display.create_image(
            event.width / 2, event.height / 2, image=self.image_tk
        )

    def reset_image(self):
        self.image = None
        self.image_display.grid_forget()
        self.image_preview_footer.grid_forget()
        self.image_placeholder.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


class ImagePlaceholder(customtkinter.CTkFrame):
    def __init__(self, parent, import_image_command):
        super().__init__(
            master=parent,
            border_width=2,
            border_color=("grey75", "grey25"),
            fg_color="transparent",
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.import_image_command = import_image_command

        self.image_holder = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(IMAGE_PATH, "image_holder.png")),
            dark_image=Image.open(os.path.join(IMAGE_PATH, "image_holder.png")),
            size=(100, 100),
        )
        self.image = customtkinter.CTkLabel(self, image=self.image_holder, text="")
        self.image.grid(row=1, column=0)
        self.import_label = customtkinter.CTkLabel(
            self,
            text="Select an main image.",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.import_label.grid(row=2, column=0, pady=10)
        self.import_button = customtkinter.CTkButton(
            self, text="Import Image", command=self.import_image_command
        )
        self.import_button.grid(row=3, column=0)


class ImageDisplay(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(
            master=parent,
            background="#282828",
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.bind("<Configure>", resize_image)


class ImagePreviewFooter(customtkinter.CTkFrame):
    def __init__(self, parent, filename, import_image_command):
        super().__init__(master=parent, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self.filename = filename
        self.import_image_command = import_image_command

        self.imported_label = customtkinter.CTkLabel(
            self, text=self.filename, anchor="w"
        )
        self.imported_label.grid(row=0, column=0, sticky="we")
        self.import_button = customtkinter.CTkButton(
            self, text="Change Image", command=self.import_image_command
        )
        self.import_button.grid(row=0, column=1)
