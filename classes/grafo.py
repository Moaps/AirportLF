import networkx as nx
import random

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

rotas = [
    ("GRU (São Paulo)", "BOG (Bogotá)"),
    ("BOG (Bogotá)", "MGA (Manágua)"),
    ("MGA (Manágua)", "MEX (Cidade do México)"),
    ("MEX (Cidade do México)", "JFK (Nova York)"),
    ("MEX (Cidade do México)", "MIA (Miami)"),
    ("MEX (Cidade do México)", "LAX (Los Angeles)"),
    ("GRU (São Paulo)", "CDG (Paris)"),
    ("GRU (São Paulo)", "LHR (Londres)"),
    ("GRU (São Paulo)", "FRA (Frankfurt)"),
    ("CDG (Paris)", "JFK (Nova York)"),
    ("LHR (Londres)", "JFK (Nova York)"),
    ("FRA (Frankfurt)", "JFK (Nova York)"),
]
class Grafo:
    def __init__(self):
        self.grafo = nx.DiGraph()

    def adicionar_vertice(self, vertice):
        self.grafo.add_node(vertice)

    def adicionar_aresta(self, origem, destino):
        self.grafo.add_edge(origem, destino)
        self.grafo.add_edge(destino, origem)

    def remover_vertice(self, vertice):
        self.grafo.remove_node(vertice)

    def remover_aresta(self, origem, destino):
        self.grafo.remove_edge(origem, destino)
        self.grafo.remove_edge(destino, origem)

    def obter_vizinhos(self, vertice):
        return self.grafo.neighbors(vertice)

    def obter_vertices(self):
        return self.grafo.nodes()

    def obter_arestas(self):
        return self.grafo.edges()

    def obter_grafo(self):
        return self.grafo

    def criar_grafo_fixo(self):
        self.grafo = nx.Graph()
        for aeroporto in aeroportos:
            self.grafo.add_node(aeroporto)
        for i, rota in enumerate(rotas):
            self.grafo.add_edge(rota[0], rota[1], weight=i + 1)  # Peso fixo, mas diferente para cada rota
            self.grafo.add_edge(rota[1], rota[0], weight=i + 1)  # Peso fixo, mas diferente para a rota inversa
        return self.grafo

    def criar_grafo_dinamico(self):
        self.grafo = nx.Graph()
        aeroportos_selecionados = random.sample(aeroportos, random.randint(4, len(aeroportos)))
        for aeroporto in aeroportos_selecionados:
            self.grafo.add_node(aeroporto)
        for i in range(len(aeroportos_selecionados)):
            for j in range(i + 1, len(aeroportos_selecionados)):
                if random.random() < 0.5:  # 50% chance to add an edge
                    self.grafo.add_edge(aeroportos_selecionados[i], aeroportos_selecionados[j], weight=random.randint(1, 10))
                    self.grafo.add_edge(aeroportos_selecionados[j], aeroportos_selecionados[i],
                                   weight=random.randint(1, 10))  # Adiciona a rota inversa
        return self.grafo

    def adicionar_obstaculo(grafo, origem, destino):
        if grafo.has_edge(origem, destino):
            grafo.remove_edge(origem, destino)
        if grafo.has_edge(destino, origem):  # Se o grafo for não direcionado
            grafo.remove_edge(destino, origem)