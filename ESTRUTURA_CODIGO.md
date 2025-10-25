# Estrutura do Código - Algoritmo de Dijkstra

## 📁 Estrutura de Arquivos

```
src/
├── node.py          # Classe Node (representa um ponto/nó)
├── graph.py         # Classe Graph (estrutura do grafo)
├── dijkstra.py      # Algoritmo de Dijkstra e funções auxiliares
└── main.py          # Carregamento de dados e execução principal
```

## 📋 Módulos

### `node.py`
Define a classe `Node` que representa um ponto (hospital ou paciente):
- **Atributos**: id, tipo, nome, prioridade, tempo_cuidados_minimos, is_hospital

### `graph.py`
Define a classe `Graph` que gerencia o grafo:
- **Métodos principais**:
  - `add_node(node)` - Adiciona um nó
  - `add_edge(from_id, to_id, weight, bidirectional)` - Adiciona aresta
  - `get_neighbors(node_id)` - Retorna vizinhos de um nó
  - `has_node(node_id)` - Verifica se nó existe

### `dijkstra.py` ⭐
Implementa o algoritmo de Dijkstra e funções relacionadas:

#### Funções principais:
- **`dijkstra(graph, start_node)`**
  - Calcula caminhos mais curtos de um nó para todos os outros
  - Retorna: (distâncias, predecessores)

- **`get_shortest_path(predecessors, start_node, end_node)`**
  - Reconstrói o caminho a partir dos predecessores
  - Retorna: lista de nós no caminho

- **`all_pairs_shortest_paths(graph)`**
  - Calcula caminhos mais curtos entre TODOS os pares de nós
  - Retorna: dicionário {(origem, destino): (distância, caminho)}

#### Funções de visualização:
- **`print_shortest_paths(graph, all_paths)`**
  - Imprime todos os caminhos formatados

- **`print_distance_matrix(graph, all_paths)`**
  - Imprime matriz de distâncias

### `main.py`
Carrega dados dos CSVs e executa o programa:
- **`load_nodes(path)`** - Carrega pontos do CSV
- **`load_edges(path)`** - Carrega ruas do CSV
- **`print_graph(graph)`** - Visualiza o grafo
- **`main()`** - Função principal

## 🚀 Como Usar

### Executar o programa:
```bash
cd src
python3 main.py
```

### Usar Dijkstra em outro código:
```python
from dijkstra import dijkstra, all_pairs_shortest_paths

# Caminho de um nó específico
distances, predecessors = dijkstra(grafo, nó_inicial)

# Todos os pares
all_paths = all_pairs_shortest_paths(grafo)
distancia, caminho = all_paths[(origem, destino)]
```

## 📊 Saída do Programa

O programa exibe:
1. **Grafo carregado** - Nós e adjacências
2. **Caminhos mais curtos** - Entre todos os pares de nós
3. **Matriz de distâncias** - Tabela visual das distâncias
4. **Exemplo prático** - Caminhos do hospital para cada paciente

## ⚙️ Complexidade do Algoritmo

- **Dijkstra**: O(V log V + E log V) onde V = vértices, E = arestas
- **All pairs**: O(V² log V + VE log V) = executa Dijkstra V vezes

## 📝 Datasets Disponíveis

```
datasets/
├── easy/    (1, 2, 3)    - Grafos pequenos e simples
├── medium/  (4, 5, 6, 7) - Grafos médios
└── hard/    (8, 9, 10)   - Grafos grandes e complexos
```

Para mudar o dataset, edite em `main.py`:
```python
PATH_NODES = BASE_DIR / "datasets" / "medium" / "5" / "pontos.csv"
PATH_EDGES = BASE_DIR / "datasets" / "medium" / "5" / "ruas.csv"
```
