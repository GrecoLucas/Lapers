from pathlib import Path
import csv
from typing import Dict, List, Tuple, Optional
from .node import Node

class Graph:
    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        # adjacency[u] = list of (v, weight)
        self.adjacency: Dict[int, List[Tuple[int, float]]] = {}

    def add_node(self, node: Node) -> None:
        """Adiciona/atualiza um nó no grafo."""
        self.nodes[node.id] = node
        if node.id not in self.adjacency:
            self.adjacency[node.id] = []

    def has_node(self, node_id: int) -> bool:
        return node_id in self.nodes

    def add_edge(
        self,
        from_id: int,
        to_id: int,
        weight: float = 1.0,
        bidirectional: bool = True,
    ) -> None:
        """
        Adiciona uma aresta. Se os nós não existirem, lança KeyError.
        Por defeito adiciona uma aresta bidirecional.
        """
        if from_id not in self.nodes or to_id not in self.nodes:
            raise KeyError("Both nodes must exist in the graph before adding an edge.")
        self.adjacency.setdefault(from_id, [])
        self.adjacency[from_id].append((to_id, float(weight)))
        if bidirectional:
            self.adjacency.setdefault(to_id, [])
            self.adjacency[to_id].append((from_id, float(weight)))

    def remove_edge(self, from_id: int, to_id: int, bidirectional: bool = True) -> None:
        """Remove aresta(s) entre from_id e to_id se existirem."""
        if from_id in self.adjacency:
            self.adjacency[from_id] = [
                (v, w) for (v, w) in self.adjacency[from_id] if v != to_id
            ]
        if bidirectional and to_id in self.adjacency:
            self.adjacency[to_id] = [
                (v, w) for (v, w) in self.adjacency[to_id] if v != from_id
            ]

    def remove_node(self, node_id: int) -> None:
        """Remove nó e todas as arestas entrantes/saientes relacionadas."""
        if node_id in self.adjacency:
            del self.adjacency[node_id]
        # remover arestas que apontam para node_id
        for u in list(self.adjacency.keys()):
            self.adjacency[u] = [(v, w) for (v, w) in self.adjacency[u] if v != node_id]
        if node_id in self.nodes:
            del self.nodes[node_id]

    def get_neighbors(self, node_id: int) -> List[Tuple[int, float]]:
        """Retorna lista de (vizinho_id, peso)."""
        return list(self.adjacency.get(node_id, []))

    def nodes_count(self) -> int:
        return len(self.nodes)

    def edges_count(self) -> int:
        return sum(len(neigh) for neigh in self.adjacency.values())

    def to_dict(self) -> dict:
        """Serializa o grafo em dicionário simples."""
        return {
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "adjacency": {nid: list(neigh) for nid, neigh in self.adjacency.items()},
        }