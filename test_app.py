"""
Script de teste rápido para verificar se app.py funciona corretamente
sem precisar abrir o navegador.
"""

from pathlib import Path
import sys

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from node import Node
from graph import Graph
from dijkstra import all_pairs_shortest_paths
from dp import read_time_budget, maximize_priority_dp
import csv

def test_load_dataset():
    """Testa carregamento de um dataset."""
    print("🧪 Teste 1: Carregamento de Dataset")
    
    BASE_DIR = Path(__file__).parent
    dataset_path = BASE_DIR / "datasets" / "easy" / "1"
    
    g = Graph()
    
    # Carrega nós
    with open(dataset_path / "pontos.csv", newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            nid = int(row['id'])
            tipo = row.get('tipo', '')
            nome = row.get('nome', '')
            prioridade = int(row['prioridade']) if row.get('prioridade') else None
            tempo = float(row['tempo_cuidados_minimos']) if row.get('tempo_cuidados_minimos') else None
            is_h = tipo.lower() == 'hospital'
            
            n = Node(id=nid, tipo=tipo, nome=nome, prioridade=prioridade, 
                    tempo_cuidados_minimos=tempo, is_hospital=is_h)
            g.add_node(n)
    
    # Carrega arestas
    with open(dataset_path / "ruas.csv", newline='', encoding='utf-8') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            a = int(row['ponto_origem'])
            b = int(row['ponto_destino'])
            w = float(row['tempo_transporte'])
            g.add_edge(a, b, w, bidirectional=True)
    
    print(f"✅ Carregado: {len(g.nodes)} nós, {sum(len(adj) for adj in g.adjacency.values()) // 2} arestas")
    return g, dataset_path

def test_optimization(g, dataset_path):
    """Testa otimização."""
    print("\n🧪 Teste 2: Otimização de Rota")
    
    # Lê tempo
    tempo_total = read_time_budget(dataset_path / "dados_iniciais.csv")
    print(f"⏱️  Tempo disponível: {tempo_total}")
    
    # Calcula caminhos
    all_paths = all_pairs_shortest_paths(g)
    
    # Otimiza
    hospital_id = 0
    route, priority, time_used, optimal = maximize_priority_dp(
        g, all_paths, hospital_id, tempo_total
    )
    
    print(f"✅ Rota calculada:")
    print(f"   - Pacientes atendidos: {len(route) - 1}")
    print(f"   - Prioridade total: {priority}")
    print(f"   - Tempo usado: {time_used:.2f}/{tempo_total}")
    print(f"   - Método: {'DP Ótimo' if optimal else 'Heurística'}")
    print(f"   - Rota: {' → '.join(str(x) for x in route)}")
    
    return route, priority

def test_visualization():
    """Testa se bibliotecas de visualização estão disponíveis."""
    print("\n🧪 Teste 3: Bibliotecas de Visualização")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit não instalado")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__}")
    except ImportError:
        print("❌ Pandas não instalado")
        return False
    
    try:
        import matplotlib
        print(f"✅ Matplotlib {matplotlib.__version__}")
    except ImportError:
        print("❌ Matplotlib não instalado")
        return False
    
    try:
        import networkx
        print(f"✅ NetworkX {networkx.__version__}")
    except ImportError:
        print("❌ NetworkX não instalado")
        return False
    
    return True

def main():
    print("=" * 60)
    print("🚑 TESTE DA APLICAÇÃO STREAMLIT")
    print("=" * 60)
    
    try:
        # Teste 1: Carregamento
        g, dataset_path = test_load_dataset()
        
        # Teste 2: Otimização
        route, priority = test_optimization(g, dataset_path)
        
        # Teste 3: Visualização
        libs_ok = test_visualization()
        
        print("\n" + "=" * 60)
        if priority > 0 and libs_ok:
            print("✅ TODOS OS TESTES PASSARAM!")
            print("\n🚀 Para executar a aplicação:")
            print("   streamlit run src/app.py")
            print("\n   ou")
            print("   ./run_app.sh")
        else:
            print("⚠️  ALGUNS TESTES FALHARAM")
            if not libs_ok:
                print("\n📦 Instale as dependências:")
                print("   pip install -r requirements.txt")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
