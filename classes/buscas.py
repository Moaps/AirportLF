import networkx as nx
import tkinter
import tkinter.messagebox

class Buscas:
    def __init__(self, grafo):
        self.grafo = grafo

    def busca_amplitude(self, grafo, origem, destino):
        rota = nx.Graph()

        visited = set()  # Conjunto de nós visitados
        queue = [[origem]]  # Fila para a busca em amplitude
        found_path = False

        while queue:  # Enquanto houver nós na fila
            # Retire o primeiro caminho da fila
            path = queue.pop(0)
            # Obtenha o último nó do caminho
            node = path[-1]

            if node == destino:  # Se o último nó for o destino, encontramos o caminho
                rota.add_nodes_from(path)
                for i in range(len(path) - 1):
                    rota.add_edge(path[i], path[i + 1])
                return rota

            if node not in visited:  # Se o nó não foi visitado, visite-o
                neighbors = rota.neighbors(node)
                # Adicione os vizinhos do nó ao caminho e à fila
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                visited.add(node)  # Marque o nó como visitado

        if not found_path:
            tkinter.messagebox.showinfo(
                "Informação", "Não há caminho entre a origem e o destino."
            )
            return "ERRO"