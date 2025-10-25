from pathlib import Path
from node import Node
from graph import Graph
import csv

# Make dataset paths relative to repository root (two levels up from this file's folder)
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_NODES = BASE_DIR / "datasets" / "easy" / "1" / "pontos.csv"
PATH_EDGES = BASE_DIR / "datasets" / "easy" / "1" / "ruas.csv"
PATH_INITIAL = BASE_DIR / "datasets" / "easy" / "1" / "dados_iniciais.csv"

g = Graph()

def load_nodes(path):
    with open(path, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            nid = int(row.get('id') or row.get('Id') or row.get('ID') or row.get('node') )
            tipo = row.get('tipo','')
            nome = row.get('nome','')
            prioridade = int(row['prioridade']) if row.get('prioridade') else None
            tempo = float(row['tempo_cuidados_minimos']) if row.get('tempo_cuidados_minimos') else None
            # determina is_hospital a partir da coluna se existir, caso contrário deduz pelo tipo
            is_h_col = row.get('is_hospital', '')
            is_h = False
            try:
                if isinstance(is_h_col, str) and is_h_col.strip() != '':
                    is_h = is_h_col.lower().strip() in ('1', 'true', 'sim', 'yes')
            except Exception:
                is_h = False
            # se não houver coluna explícita, marque como hospital quando tipo == 'hospital'
            if not is_h and isinstance(tipo, str) and tipo.strip().lower() == 'hospital':
                is_h = True
            n = Node(id=nid, tipo=tipo, nome=nome, prioridade=prioridade, tempo_cuidados_minimos=tempo, is_hospital=is_h)
            g.add_node(n)

def load_edges(path):
    with open(path, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            # suporte a diferentes nomes de coluna encontrados nos datasets
            a_raw = row.get('from') or row.get('a') or row.get('u') or row.get('ponto_origem') or row.get('origem') or row.get('source')
            b_raw = row.get('to') or row.get('b') or row.get('v') or row.get('ponto_destino') or row.get('destino') or row.get('target')
            w_raw = row.get('weight') or row.get('peso') or row.get('cost') or row.get('tempo_transporte') or row.get('time')

            if a_raw is None or b_raw is None:
                # pula linhas malformadas
                print(f"Ignorando aresta com colunas ausentes: {row}")
                continue

            try:
                a = int(a_raw)
                b = int(b_raw)
            except ValueError:
                print(f"Ignorando aresta com ids inválidos: {row}")
                continue

            try:
                w = float(w_raw) if w_raw not in (None, '') else 1.0
            except ValueError:
                w = 1.0

            g.add_edge(a, b, w, bidirectional=True)

def print_graph(graph: Graph):
    # print nodes
    try:
        nodes = getattr(graph, "nodes")
        print(f"Nós ({len(nodes)}):")
        for nid, n in nodes.items():
            tipo = getattr(n, "tipo", "")
            nome = getattr(n, "nome", "")
            prioridade = getattr(n, "prioridade", None)
            is_h = getattr(n, "is_hospital", None)
            print(f"  {nid}: tipo={tipo} nome={nome} prioridade={prioridade} is_hospital={is_h}")
    except Exception as e:
        print("Não foi possível listar nós:", e)

    # print edges - tenta várias representações possíveis
    if hasattr(graph, "edges") and getattr(graph, "edges"):
        edges = getattr(graph, "edges")
        print(f"\nArestas ({len(edges)}):")
        for e in edges:
            print(f"  {e}")
    elif hasattr(graph, "adj") and getattr(graph, "adj"):
        adj = getattr(graph, "adj")
        print(f"\nAdjacência ({len(adj)} entradas):")
        for u, nbrs in adj.items():
            print(f"  {u} -> {nbrs}")
    elif hasattr(graph, "adjacency") and getattr(graph, "adjacency"):
        adj = getattr(graph, "adjacency")
        print(f"\nAdjacência ({len(adj)} entradas):")
        for u, nbrs in adj.items():
            print(f"  {u} -> {nbrs}")
    else:
        # tenta derivar arestas a partir de métodos/atributos dos nós
        printed = False
        nodes = getattr(graph, "nodes", {})
        for nid, n in nodes.items():
            if hasattr(n, "neighbors"):
                printed = True
                nbrs = getattr(n, "neighbors")
                print(f"  {nid} -> {nbrs}")
        if not printed:
            print("\nNenhuma representação de arestas encontrada no objeto Graph.")

def main():
    load_nodes(PATH_NODES)
    load_edges(PATH_EDGES)
    print_graph(g)

if __name__ == "__main__":
    main()