import customtkinter

from src.widgets.decode import Decode
from src.widgets.encode import Encode
from src.widgets.navigation import Navigation
from src.widgets.compare import Compare

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Steganography")
        self.geometry("1280x720")
        self.resizable(False, False)

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create sidebar frame
        self.navigation = Navigation(
            self,
            on_encode_command=lambda: self.open_frame("encode"),
            on_decode_command=lambda: self.open_frame("decode"),
            on_compare_command=lambda: self.open_frame("compare"),
        )

        # Create frames
        self.encode_frame = Encode(self)
        self.decode_frame = Decode(self)
        self.compare_frame = Compare(self)

        # Open default frame
        self.navigation.encode_btn_event()

    def open_frame(self, frame):
        if frame == "encode":
            self.encode_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.encode_frame.grid_forget()
        if frame == "decode":
            self.decode_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.decode_frame.grid_forget()
        if frame == "compare":
            self.compare_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.compare_frame.grid_forget()
