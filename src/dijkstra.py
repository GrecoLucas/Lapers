"""
Módulo contendo implementação do algoritmo de Dijkstra e funções relacionadas
para cálculo de caminhos mais curtos em grafos.
"""

import heapq
from typing import Dict, List, Tuple, Optional
from graph import Graph


def dijkstra(graph: Graph, start_node: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Implementa o algoritmo de Dijkstra para encontrar o caminho mais curto
    de um nó inicial para todos os outros nós.
    
    Args:
        graph: O grafo a ser percorrido
        start_node: O nó inicial
    
    Returns:
        Tupla contendo:
        - distances: Dicionário {node_id: distância_mínima_do_start}
        - predecessors: Dicionário {node_id: nó_anterior_no_caminho}
    """
    # Inicializa distâncias com infinito para todos os nós
    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_node] = 0
    
    # Inicializa predecessores
    predecessors = {node_id: None for node_id in graph.nodes}
    
    # Fila de prioridade: (distância, node_id)
    priority_queue = [(0, start_node)]
    
    # Conjunto de nós visitados
    visited = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Se já visitamos este nó, pula
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # Se a distância atual é maior que a registrada, pula
        if current_distance > distances[current_node]:
            continue
        
        # Explora os vizinhos
        neighbors = graph.get_neighbors(current_node)
        for neighbor_id, edge_weight in neighbors:
            distance = current_distance + edge_weight
            
            # Se encontramos um caminho mais curto, atualiza
            if distance < distances[neighbor_id]:
                distances[neighbor_id] = distance
                predecessors[neighbor_id] = current_node
                heapq.heappush(priority_queue, (distance, neighbor_id))
    
    return distances, predecessors


def get_shortest_path(predecessors: Dict[int, Optional[int]], start_node: int, end_node: int) -> List[int]:
    """
    Reconstrói o caminho mais curto usando o dicionário de predecessores.
    
    Args:
        predecessors: Dicionário de predecessores do Dijkstra
        start_node: Nó inicial
        end_node: Nó final
    
    Returns:
        Lista de nós representando o caminho de start_node até end_node
    """
    path = []
    current = end_node
    
    # Se não há caminho até o nó final
    if predecessors[current] is None and current != start_node:
        return []
    
    # Reconstrói o caminho de trás para frente
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    # Inverte para obter o caminho do início ao fim
    path.reverse()
    
    return path


def all_pairs_shortest_paths(graph: Graph) -> Dict[Tuple[int, int], Tuple[float, List[int]]]:
    """
    Calcula o caminho mais curto entre todos os pares de nós usando Dijkstra.
    
    Args:
        graph: O grafo a ser analisado
    
    Returns:
        Dicionário {(origem, destino): (distância, caminho)}
        onde caminho é uma lista de nós
    """
    all_paths = {}
    
    # Para cada nó como origem
    for start_node in graph.nodes:
        distances, predecessors = dijkstra(graph, start_node)
        
        # Para cada nó como destino
        for end_node in graph.nodes:
            if start_node == end_node:
                all_paths[(start_node, end_node)] = (0, [start_node])
            else:
                distance = distances[end_node]
                path = get_shortest_path(predecessors, start_node, end_node)
                all_paths[(start_node, end_node)] = (distance, path)
    
    return all_paths


def print_shortest_paths(graph: Graph, all_paths: Dict[Tuple[int, int], Tuple[float, List[int]]]):
    """
    Imprime de forma formatada todos os caminhos mais curtos.
    
    Args:
        graph: O grafo (para acessar nomes dos nós)
        all_paths: Resultado de all_pairs_shortest_paths
    """
    print("\n" + "="*80)
    print("CAMINHOS MAIS CURTOS ENTRE TODOS OS PARES DE NÓS (Dijkstra)")
    print("="*80)
    
    # Agrupa por nó de origem
    origins = sorted(set(origem for origem, _ in all_paths.keys()))
    
    for origin in origins:
        origin_node = graph.nodes[origin]
        print(f"\nOrigem: {origin} - {origin_node.nome} ({origin_node.tipo})")
        print("-" * 80)
        
        for destination in sorted(graph.nodes.keys()):
            if origin == destination:
                continue
            
            distance, path = all_paths[(origin, destination)]
            dest_node = graph.nodes[destination]
            
            if distance == float('inf'):
                print(f"  → {destination} ({dest_node.nome}): SEM CAMINHO")
            else:
                # Formata o caminho com nomes
                path_names = []
                for node_id in path:
                    node = graph.nodes[node_id]
                    path_names.append(f"{node_id}({node.nome})")
                
                path_str = " → ".join(path_names)
                print(f"  → {destination} ({dest_node.nome}): distância={distance:.2f}, caminho: {path_str}")
    
    print("="*80 + "\n")


def print_distance_matrix(graph: Graph, all_paths: Dict[Tuple[int, int], Tuple[float, List[int]]]):
    """
    Imprime uma matriz de distâncias entre todos os nós.
    
    Args:
        graph: O grafo
        all_paths: Resultado de all_pairs_shortest_paths
    """
    nodes = sorted(graph.nodes.keys())
    
    print("\n" + "="*80)
    print("MATRIZ DE DISTÂNCIAS (tempo de transporte)")
    print("="*80)
    
    # Cabeçalho
    header = "    "
    for node_id in nodes:
        header += f"{node_id:>8}"
    print(header)
    print("-" * 80)
    
    # Linhas da matriz
    for origin in nodes:
        row = f"{origin:>3} "
        for destination in nodes:
            distance, _ = all_paths[(origin, destination)]
            if distance == float('inf'):
                row += f"{'∞':>8}"
            else:
                row += f"{distance:>8.2f}"
        print(row)
    
    print("="*80 + "\n")
