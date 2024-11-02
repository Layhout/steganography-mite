import customtkinter

from src.widgets.pixel_info import PixelInfo


class ComparePixelWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, pixel_1, pixel_2):
        super().__init__(parent)
        self.geometry("500x300")
        self.resizable(False, False)

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(0, weight=1)

        self.pixel_1_info = PixelInfo(self, pixel_1)
        self.pixel_1_info.grid(row=0, column=0, sticky="nsew")

        self.separator = customtkinter.CTkFrame(
            self,
            width=2,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.separator.grid(row=0, column=1, sticky="nsew")
        self.separator.grid_propagate(0)

        self.pixel_2_info = PixelInfo(self, pixel_2)
        self.pixel_2_info.grid(row=0, column=2, sticky="nsew")
