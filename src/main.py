from pathlib import Path
from node import Node
from graph import Graph
from dijkstra import (
    dijkstra,
    get_shortest_path,
    all_pairs_shortest_paths,
    print_shortest_paths,
    print_distance_matrix
)
from dp import (
    read_time_budget,
    maximize_priority_dp,
    greedy_maximize_priority,
)
import csv
from UI.interface import draw_graph

DIFFICULTY = "mytests"
LEVEL = "1"

# Make dataset paths relative to repository root (two levels up from this file's folder)
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_NODES = BASE_DIR / "datasets" / DIFFICULTY / LEVEL / "pontos.csv"
PATH_EDGES = BASE_DIR / "datasets" / DIFFICULTY / LEVEL / "ruas.csv"
PATH_INITIAL = BASE_DIR / "datasets" / DIFFICULTY / LEVEL / "dados_iniciais.csv"

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
            tempo = getattr(n, "tempo_cuidados_minimos", None)
            is_h = getattr(n, "is_hospital", None)
            resgatado = getattr(n, "resgatado", False)
            print(f"  {nid}: tipo={tipo} nome={nome} prioridade={prioridade} tempo={tempo} is_hospital={is_h} resgatado={resgatado}")
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
    # Carrega os dados do grafo
    print("Carregando grafo do dataset...")
    load_nodes(PATH_NODES)
    load_edges(PATH_EDGES)
    # opcional: zera estado de resgate no início da execução
    for _nid, _n in g.nodes.items():
        if getattr(_n, 'tipo', '') == 'paciente':
            _n.resgatado = False
    print_graph(g)
    # Desenha o grafo usando NetworkX/Matplotlib (UI)
    #try:
    #    draw_graph(g, show=True)
    #except Exception as e:
    #    print(f"Aviso: falha ao desenhar grafo na UI: {e}")
    
    # Calcula caminhos mais curtos entre todos os pares de nós
    print("\nCalculando caminhos mais curtos com Dijkstra...")
    all_paths = all_pairs_shortest_paths(g)


    # Lê budget de tempo
    time_budget = read_time_budget(PATH_INITIAL)
    if time_budget is None:
        print("\n[AVISO] Nenhum tempo_total encontrado em dados_iniciais.csv; não será feita otimização por budget.\n")
        return

    print(f"\nTempo total disponível (budget): {time_budget:.2f}")

    # Identifica hospitais e pacientes
    hospital_ids = [nid for nid, n in g.nodes.items() if getattr(n, 'is_hospital', False)]
    pacientes = [(nid, n) for nid, n in g.nodes.items() if getattr(n, 'tipo', '') == 'paciente' and (n.prioridade or 0) > 0]
    num_pacientes = len(pacientes)
    print(f"Hospitais encontrados: {len(hospital_ids)} | Pacientes candidatos: {num_pacientes}")

    if not hospital_ids:
        print("Nenhum hospital encontrado no grafo; abortando.")
        return

    # Escolhe método conforme número de pacientes
    use_dp = num_pacientes <= 20
    metodo = 'DP (ótimo)' if use_dp else 'Heurística (gananciosa)'
    print(f"Método de otimização: {metodo}")

    best = {
        'hospital': None,
        'route': [],
        'priority': 0,
        'time': float('inf'),
        'optimal': use_dp,
    }

    for hid in hospital_ids:
        if use_dp:
            route, prio, t, _ = maximize_priority_dp(g, all_paths, hid, time_budget, hospital_ids)
        else:
            route, prio, t, _ = greedy_maximize_priority(g, all_paths, hid, time_budget, hospital_ids)
        if prio > best['priority'] or (prio == best['priority'] and t < best['time']):
            best.update({'hospital': hid, 'route': route, 'priority': prio, 'time': t, 'optimal': use_dp})

    if not best['route'] or best['hospital'] is None or best['priority'] == 0:
        print("Nenhuma rota viável dentro do budget encontrada a partir de nenhum hospital.")
        return

    # Impressão detalhada da rota (agora com hospitais variáveis)
    print("\n" + "="*80)
    print("SOLUÇÃO ENCONTRADA")
    print("="*80)
    hid = best['hospital']
    print(f"Hospital inicial: {hid} ({g.nodes[hid].nome})")
    print(f"Tipo de solução: {'ÓTIMA (DP)' if best['optimal'] else 'HEURÍSTICA'}")

    # A rota agora é uma lista de tuplas (tipo, nid)
    route_nodes = best['route']
    
    # Extrai pacientes resgatados
    chosen_patients = [nid for tipo, nid in route_nodes if tipo == 'P']
    
    if not chosen_patients:
        print("Nenhum paciente selecionado dentro do budget.")
        print("="*80)
        return

    # Monta percurso para exibição
    percurso_display = []
    for tipo, nid in route_nodes:
        if tipo == 'H':
            percurso_display.append(f"H{nid}")
        else:
            percurso_display.append(f"P{nid}")
    
    print("Percurso: " + " → ".join(percurso_display))
    
    # Calcula tempos detalhados
    total_transp = 0.0
    total_atend = 0.0
    
    print("\nDetalhamento:")
    for i in range(len(route_nodes) - 1):
        tipo_curr, nid_curr = route_nodes[i]
        tipo_next, nid_next = route_nodes[i + 1]
        
        # Distância entre localizações consecutivas
        d = all_paths.get((nid_curr, nid_next), (float('inf'), []))[0]
        if d != float('inf'):
            total_transp += d
        
        # Se próximo é paciente, adiciona tempo de atendimento
        if tipo_next == 'P':
            node = g.nodes[nid_next]
            g.nodes[nid_next].resgatado = True
            tempo = getattr(node, 'tempo_cuidados_minimos', 0) or 0
            total_atend += float(tempo)
            
            prev_label = f"H{nid_curr}" if tipo_curr == 'H' else f"P{nid_curr}"
            print(f"  {prev_label} → P{nid_next}: {d:.2f} (transporte) + {tempo:.2f} (atendimento)")

    print("-"*80)
    print(f"Prioridade total atendida: {best['priority']}")
    print(f"Tempo total transporte: {total_transp:.2f}")
    print(f"Tempo total atendimento: {total_atend:.2f}")
    print(f"Tempo total usado: {total_transp + total_atend:.2f} (budget={time_budget:.2f})")
    
    # Hospital final
    final_tipo, final_nid = route_nodes[-1]
    if final_tipo == 'H':
        print(f"Hospital final: {final_nid} ({g.nodes[final_nid].nome})")
    
    # Resumo final dos pacientes resgatados
    rescued_ids = [str(nid) for nid in chosen_patients]
    print(f"Pacientes resgatados: {', '.join(rescued_ids) if rescued_ids else 'nenhum'}")
    print("="*80)

if __name__ == "__main__":
    main()