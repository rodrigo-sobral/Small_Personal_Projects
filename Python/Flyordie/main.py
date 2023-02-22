import tkinter as tk
from PIL import Image, ImageTk
from requests import get
from io import BytesIO
from utils import add_player_input_field, NORMAL_FONT, BG_COLOR, TEXT_PROPS, TITLE_PROPS, GREEN_BUTTON_PROPS, LIGHTBLUE_BUTTON_PROPS, DARKRED_BUTTON_PROPS, export_players_data


players_data = {}


class Window(tk.Tk):
    ICON_URL = "https://www.flyordie.com/favicon.ico"
    MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT = 380, 300
    SCREEN_WIDTH, SCREEN_HEIGHT = 480, 580

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
        self.minsize(self.MIN_SCREEN_WIDTH, self.MIN_SCREEN_HEIGHT)

    def show_frame(self, page_name: str) -> None:
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Menu Principal", **TITLE_PROPS)
        label.pack(side=tk.TOP, pady=10)

        button_players = tk.Button(self, text="Dados Jogadores", font=NORMAL_FONT, command=lambda: controller.show_frame("PlayersData"))
        button_players.pack(side=tk.TOP, pady=10)
        
        button_results = tk.Button(self, text="Simulador de Resultados", font=NORMAL_FONT, command=lambda: controller.show_frame("ResultSimulator"))
        button_results.pack(side=tk.TOP, pady=10)
        
        button_exit = tk.Button(self, text="Sair", **DARKRED_BUTTON_PROPS, command=self.quit)
        button_exit.pack(side=tk.BOTTOM, pady=10)


class PlayersData(tk.Frame):
    LIMIT_PLAYERS = 4

    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Dados dos Jogadores", **TITLE_PROPS)
        label.pack(side=tk.TOP, pady=10)
        
        add_player_input_field(self)

        button_back = tk.Button(self, text="Voltar", font=NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, pady=10)
        
        export_button = tk.Button(self, text="Exportar", **LIGHTBLUE_BUTTON_PROPS, command=lambda: export_players_data(players_data))
        export_button.pack(side=tk.BOTTOM, padx=10, pady=5)
        
        button_plus = tk.Button(self, text="+", **GREEN_BUTTON_PROPS, command=lambda: add_player_input_field(self, can_delete=True))
        button_plus.pack(side=tk.BOTTOM, pady=10)
        


class ResultSimulator(tk.Frame):
    def __init__(self, parent: tk.Frame, controller: tk.Tk):
        tk.Frame.__init__(self, parent, bg=BG_COLOR)
        self.controller = controller
        label = tk.Label(self, text="Simulador de Resultados", **TITLE_PROPS)
        label.pack(side=tk.TOP, padx=10, pady=5)
        
        input_player1 = add_player_input_field(self, "Nome do Jogador")
        vs = tk.Label(self, text="VS", **TEXT_PROPS)
        vs.pack()
        input_player2 = add_player_input_field(self, "Nome do Oponente")
        
        generate_button = tk.Button(self, text="Gerar Resultado", **GREEN_BUTTON_PROPS, command=lambda: self.generate_result())
        generate_button.pack(side=tk.TOP, padx=10, pady=5)
        
        button_back = tk.Button(self, text="Voltar", font=NORMAL_FONT, command=lambda: controller.show_frame("MainMenu"))
        button_back.pack(side=tk.BOTTOM, pady=10)


    def generate_result(self) -> None:
        pass


if __name__ == "__main__":
    app = Window()
    app.mainloop()