import customtkinter

from src.widgets.image_preview import ImagePreview

class Encode(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # self.title = customtkinter.CTkLabel(self, text="Encode", font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.title.grid(row=0, column=0, padx=20, pady=10)
        self.image_preview = ImagePreview(self)
        self.image_preview.grid(row=0, column=0, sticky="nsew")

        self.action_frame = customtkinter.CTkFrame(self, width=300, fg_color='transparent')
        self.action_frame.grid(row=0, column=1, sticky="nsew")