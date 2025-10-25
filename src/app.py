"""
🚑 Otimizador de Rotas de Ambulância - Interface Streamlit
Sistema de otimização de rotas para maximizar prioridade de atendimentos
respeitando restrições de tempo.
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import csv
import time
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from io import BytesIO

# Imports do projeto
from node import Node
from graph import Graph
from dijkstra import all_pairs_shortest_paths
from dp import (
    read_time_budget,
    maximize_priority_dp,
    greedy_maximize_priority,
)

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="🚑 Otimizador de Rotas de Ambulância",
    page_icon="🚑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONSTANTES E CONFIGURAÇÃO
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "datasets"

# Mapeamento de datasets disponíveis
DATASETS = {
    "Easy 1": "easy/1",
    "Easy 2": "easy/2",
    "Easy 3": "easy/3",
    "Medium 4": "medium/4",
    "Medium 5": "medium/5",
    "Medium 6": "medium/6",
    "Medium 7": "medium/7",
    "Hard 8": "hard/8",
    "Hard 9": "hard/9",
    "Hard 10": "hard/10",
}

# ============================================================================
# FUNÇÕES DE CARREGAMENTO DE DADOS
# ============================================================================

@st.cache_data
def load_dataset(dataset_path: str) -> Tuple[Graph, Dict, float, int]:
    """
    Carrega um dataset completo e retorna:
    - Graph configurado
    - Dados iniciais (hospital_id, tempo_total)
    - Estatísticas do dataset
    """
    g = Graph()
    
    path_nodes = DATASETS_DIR / dataset_path / "pontos.csv"
    path_edges = DATASETS_DIR / dataset_path / "ruas.csv"
    path_initial = DATASETS_DIR / dataset_path / "dados_iniciais.csv"
    
    # Carrega nós
    with open(path_nodes, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            nid = int(row.get('id') or row.get('Id') or row.get('ID'))
            tipo = row.get('tipo', '')
            nome = row.get('nome', '')
            prioridade = int(row['prioridade']) if row.get('prioridade') else None
            tempo = float(row['tempo_cuidados_minimos']) if row.get('tempo_cuidados_minimos') else None
            
            # Determina se é hospital
            is_h_col = row.get('is_hospital', '')
            is_h = False
            try:
                if isinstance(is_h_col, str) and is_h_col.strip() != '':
                    is_h = is_h_col.lower().strip() in ('1', 'true', 'sim', 'yes')
            except Exception:
                is_h = False
            
            if not is_h and isinstance(tipo, str) and tipo.strip().lower() == 'hospital':
                is_h = True
            
            n = Node(
                id=nid,
                tipo=tipo,
                nome=nome,
                prioridade=prioridade,
                tempo_cuidados_minimos=tempo,
                is_hospital=is_h
            )
            g.add_node(n)
    
    # Carrega arestas
    with open(path_edges, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            a_raw = row.get('ponto_origem') or row.get('from') or row.get('a')
            b_raw = row.get('ponto_destino') or row.get('to') or row.get('b')
            w_raw = row.get('tempo_transporte') or row.get('weight') or row.get('peso')
            
            if a_raw is None or b_raw is None:
                continue
            
            try:
                a = int(a_raw)
                b = int(b_raw)
                w = float(w_raw) if w_raw not in (None, '') else 1.0
            except ValueError:
                continue
            
            g.add_edge(a, b, w, bidirectional=True)
    
    # Lê dados iniciais
    tempo_total = read_time_budget(path_initial)
    hospital_id = None
    
    with open(path_initial, newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            try:
                hospital_id = int(row.get('ponto_inicial') or list(row.values())[0])
                break
            except:
                pass
    
    return g, hospital_id, tempo_total

def get_dataset_stats(g: Graph) -> Dict:
    """Retorna estatísticas do dataset carregado."""
    hospitais = [n for n in g.nodes.values() if n.is_hospital]
    pacientes = [n for n in g.nodes.values() if n.tipo == 'paciente']
    
    return {
        'total_nodes': len(g.nodes),
        'hospitais': len(hospitais),
        'pacientes': len(pacientes),
        'arestas': sum(len(adj) for adj in g.adjacency.values()) // 2,  # Bidirecionais
        'hospital_list': hospitais,
        'paciente_list': pacientes,
    }

# ============================================================================
# FUNÇÕES DE OTIMIZAÇÃO
# ============================================================================

def calculate_optimal_route(g: Graph, hospital_id: int, time_budget: float, force_algorithm: str = 'auto'):
    """
    Calcula a rota ótima usando DP ou heurística conforme necessário.
    Retorna dict com resultados completos.
    
    Args:
        g: Grafo com nós e arestas
        hospital_id: ID do hospital inicial
        time_budget: Tempo total disponível
        force_algorithm: 'auto', 'dp', ou 'greedy'
    """
    # Calcula caminhos mais curtos
    start_dijkstra = time.time()
    all_paths = all_pairs_shortest_paths(g)
    time_dijkstra = time.time() - start_dijkstra
    
    # Zera estado de resgate
    for n in g.nodes.values():
        if n.tipo == 'paciente':
            n.resgatado = False
    
    # Identifica pacientes candidatos
    pacientes = [
        (nid, n) for nid, n in g.nodes.items()
        if n.tipo == 'paciente' and (n.prioridade or 0) > 0
    ]
    num_pacientes = len(pacientes)
    
    # Identifica todos os hospitais
    all_hospitals = [nid for nid, n in g.nodes.items() if n.is_hospital]
    
    # Escolhe método
    if force_algorithm == 'auto':
        use_dp = num_pacientes <= 20
    elif force_algorithm == 'dp':
        use_dp = True
    else:  # greedy
        use_dp = False
    
    metodo = 'DP Ótimo' if use_dp else 'Heurística Gananciosa'
    
    # Complexidade do algoritmo com explicações
    num_nodes = len(g.nodes)
    num_hospitals = len(all_hospitals)
    num_edges = sum(len(adj) for adj in g.adjacency.values()) // 2
    
    if use_dp:
        complexity = f"O(H × 2^P × P × V)"
        complexity_values = f"O({num_hospitals} × 2^{num_pacientes} × {num_pacientes} × {num_nodes})"
        complexity_explanation = (
            "**H** = Número de hospitais (pontos de partida/retorno)\n"
            "**P** = Número de pacientes candidatos\n"
            "**V** = Número total de vértices (nós) no grafo\n"
            "**2^P** = Número de subconjuntos possíveis de pacientes (programação dinâmica com bitmask)"
        )
    else:
        complexity = f"O(H × P² × V)"
        complexity_values = f"O({num_hospitals} × {num_pacientes}² × {num_nodes})"
        complexity_explanation = (
            "**H** = Número de hospitais (pontos de partida/retorno)\n"
            "**P** = Número de pacientes candidatos\n"
            "**V** = Número total de vértices (nós) no grafo\n"
            "**P²** = Iterações para selecionar próximo paciente de forma gulosa"
        )
    
    dijkstra_complexity = f"O(V² × (V + E) log V)"
    dijkstra_values = f"O({num_nodes}² × ({num_nodes} + {num_edges}) log {num_nodes})"
    dijkstra_explanation = (
        "**V** = Número de vértices (nós)\n"
        "**E** = Número de arestas\n"
        "Executa Dijkstra V vezes (uma para cada nó)"
    )
    
    # Executa otimização
    start_optimization = time.time()
    if use_dp:
        route, priority, time_used, optimal = maximize_priority_dp(
            g, all_paths, hospital_id, time_budget, all_hospitals
        )
    else:
        route, priority, time_used, optimal = greedy_maximize_priority(
            g, all_paths, hospital_id, time_budget, all_hospitals
        )
    time_optimization = time.time() - start_optimization
    
    # Monta percurso detalhado (hospital -> paciente -> hospital -> ...)
    # A rota agora é uma lista de tuplas (tipo, nid)
    chosen_patients = []
    full_path = []
    
    for tipo, nid in route:
        full_path.append(nid)
        if tipo == 'P':  # Paciente
            chosen_patients.append(nid)
    
    # Marca resgatados
    for pid in chosen_patients:
        if pid in g.nodes:
            g.nodes[pid].resgatado = True
    
    return {
        'route': route,
        'full_path': full_path,
        'chosen_patients': chosen_patients,
        'priority': priority,
        'time_used': time_used,
        'method': metodo,
        'is_optimal': optimal,
        'num_patients': len(chosen_patients),
        'all_paths': all_paths,
        'time_dijkstra': time_dijkstra,
        'time_optimization': time_optimization,
        'time_total': time_dijkstra + time_optimization,
        'complexity': complexity,
        'complexity_values': complexity_values,
        'complexity_explanation': complexity_explanation,
        'dijkstra_complexity': dijkstra_complexity,
        'dijkstra_values': dijkstra_values,
        'dijkstra_explanation': dijkstra_explanation,
    }

# ============================================================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================================================

def create_graph_visualization(g: Graph, result: Dict, hospital_id: int):
    """
    Cria visualização do grafo usando NetworkX e Matplotlib.
    Destaca a rota escolhida.
    """
    # Cria grafo NetworkX
    G = nx.Graph()
    
    # Adiciona nós
    for nid, node in g.nodes.items():
        G.add_node(nid, node=node)
    
    # Adiciona arestas
    edges_info = []
    for u, neighbors in g.adjacency.items():
        for v, w in neighbors:
            if u < v:  # Evita duplicatas em grafo não-direcionado
                G.add_edge(u, v, weight=w)
                edges_info.append((u, v, w))
    
    # Layout
    pos = nx.spring_layout(G, seed=42, k=2, iterations=50)
    
    # Figura
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Determina conjunto de arestas da rota
    route_edges = set()
    full_path = result.get('full_path', [])
    all_paths = result.get('all_paths', {})
    # highlight_nodes conterá todos os nós que aparecem nos caminhos usados
    highlight_nodes = set()
    for i in range(len(full_path) - 1):
        u0, v0 = full_path[i], full_path[i + 1]
        # procura o caminho mais curto entre u0 e v0 (pode conter nós intermediários)
        d_path = all_paths.get((u0, v0))
        if d_path:
            _d, path = d_path
        else:
            path = []

        if path and len(path) >= 2:
            # adiciona cada aresta do caminho à lista de arestas da rota
            for j in range(len(path) - 1):
                a, b = path[j], path[j + 1]
                route_edges.add((min(a, b), max(a, b)))
            highlight_nodes.update(path)
        else:
            # fallback: adiciona a aresta direta entre u0 e v0
            route_edges.add((min(u0, v0), max(u0, v0)))
            highlight_nodes.update([u0, v0])
    
    # Desenha arestas normais
    normal_edges = [(u, v) for u, v, _ in edges_info if (min(u, v), max(u, v)) not in route_edges]
    nx.draw_networkx_edges(
        G, pos, edgelist=normal_edges,
        width=1, alpha=0.3, edge_color='gray', ax=ax
    )
    
    # Desenha arestas da rota
    route_edge_list = [(u, v) for u, v, _ in edges_info if (min(u, v), max(u, v)) in route_edges]
    nx.draw_networkx_edges(
        G, pos, edgelist=route_edge_list,
        width=4, alpha=0.8, edge_color='red', ax=ax
    )
    
    # Prepara cores e tamanhos dos nós
    node_colors = []
    node_sizes = []
    node_shapes = []
    
    for nid in G.nodes():
        node = g.nodes[nid]
        if node.is_hospital:
            node_colors.append('white')
            node_sizes.append(1200)
        else:
            # Cor por prioridade (gradiente verde -> amarelo -> vermelho)
            prio = node.prioridade or 0
            if prio == 0:
                color = 'lightgray'
            elif prio <= 10:
                color = 'green'
            elif prio <= 20:
                color = 'yellow'
            elif prio <= 30:
                color = 'orange'
            else:
                color = 'red'

            # se o nó estiver em highlight_nodes (nó do caminho intermediário), destaque-o
            if nid in highlight_nodes and not node.is_hospital:
                # sobrescreve a cor para um tom chamativo
                color = 'deepskyblue'

            node_colors.append(color)

            # Tamanho proporcional à prioridade
            size = 300 + (prio * 15)
            node_sizes.append(size)
    
    # Desenha nós
    nx.draw_networkx_nodes(
        G, pos,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=0.9,
        edgecolors='black',
        linewidths=2,
        ax=ax
    )
    
    # Labels dos nós
    labels = {}
    for nid, node in g.nodes.items():
        if node.is_hospital:
            labels[nid] = f"🏥\n{node.nome}\n({nid})"
        else:
            resgatado = "✓" if getattr(node, 'resgatado', False) else ""
            labels[nid] = f"{node.nome}\n({nid})\nP:{node.prioridade}{resgatado}"
    
    nx.draw_networkx_labels(
        G, pos, labels, font_size=8, font_weight='bold', ax=ax
    )
    
    # Labels das arestas (tempos)
    edge_labels = {(u, v): f"{w:.1f}" for u, v, w in edges_info}
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels, font_size=7, ax=ax
    )
    
    # Legenda
    legend_elements = [
        mpatches.Patch(facecolor='white', edgecolor='black', label='Hospital'),
        mpatches.Patch(color='green', label='Paciente (Prioridade ≤10)'),
        mpatches.Patch(color='yellow', label='Paciente (Prioridade 11-20)'),
        mpatches.Patch(color='orange', label='Paciente (Prioridade 21-30)'),
        mpatches.Patch(color='red', label='Paciente (Prioridade >30)'),
        mpatches.Patch(color='lightgray', label='Não atendido'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    ax.set_title(
        f"Grafo de Atendimentos - {result['method']}\n"
        f"Prioridade Total: {result['priority']} | "
        f"Tempo: {result['time_used']:.2f} | "
        f"Pacientes: {result['num_patients']}",
        fontsize=14, fontweight='bold'
    )
    ax.axis('off')
    
    plt.tight_layout()
    return fig

def create_route_table(g: Graph, result: Dict, hospital_id: int):
    """Cria DataFrame com detalhes da rota."""
    rows = []
    full_path = result['full_path']
    tempo_acum = 0.0
    
    for idx, nid in enumerate(full_path):
        node = g.nodes[nid]
        
        # Calcula tempo desde último nó
        if idx > 0:
            prev_nid = full_path[idx - 1]
            # Busca tempo de transporte
            dist_info = result['all_paths'].get((prev_nid, nid), (0, []))
            tempo_transporte = dist_info[0]
            path_between = dist_info[1] if len(dist_info) > 1 else []
            path_str = " → ".join(str(x) for x in path_between) if path_between else '-'
            tempo_acum += tempo_transporte
        
        # Adiciona tempo de atendimento se for paciente
        tempo_atend = 0
        if not node.is_hospital and node.tipo == 'paciente':
            tempo_atend = node.tempo_cuidados_minimos or 0
            tempo_acum += tempo_atend
        
        rows.append({
            'Ordem': idx + 1,
            'Tipo': '🏥 Hospital' if node.is_hospital else '👤 Paciente',
            'Nome': node.nome,
            'ID': nid,
            'Prioridade': node.prioridade if not node.is_hospital else '-',
            'Tempo Atend.': f"{tempo_atend:.1f}" if tempo_atend > 0 else '-',
            'Tempo Acum.': f"{tempo_acum:.2f}",
            'Caminho': path_str if idx > 0 else '-',
        })
    
    return pd.DataFrame(rows)

# ============================================================================
# FUNÇÃO PRINCIPAL DA APP
# ============================================================================

def main():
    # ========================================================================
    # SIDEBAR - Seleção e Configuração
    # ========================================================================
    
    st.sidebar.title("🚑 Otimizador de Rotas")
    st.sidebar.markdown("---")
    
    # Seleção de dataset
    st.sidebar.subheader("📂 Seleção de Dataset")
    selected_dataset = st.sidebar.selectbox(
        "Escolha o dataset:",
        options=list(DATASETS.keys()),
        index=0
    )
    
    dataset_path = DATASETS[selected_dataset]
    
    # Carrega dataset
    try:
        with st.spinner(f"Carregando {selected_dataset}..."):
            g, default_hospital_id, default_time_budget = load_dataset(dataset_path)
            stats = get_dataset_stats(g)
    except Exception as e:
        st.error(f"❌ Erro ao carregar dataset: {e}")
        return
    
    # Preview do dataset
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Preview do Dataset")
    st.sidebar.metric("🏥 Hospitais", stats['hospitais'])
    st.sidebar.metric("👤 Pacientes", stats['pacientes'])
    st.sidebar.metric("⏱️ Tempo Disponível", f"{default_time_budget:.1f}")
    
    if stats['hospital_list']:
        hospital_info = stats['hospital_list'][0]
        st.sidebar.info(f"**Hospital inicial:** {hospital_info.nome} (ID: {hospital_info.id})")
    
    # Override de parâmetros
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Configuração Avançada")
    
    override_params = st.sidebar.checkbox("Alterar parâmetros padrão")
    
    if override_params:
        # Lista de hospitais disponíveis
        hospital_options = {
            f"{h.nome} (ID: {h.id})": h.id
            for h in stats['hospital_list']
        }
        
        selected_hospital_label = st.sidebar.selectbox(
            "Hospital inicial:",
            options=list(hospital_options.keys()),
            index=0
        )
        hospital_id = hospital_options[selected_hospital_label]
        
        time_budget = st.sidebar.number_input(
            "Tempo total disponível:",
            min_value=0.0,
            value=float(default_time_budget),
            step=0.5,
            format="%.1f"
        )
    else:
        hospital_id = default_hospital_id
        time_budget = default_time_budget
    
    # Seleção de algoritmo
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧮 Seleção de Algoritmo")
    
    algorithm_choice = st.sidebar.radio(
        "Escolha o algoritmo de otimização:",
        options=['Automático', 'DP (Programação Dinâmica)', 'Heurística Gulosa'],
        index=0,
        help=(
            "**Automático:** Usa DP para ≤20 pacientes, Heurística para >20\n\n"
            "**DP:** Solução ótima, mas exponencial (pode ser lento)\n\n"
            "**Heurística:** Solução aproximada, mais rápida para muitos pacientes"
        )
    )
    
    # Mapeia escolha para parâmetro
    if algorithm_choice == 'Automático':
        force_algorithm = 'auto'
    elif algorithm_choice == 'DP (Programação Dinâmica)':
        force_algorithm = 'dp'
    else:
        force_algorithm = 'greedy'
    
    # Aviso se DP for escolhido com muitos pacientes
    if force_algorithm == 'dp' and stats['pacientes'] > 20:
        st.sidebar.warning(
            f"⚠️ Atenção: DP com {stats['pacientes']} pacientes pode ser muito lento! "
            f"Complexidade: O(2^{stats['pacientes']}) subconjuntos."
        )
    
    # ========================================================================
    # MAIN AREA - Botão de Cálculo e Resultados
    # ========================================================================
    
    st.title("🚑 Sistema de Otimização de Rotas de Ambulância")
    st.markdown("---")
    
    # Botão de cálculo
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        calculate_button = st.button(
            "🚀 CALCULAR ROTA ÓTIMA",
            type="primary",
            use_container_width=True
        )
    
    # Estado da aplicação
    if 'result' not in st.session_state:
        st.session_state.result = None
    
    if calculate_button:
        with st.spinner("🔄 Calculando rota ótima..."):
            try:
                result = calculate_optimal_route(g, hospital_id, time_budget, force_algorithm)
                st.session_state.result = result
            except Exception as e:
                st.error(f"❌ Erro ao calcular rota: {e}")
                import traceback
                st.code(traceback.format_exc())
                return
    
    # Exibe resultados se disponíveis
    result = st.session_state.result
    
    if result is None:
        st.info("👆 Selecione um dataset e clique em **CALCULAR ROTA ÓTIMA** para começar.")
        
        # Preview dos pacientes
        st.subheader("📋 Pacientes Disponíveis no Dataset")
        pacientes_df = pd.DataFrame([
            {
                'ID': p.id,
                'Nome': p.nome,
                'Prioridade': p.prioridade,
                'Tempo Atend.': p.tempo_cuidados_minimos,
            }
            for p in stats['paciente_list']
        ])
        st.dataframe(pacientes_df, use_container_width=True)
        
        return
    
    # ========================================================================
    # RESULTADOS - Métricas Principais
    # ========================================================================
    
    st.markdown("---")
    
    # Mensagem de sucesso/aviso
    if result['priority'] > 0:
        if result['is_optimal']:
            st.success(f"✅ **Rota Calculada com Sucesso!** (Método: {result['method']})")
        else:
            st.warning(f"⚠️ **Rota Calculada!** (Método: {result['method']} - Solução aproximada)")
    else:
        st.error("❌ Nenhuma rota viável encontrada dentro do budget de tempo.")
        return
    
    # Informação de complexidade e tempo
    with st.expander("📊 Análise de Complexidade e Desempenho", expanded=True):
        st.markdown("### 🔍 Complexidade Computacional")
        
        # Dijkstra
        st.markdown("**1️⃣ Dijkstra (Caminhos Mais Curtos):**")
        st.code(f"{result['dijkstra_complexity']} = {result['dijkstra_values']}", language="")
        st.markdown(result['dijkstra_explanation'])
        st.caption(f"⏱️ Tempo de execução: **{result['time_dijkstra']:.4f}s**")
        
        st.markdown("---")
        
        # Otimização
        st.markdown(f"**2️⃣ {result['method']}:**")
        st.code(f"{result['complexity']} = {result['complexity_values']}", language="")
        st.markdown(result['complexity_explanation'])
        st.caption(f"⏱️ Tempo de execução: **{result['time_optimization']:.4f}s**")
        
        st.markdown("---")
        
        # Total
        st.markdown("### ⏱️ Tempo Total de Execução")
        col_t1, col_t2, col_t3 = st.columns(3)
        with col_t1:
            st.metric("Dijkstra", f"{result['time_dijkstra']:.4f}s")
        with col_t2:
            st.metric("Otimização", f"{result['time_optimization']:.4f}s")
        with col_t3:
            st.metric("Total", f"{result['time_total']:.4f}s", delta=None)
    
    # Métricas em colunas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Prioridade Total",
            value=result['priority'],
            help="Soma das prioridades de todos os pacientes atendidos"
        )
    
    with col2:
        tempo_pct = (result['time_used'] / time_budget * 100) if time_budget > 0 else 0
        st.metric(
            label="⏱️ Tempo Usado",
            value=f"{result['time_used']:.1f} / {time_budget:.1f}",
            delta=f"{tempo_pct:.1f}%",
            help="Tempo total usado vs disponível"
        )
    
    with col3:
        st.metric(
            label="👥 Pacientes Atendidos",
            value=result['num_patients'],
            help="Número de pacientes resgatados"
        )
    
    with col4:
        st.metric(
            label="🔧 Método",
            value=result['method'],
            help="Algoritmo utilizado para otimização"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # VISUALIZAÇÕES - Grafo e Tabela
    # ========================================================================
    
    tab1, tab2 = st.tabs(["🗺️ Visualização do Grafo", "📋 Detalhes da Rota"])
    
    with tab1:
        st.subheader("Mapa de Atendimentos")
        try:
            fig = create_graph_visualization(g, result, hospital_id)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Erro ao gerar visualização: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    with tab2:
        st.subheader("Sequência de Atendimentos")
        try:
            route_df = create_route_table(g, result, hospital_id)
            st.dataframe(route_df, use_container_width=True, height=400)
            
            # Resumo
            st.markdown("---")
            st.markdown("### 📊 Resumo da Operação")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(f"""
                **Informações da Rota:**
                - **Total de paradas:** {len(result['full_path'])}
                - **Pacientes atendidos:** {result['num_patients']}
                - **Prioridade acumulada:** {result['priority']}
                """)
            
            with col_b:
                st.markdown(f"""
                **Tempos:**
                - **Tempo total usado:** {result['time_used']:.2f}
                - **Tempo disponível:** {time_budget:.2f}
                - **Tempo restante:** {max(0, time_budget - result['time_used']):.2f}
                """)
            
            # Lista de pacientes atendidos
            if result['chosen_patients']:
                st.markdown("**Pacientes Atendidos:**")
                pacientes_info = []
                for pid in result['chosen_patients']:
                    node = g.nodes[pid]
                    pacientes_info.append(f"- {node.nome} (ID: {pid}, Prioridade: {node.prioridade})")
                st.markdown("\n".join(pacientes_info))
            
        except Exception as e:
            st.error(f"Erro ao gerar tabela: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    # ========================================================================
    # EXPORTAÇÃO - Relatório PDF (Tarefa Extra)
    # ========================================================================
    
    st.markdown("---")
    st.subheader("📄 Exportação de Relatório")
    
    col_pdf1, col_pdf2, col_pdf3 = st.columns([1, 2, 1])
    
    with col_pdf2:
        if st.button("📥 Gerar Nota Clínica (CSV)", use_container_width=True):
            # Gera CSV como alternativa ao PDF (mais simples)
            try:
                csv_buffer = BytesIO()
                route_df = create_route_table(g, result, hospital_id)
                route_df.to_csv(csv_buffer, index=False, encoding='utf-8')
                csv_buffer.seek(0)
                
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_buffer,
                    file_name=f"nota_clinica_{selected_dataset.replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.success("✅ Relatório CSV gerado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao gerar relatório: {e}")

# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
