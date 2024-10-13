import customtkinter

class Decode(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, corner_radius=0)
        self.grid_columnconfigure(0, weight=1)

        self.title = customtkinter.CTkLabel(self, text="Decode", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=10)