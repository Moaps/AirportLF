import customtkinter
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import grafo as gr
import buscas as bu

customtkinter.set_appearance_mode(
    "Light"
)
customtkinter.set_default_color_theme(
    "green"
)

# Criação do grafo
rotaFinal = nx.DiGraph()

randomgraph = 0
runCount = 0

# Lista de aeroportos
aeroportos = [
    "GRU (São Paulo)",
    "BOG (Bogotá)",
    "MGA (Manágua)",
    "MEX (Cidade do México)",
    "JFK (Nova York)",
    "MIA (Miami)",
    "LAX (Los Angeles)",
    "CDG (Paris)",
    "LHR (Londres)",
    "FRA (Frankfurt)",
]


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configurando a janela
        self.title("Aeroporto")
        self.geometry(f"{1100}x{580}")

        # Configurando o layout de grade
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        #
        # Criando uma barra lateral
        #

        # Texto - Titulo do App
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=18, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(16, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Rotas ✈",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Texto - Grafo dinâmico
        self.grafo_Label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Gerar grafo dinâmico?", anchor="w", justify="left"
        )
        self.grafo_Label.grid(row=1, column=0, padx=20)

        # Botão - Sim, grafo dinamico
        self.grafo_Botao_Sim = customtkinter.CTkButton(
            self.sidebar_frame,
            command=lambda: self.grafo_selecao(int(1)),
            text="Sim",
        )
        self.grafo_Botao_Sim.grid(row=2, column=0, padx=20, pady=3)

        # Botão - Não, grafo fixo
        self.grafo_Botao_Nao = customtkinter.CTkButton(
            self.sidebar_frame,
            command=lambda: self.grafo_selecao(int(2)),
            text="Não",
        )
        self.grafo_Botao_Nao.grid(row=3, column=0, padx=20, pady=3)

        # Dropdown - Trocar o Tema
        self.sidebar_Tema = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.trocar_tema,
        )
        self.sidebar_Tema.grid(row=20, column=0, padx=20, pady=(10, 10))

        # Janela - Plotagem do Grafo
        self.figure = plt.figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(
            row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

    def trocar_tema(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def grafo_dinamico(self):
        grafo = gr.Grafo.criar_grafo_dinamico(self)
        return grafo

    def grafo_fixo(self):
        grafo = gr.Grafo.criar_grafo_fixo(self)
        return grafo

    def grafo_selecao(self, valor):
        match valor:
            case 1:
                grafo = self.grafo_dinamico()
                self.plotagem(grafo)
                self.desbloquear_escolhas()
                self.desbloquear_direcao(grafo)
            case 2:
                grafo = self.grafo_fixo()
                self.plotagem(grafo)
                self.desbloquear_escolhas()
                self.desbloquear_direcao(grafo)

    def desbloquear_escolhas(self):
        # Título - Escolha de Metodo
        self.metodo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Metodo", anchor="w", justify="left"
        )
        self.metodo_label.grid(row=8, column=0, padx=20)

        # Dropdown - Escolha de Metodo
        self.metodo_escolha = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=[
                "Amplitude",
                "Profundidade",
                "Profundidade Limitada",
                "Aprofundamento",
                "Bidirecional",
            ],
            dynamic_resizing=False,
        )
        self.metodo_escolha.grid(row=9, column=0, padx=20, pady=(0, 7))

        # Título - Escolha de Bloqueio
        self.bloqueio_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Qtd Bloqueio", anchor="w", justify="left"
        )
        self.bloqueio_label.grid(row=10, column=0, padx=20)

        # Dropdown - Escolha de Bloqueio
        self.bloqueio_escolha = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=[
                "0",
                "1",
                "2",
                "3"
            ],
            dynamic_resizing=False,
        )
        self.bloqueio_escolha.grid(row=11, column=0, padx=20, pady=(0, 7))

        # Botão - Rodar Algorítmo
        self.rodar_algoritmo = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Rodar Algorítmo",
            command=lambda: self.sidebar_metodo_escolhido(),
        )
        self.rodar_algoritmo.grid(row=12, column=0, padx=20, pady=3)

    def desbloquear_direcao(self, grafo):
        # Título - Origem
        self.origem_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Origem", anchor="w", justify="left"
        )
        self.origem_label.grid(row=4, column=0, padx=20)

        # Título - Destino
        self.destino_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Destino", anchor="w", justify="left"
        )
        self.destino_label.grid(row=6, column=0, padx=20)

        # Obter os nós do grafo e atualizar o menu suspenso de destino
        nos = list(grafo.nodes())

        # Dropdown - Origem
        self.origem_escolhas = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=nos, dynamic_resizing=False
        )
        self.origem_escolhas.grid(row=5, column=0, padx=20, pady=3)

        # Dropdown - Destino
        self.destino_escolhas = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=nos, dynamic_resizing=False
        )
        self.destino_escolhas.grid(row=7, column=0, padx=20, pady=3)

    def desbloquear_limpar(self):
        # Botão - Limpar
        self.limpar_grafo = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Limpar Grafo",
            command=lambda: self.plotagem(gr.Grafo.obter_grafo(self)),
        )
        self.limpar_grafo.grid(row=13, column=0, padx=20, pady=3)

    def sidebar_metodo_escolhido(self):
        match self.metodo_escolha.get():
            case "Amplitude":
                rota = bu.Buscas.busca_amplitude(gr.Grafo.obter_grafo(), self.origem_escolhas.get(), self.destino_escolhas.get())
                if rota != "ERRO":
                    self.plotagem(rota)
                print("Amplitude")
            case "Profundidade":
                #self.busca_profundidade()
                print("Profundidade")
            case "Profundidade Limitada":
                #self.busca_profundidade_limitada(2)
                print("Amplitude")
            case "Aprofundamento":
                #self.busca_aprofundamento()
                print("Aprofundamento")
            case "Bidirecional":
                #self.busca_bidirecional()
                print("Bidirecional")

        self.desbloquear_limpar()

    def plotagem(self, grafo):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        pos = nx.circular_layout(grafo)  # Utilize um algoritmo de layout Circular
        nx.draw(
            grafo,
            pos,
            with_labels=True,
            node_size=700,
            node_color="#2cc985",
            font_size=10,
            arrows=False,
            ax=ax,
        )
        edge_labels = nx.get_edge_attributes(grafo, 'weight')
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)
        ax.set_title("Grafo de Rotas de Aeroporto")
        ax.axis("off")
        self.canvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()