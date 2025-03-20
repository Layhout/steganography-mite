from tkinter import messagebox

import customtkinter
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from src.widgets.image_preview import ImagePreview
from src.windows.compare_pixel import ComparePixelWindow


class Compare(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.border_width = 2
        self.fig = None
        self.cid = None
        self.compare_pixel_window = None

        self.image_preview_1 = ImagePreview(self, lable_text="Select original image.")
        self.image_preview_1.grid(row=0, column=0, sticky="nsew")
        self.image_preview_1.grid_propagate(0)

        self.separator = customtkinter.CTkFrame(
            self,
            width=self.border_width,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.separator.grid(row=0, column=1, sticky="nsew")
        self.separator.grid_propagate(0)

        self.image_preview_2 = ImagePreview(self, lable_text="Select encoded image.")
        self.image_preview_2.grid(row=0, column=2, sticky="nsew")
        self.image_preview_2.grid_propagate(0)

        self.border_frame = customtkinter.CTkFrame(
            self,
            height=self.border_width,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.border_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.border_frame.grid_propagate(0)

        self.action_frame = customtkinter.CTkFrame(
            self,
            height=50,
            corner_radius=0,
        )
        self.action_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.action_frame.grid_columnconfigure(0, weight=1)
        self.action_frame.grid_rowconfigure(0, weight=1)
        self.action_frame.grid_propagate(0)

        self.compare_button = customtkinter.CTkButton(
            self.action_frame,
            text="Compare",
            command=self.ask_for_pixel,
        )
        self.compare_button.grid(row=0, column=0)

    def compare_images_event(self):
        if self.image_preview_1.image is None or self.image_preview_2.image is None:
            messagebox.showerror("Error", "Please make sure both images are selected.")
            return

        try:
            self.fig, axs = plt.subplots(
                1, 2, figsize=(15, 5), sharex=True, sharey=True
            )

            axs[0].imshow(np.asarray(self.image_preview_1.image))
            axs[1].imshow(np.asarray(self.image_preview_2.image))

            for ax in axs:
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            self.cid = self.fig.canvas.mpl_connect(
                "button_press_event", self.on_click_fig
            )
            self.fig.canvas.mpl_connect("close_event", self.on_close_fig)

            plt.tight_layout()
            plt.show()
        except Exception:
            print(Exception)

    def on_click_fig(self, event):
        pixels_image_1 = self.image_preview_1.image.load()
        pixels_image_2 = self.image_preview_2.image.load()

        if event.button == 3:
            self.ask_for_pixel()

        if event.dblclick:
            x = round(event.xdata)
            y = round(event.ydata)

            self.open_compare_pixel_window(
                pixels_image_1[x, y],
                pixels_image_2[x, y],
                x,
                y,
            )

    def on_close_fig(self, event):
        if self.cid is None or self.fig is None:
            return

        self.fig.canvas.mpl_disconnect(self.cid)
        self.cid = None
        self.fig = None

    def ask_for_pixel(self):
        pixels_image_1 = self.image_preview_1.image.load()
        pixels_image_2 = self.image_preview_2.image.load()

        pixel_string = customtkinter.CTkInputDialog(
            text="Input pixel at 'x, y'", title="Inspect Pixel"
        ).get_input()

        if pixel_string == "" or pixel_string is None:
            return

        xString, yString = pixel_string.split(",")

        try:
            xInt = int(xString)
            yInt = int(yString)

            self.open_compare_pixel_window(
                pixels_image_1[xInt, yInt],
                pixels_image_2[xInt, yInt],
                xInt,
                yInt,
            )

        except Exception:
            messagebox.showerror("Error", "Invalid pixel string format.")

    def open_compare_pixel_window(self, pixel_1, pixel_2, x, y):
        if (
            self.compare_pixel_window is None
            or not self.compare_pixel_window.winfo_exists()
        ):
            self.compare_pixel_window = ComparePixelWindow(self, pixel_1, pixel_2, x, y)
        else:
            self.compare_pixel_window.focus()
