import customtkinter

from src.widgets.pixel_info import PixelInfo


class ComparePixelWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, pixel_1, pixel_2, x, y):
        super().__init__(parent)
        self.geometry("500x350")
        self.resizable(False, False)

        self.columnconfigure((0, 2), weight=1)
        self.rowconfigure(2, weight=1)

        self.pixels = customtkinter.CTkFrame(
            self,
            height=50,
            corner_radius=0,
        )
        self.pixels.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.pixels.grid_propagate(0)
        self.pixels.columnconfigure(0, weight=1)
        self.pixels.rowconfigure(0, weight=1)

        self.pixel_label = customtkinter.CTkLabel(
            self.pixels,
            text=f"Pixels ({x}, {y})",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.pixel_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.separator = customtkinter.CTkFrame(
            self,
            height=2,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.separator.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.separator.grid_propagate(0)

        self.pixel_1_info = PixelInfo(self, pixel_1)
        self.pixel_1_info.grid(row=2, column=0, sticky="nsew")

        self.separator_1 = customtkinter.CTkFrame(
            self,
            width=2,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.separator_1.grid(row=2, column=1, sticky="nsew")
        self.separator_1.grid_propagate(0)

        self.pixel_2_info = PixelInfo(self, pixel_2)
        self.pixel_2_info.grid(row=2, column=2, sticky="nsew")
