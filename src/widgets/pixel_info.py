import customtkinter


class PixelInfo(customtkinter.CTkFrame):
    def __init__(self, parent, pixel, name):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        self.r = pixel[0]
        self.g = pixel[1]
        self.b = pixel[2]
        self.hex_color = "#{:02x}{:02x}{:02x}".format(
            self.r,
            self.g,
            self.b,
        )
        self.binary_val = "r: {:08b}\ng: {:08b}\nb: {:08b}".format(
            self.r,
            self.g,
            self.b,
        )

        self.color_rgb_label = customtkinter.CTkLabel(
            self,
            anchor="w",
            text=name,
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.color_rgb_label.grid(row=0, column=0)

        self.color_display = customtkinter.CTkFrame(
            self,
            corner_radius=0,
            width=100,
            height=100,
            fg_color="transparent",
            bg_color=self.hex_color,
        )
        self.color_display.grid(row=1, column=0, pady=(20, 10))

        self.color_rgb_label = customtkinter.CTkLabel(
            self, anchor="w", text=f"RGB: ({self.r}, {self.g}, {self.b})"
        )
        self.color_rgb_label.grid(row=2, column=0)

        self.hex_color_label = customtkinter.CTkLabel(
            self, anchor="w", text=f"HEX: {self.hex_color}"
        )
        self.hex_color_label.grid(row=3, column=0)

        self.binary_val_label = customtkinter.CTkLabel(
            self, anchor="w", text=f"Binary:\n{self.binary_val}"
        )
        self.binary_val_label.grid(row=4, column=0)
