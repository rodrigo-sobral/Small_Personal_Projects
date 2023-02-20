import tkinter as tk


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (MainMenu, PlayersData, ResultSimulator):
            self.frames[frame.__name__] = frame(parent=container, controller=self)
            self.frames[frame.__name__].grid(row=0, column=0, sticky=tk.NSEW)
        
        self.show_frame("MainMenu")

    def show_frame(self, page_name: str) -> None:
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page")
        label.pack(side=tk.TOP, fill=tk.X, pady=10)

        button1 = tk.Button(self, text="Go to Page One", command=lambda: controller.show_frame("PlayersData"))
        button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("ResultSimulator"))
        button1.pack()
        button2.pack()


class PlayersData(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1")
        label.pack(side=tk.TOP, fill=tk.X, pady=10)
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("MainMenu"))
        button.pack()


class ResultSimulator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2")
        label.pack(side=tk.TOP, fill=tk.X, pady=10)
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("MainMenu"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()