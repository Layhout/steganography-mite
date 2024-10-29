from tkinter import messagebox

import customtkinter
from matplotlib.ticker import MaxNLocator
import numpy as np
from matplotlib import pyplot as plt

from src.widgets.image_preview import ImagePreview


class Compare(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.border_width = 2

        self.image_preview_1 = ImagePreview(self, lable_text="Select image 1.")
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

        self.image_preview_2 = ImagePreview(self, lable_text="Select image 2.")
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
            command=self.compare_images_event,
        )
        self.compare_button.grid(row=0, column=0)

    def compare_images_event(self):
        if self.image_preview_1.image is None or self.image_preview_2.image is None:
            messagebox.showerror("Error", "Please make sure both images are selected.")
            return

        try:
            plt.ion()

            fig, axs = plt.subplots(1, 2, figsize=(15, 5), sharex=True, sharey=True)

            axs[0].imshow(np.asarray(self.image_preview_1.image))
            axs[1].imshow(np.asarray(self.image_preview_2.image))

            for ax in axs:
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            # cid = fig.canvas.mpl_connect("button_press_event", lambda: print("Pressed"))
            # fig.canvas.mpl_disconnect(cid)

            fig.canvas.mpl_connect("close_event", lambda: print("close_event"))

            plt.tight_layout()
            plt.show()
        except Exception:
            print(Exception)

    def on_click_fig(self, event):
        print("123")
        print(
            "%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f"
            % (
                "double" if event.dblclick else "single",
                event.button,
                event.x,
                event.y,
                event.xdata,
                event.ydata,
            )
        )
