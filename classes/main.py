import customtkinter
from customtkinter import CTk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import grafo as gr
import tkinter as tk
from tkinter import messagebox
import buscas

customtkinter.set_appearance_mode(
    "System"
)
customtkinter.set_default_color_theme(
    "green"
)

# Criação do grafo
rotaFinal = nx.DiGraph()
grafoInicial = nx.DiGraph()
rotasBloqueadas = None

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
        self.geometry(self.CentralizarJanela(1100, 580, self._get_window_scaling()))

        # Configurando o layout de grade
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

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
            values=["System", "Light", "Dark"],
            command=self.trocar_tema,
        )
        self.sidebar_Tema.grid(row=20, column=0, padx=20, pady=(10, 10))

        # Cria Janelas
        self.frameTab = customtkinter.CTkFrame(self, width=900, corner_radius=0, fg_color="transparent")
        self.frameTab.grid(row=0, column=1, sticky="nsew")
        self.frameTab.grid_rowconfigure(0, weight=1)
        self.frameTab.grid_columnconfigure(0, weight=1)
        self.tabGrafos = customtkinter.CTkTabview(
            self.frameTab
        )
        self.tabGrafos.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.tabGrafos.add("Grafo")

        # Janela - Plotagem do Grafo Inicial
        self.figuraGrafo = plt.figure()
        self.canvasGrafo = FigureCanvasTkAgg(self.figuraGrafo, master=self.tabGrafos.tab("Grafo"))
        self.canvasGrafo.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def trocar_tema(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def CentralizarJanela(Screen: CTk, width: int, height: int, scale_factor: float = 1.0):
        """Centers the window to the main display/monitor"""
        screen_width = Screen.winfo_screenwidth()
        screen_height = Screen.winfo_screenheight()
        x = int(((screen_width / 2) - (width / 2)) * scale_factor)
        y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
        return f"{width}x{height}+{x}+{y}"

    def grafo_dinamico(self):
        grafo = gr.Grafo.criar_grafo_dinamico(self)
        return grafo

    def grafo_fixo(self):
        grafo = gr.Grafo.criar_grafo_fixo(self)
        return grafo

    def bloquear_rotas(self):
        return gr.Grafo.bloquear_rotas(self, grafoInicial)

    def grafo_selecao(self, valor):
        global grafoInicial, bloqueio

        match valor:
            case 1:
                grafoInicial = self.grafo_dinamico()
                bloqueio = self.bloquear_rotas()
                self.plotagem(grafoInicial)
                self.desbloquear_escolhas()
                self.desbloquear_direcao(grafoInicial)
            case 2:
                grafoInicial = self.grafo_fixo()
                bloqueio = self.bloquear_rotas()
                self.plotagem(grafoInicial)
                self.desbloquear_escolhas()
                self.desbloquear_direcao(grafoInicial)

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
                "Custo Uniforme",
                "Greedy",
                "A*",
                "Aprofundamento Iterativo A*"
            ],
            dynamic_resizing=False,
        )
        self.metodo_escolha.grid(row=9, column=0, padx=20, pady=(0, 7))

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
            command=lambda: self.plotagem(grafoInicial),
        )
        self.limpar_grafo.grid(row=13, column=0, padx=20, pady=3)

    def calculate_heuristic(self, grafo, destino):
        heuristic = {}
        destino_index = aeroportos.index(destino)
        for node in grafo.nodes():
            node_index = aeroportos.index(node)
            heuristic[node] = abs(destino_index - node_index)  # Diferença de índices como heurística simples
        return heuristic

    def sidebar_metodo_escolhido(self):
        origem = self.origem_escolhas.get()
        destino = self.destino_escolhas.get()
        global rotaFinal
        rotaFinal = grafoInicial

        heuristic = self.calculate_heuristic(rotaFinal, destino)

        match self.metodo_escolha.get():
            case "Custo Uniforme":
                resultado = buscas.Buscas(rotaFinal).busca_uniforme(origem, destino)
            case "Greedy":
                resultado = buscas.Buscas(rotaFinal).greedy(origem, destino, heuristic)
            case "A*":
                resultado = buscas.Buscas(rotaFinal).a_star(origem, destino, heuristic)
            case "Aprofundamento Iterativo A*":
                resultado = buscas.Buscas(rotaFinal).iterative_deepening_a_star(origem, destino, heuristic)

        if resultado:
            self.plotagem_com_caminho(rotaFinal, resultado)
        else:
            messagebox.showinfo("Resultado", "Não foi encontrado um caminho.")

        self.desbloquear_limpar()

    def plotagem(self, grafo):
        self.figuraGrafo.clear()
        ax = self.figuraGrafo.add_subplot()
        pos = nx.circular_layout(grafo)  # Utilize um algoritmo de layout Circular
        nx.draw(
            grafo,
            pos,
            with_labels=True,
            node_size=1000,
            node_color="#2cc985",
            font_size=10,
            arrows=False,
            ax=ax,
        )

        # Desenha as rotas bloqueadas em cinza
        nx.draw_networkx_edges(
            grafo,
            pos,
            edgelist=bloqueio,
            edge_color='gray',
            width=2,
            style='dashed'
        )

        edge_labels = nx.get_edge_attributes(grafo, 'weight')
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)
        ax.set_title("Grafo de Rotas de Aeroporto")
        ax.axis("off")
        self.canvasGrafo.draw()

    def plotagem_com_caminho(self, grafo, caminho):
        self.figuraGrafo.clear()  # Limpa o gráfico anterior
        ax = self.figuraGrafo.add_subplot()
        pos = nx.circular_layout(grafo)  # Posicionamento dos nós

        # Desenha o grafo inteiro
        nx.draw(
            grafo,
            pos,
            with_labels=True,
            node_size=1000,
            node_color="#2cc985",
            font_size=10,
            arrows=False,
            ax=ax
        )

        # Desenha o caminho com uma cor diferente
        caminho_edges = list(zip(caminho[:-1], caminho[1:]))
        nx.draw_networkx_edges(
            grafo,
            pos,
            edgelist=caminho_edges,
            edge_color='red',
            width=2,
            arrows=True
        )

        # Desenha as rotas bloqueadas em cinza
        nx.draw_networkx_edges(
            grafo,
            pos,
            edgelist=bloqueio,
            edge_color='gray',
            width=2,
            style='dashed'
        )

        # Etiquetas para os pesos das arestas
        edge_labels = nx.get_edge_attributes(grafo, 'weight')
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)

        ax.set_title("Grafo de Rotas de Aeroporto com Caminho")
        ax.axis("off")
        self.canvasGrafo.draw()  # Atualiza o canvas com o novo gráfico

if __name__ == "__main__":
    app = App()
    app.mainloop()