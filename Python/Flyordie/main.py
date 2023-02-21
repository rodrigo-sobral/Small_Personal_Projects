import tkinter as tk
from PIL import Image, ImageTk
from requests import get
from io import BytesIO
from utils import add_player_input_field
    
class SampleApp(tk.Tk):
    ICON_URL = "https://www.flyordie.com/favicon.ico"
    SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.custom_window()
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (MainMenu, PlayersData, ResultSimulator):
            self.frames[frame.__name__] = frame(parent=container, controller=self)
            self.frames[frame.__name__].grid(row=0, column=0, sticky=tk.NSEW)
        
        self.show_frame("MainMenu")

    def custom_window(self) -> None:
        favicon = get(self.ICON_URL).content
        self.title("FlyorDie - Fernando Sobral")
        self.geometry(f"{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")
        self.iconphoto(True, ImageTk.PhotoImage(Image.open(BytesIO(favicon))))

    def show_frame(self, page_name: str) -> None:
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    NORMAL_FONT = ("Arial", 12)

    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Menu Principal", font=("Arial", 24))
        label.pack(side=tk.TOP, fill=tk.X, pady=10)

        button_players = tk.Button(self, text="Dados Jogadores", font=self.NORMAL_FONT, command=lambda: controller.show_frame("PlayersData"))
        button_players.pack(pady=10)
        
        button_results = tk.Button(self, text="Simulador de Resultados", font=self.NORMAL_FONT, command=lambda: controller.show_frame("ResultSimulator"))
        button_results.pack(pady=10)
        
        button_exit = tk.Button(self, text="Sair", bg="darkred", fg="white", font=self.NORMAL_FONT, command=self.quit)
        button_exit.pack(side=tk.BOTTOM, pady=10)


class PlayersData(tk.Frame):
    NORMAL_FONT = ("Arial", 12)

    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Dados dos Jogadores", font=("Arial", 24), pady=10)
        label.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        add_player_input_field(self)
        
        button_plus = tk.Button(self, text="+", font=self.NORMAL_FONT, command=lambda: add_player_input_field(self))
        button_plus.pack(side=tk.BOTTOM, pady=10)
        
        button_back = tk.Button(self, text="Voltar", font=self.NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, pady=10)



class ResultSimulator(tk.Frame):
    NORMAL_FONT = ("Arial", 12)

    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Simulador de Resultados", font=("Arial", 24), pady=10)
        label.pack(side=tk.TOP, padx=10, pady=5)
        
        input_player1 = add_player_input_field(self)
        vs = tk.Label(self, text="VS")
        vs.pack(pady=2)
        input_player2 = add_player_input_field(self)
        
        generate_button = tk.Button(self, text="Gerar Resultado", bg="green", fg="white", font=self.NORMAL_FONT, command=lambda: self.generate_result())
        generate_button.pack(side=tk.TOP, padx=10, pady=5)
        
        button_back = tk.Button(self, text="Voltar", font=self.NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, padx=10, pady=5)


    def generate_result(self) -> None:
        pass


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()