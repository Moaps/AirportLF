import networkx as nx
from queue import PriorityQueue
import tkinter as tk
from tkinter import messagebox


class Buscas:
    def __init__(self, grafo):
        self.grafo = grafo

    def busca_uniforme(self, origem, destino):
        visited = set()
        queue = PriorityQueue()
        queue.put((0, [origem]))

        while not queue.empty():
            (cost, path) = queue.get()
            node = path[-1]

            if node in visited:
                continue

            visited.add(node)

            if node == destino:
                return path

            for next_node, data in self.grafo[node].items():
                if next_node not in visited:
                    total_cost = cost + data['weight']
                    queue.put((total_cost, path + [next_node]))

        return None

    def greedy(self, origem, destino, heuristic):
        visited = set()
        queue = PriorityQueue()
        queue.put((heuristic[origem], [origem]))

        while not queue.empty():
            (_, path) = queue.get()
            node = path[-1]

            if node in visited:
                continue

            visited.add(node)

            if node == destino:
                return path

            for next_node, data in self.grafo[node].items():
                if next_node not in visited:
                    estimated_cost = heuristic[next_node]
                    queue.put((estimated_cost, path + [next_node]))

        return None

    def a_star(self, origem, destino, heuristic):
        visited = set()
        queue = PriorityQueue()
        queue.put((0 + heuristic[origem], [origem], 0))

        while not queue.empty():
            (_, path, cost) = queue.get()
            node = path[-1]

            if node in visited:
                continue

            visited.add(node)

            if node == destino:
                return path

            for next_node, data in self.grafo[node].items():
                if next_node not in visited:
                    total_cost = cost + data['weight']
                    estimated_cost = total_cost + heuristic[next_node]
                    queue.put((estimated_cost, path + [next_node], total_cost))

        return None

    def iterative_deepening_a_star(self, origem, destino, heuristic):
        limit = heuristic[origem]

        while True:
            result = self._ida_star_recursive(origem, destino, [origem], 0, limit, heuristic)
            if result == "found":
                return self.path
            if result == float('inf'):
                return None
            limit = result

    def _ida_star_recursive(self, node, destino, path, cost, limit, heuristic):
        f = cost + heuristic[node]

        if f > limit:
            return f
        if node == destino:
            self.path = path
            return "found"

        min_cost = float('inf')
        for next_node, data in self.grafo[node].items():
            if next_node not in path:
                total_cost = cost + data['weight']
                temp = self._ida_star_recursive(next_node, destino, path + [next_node], total_cost, limit, heuristic)
                if temp == "found":
                    return "found"
                if temp < min_cost:
                    min_cost = temp
        return min_cost
