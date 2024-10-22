import customtkinter


class Compare(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
