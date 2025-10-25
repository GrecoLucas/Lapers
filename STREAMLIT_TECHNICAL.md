# 🚑 Aplicação Streamlit - Visão Geral Técnica

## Arquitetura da Solução

### Fluxo de Dados

```
Dataset (CSV) → Graph Loading → All-Pairs Shortest Paths → Optimization → Visualization
     ↓              ↓                    ↓                      ↓              ↓
pontos.csv      Node/Graph          Dijkstra             DP/Greedy      NetworkX+Matplotlib
ruas.csv                                                                       
dados_iniciais.csv
```

### Componentes Principais

#### 1. Carregamento de Dados (`load_dataset`)
- **Cache**: `@st.cache_data` para evitar recarregamentos desnecessários
- **Parsing flexível**: Suporta variações nos nomes das colunas
- **Validação**: Verifica integridade dos dados antes de processar

#### 2. Cálculo de Rotas (`calculate_optimal_route`)
- **Seleção automática de algoritmo**:
  - ≤20 pacientes → DP exato (solução ótima garantida)
  - >20 pacientes → Heurística gananciosa (rápida, solução aproximada)
- **Reutilização de código**: Usa funções de `dp.py` sem modificações
- **Estado do grafo**: Marca pacientes resgatados para tracking

#### 3. Visualização do Grafo (`create_graph_visualization`)

**Tecnologias**: NetworkX + Matplotlib

**Elementos visuais**:
- **Nós**:
  - Hospitais: Quadrados vermelhos grandes
  - Pacientes: Círculos coloridos por prioridade
  - Tamanho proporcional à prioridade
- **Arestas**:
  - Cinza claro: Conexões disponíveis
  - Vermelho grosso: Rota selecionada
  - Labels: Tempos de transporte
- **Layout**: Spring layout (força-direcional)

**Código-chave**:
```python
# Layout otimizado para visualização
pos = nx.spring_layout(G, seed=42, k=2, iterations=50)

# Destaque da rota
route_edges = set()
for i in range(len(full_path) - 1):
    u, v = full_path[i], full_path[i + 1]
    route_edges.add((min(u, v), max(u, v)))
```

#### 4. Tabela de Rota (`create_route_table`)
- **Cálculo de tempos acumulados**: Soma transporte + atendimento
- **Formato user-friendly**: Emojis e formatação clara
- **Export-ready**: Formato compatível com CSV

### Otimizações de Performance

1. **Caching**: Dataset só carrega uma vez por seleção
2. **Session State**: Resultados persistem entre interações
3. **Lazy loading**: Visualizações só são geradas quando necessárias
4. **Algoritmo adaptativo**: Escolha automática DP vs Heurística

### Estrutura de Estado

```python
st.session_state.result = {
    'route': [0, 1, 2],           # Hospital + pacientes escolhidos
    'full_path': [0,1,0,2,0],     # Percurso completo (ida/volta)
    'chosen_patients': [1, 2],     # Apenas pacientes
    'priority': 150,               # Soma de prioridades
    'time_used': 7.5,              # Tempo total consumido
    'method': 'DP Ótimo',          # Algoritmo usado
    'is_optimal': True,            # Flag de otimalidade
    'num_patients': 2,             # Contagem
    'all_paths': {...},            # Cache de caminhos
}
```

## Casos de Uso Detalhados

### Caso 1: Operação Padrão
**Cenário**: Médico quer otimizar rota para dataset Easy 1

1. Abrir aplicação: `streamlit run src/app.py`
2. Dataset já selecionado: "Easy 1"
3. Preview mostra: 1 hospital, 4 pacientes, 8.0 tempo
4. Clicar "CALCULAR ROTA ÓTIMA"
5. Ver resultados:
   - Prioridade: 100
   - Tempo: 7.0/8.0
   - Pacientes: 3
   - Método: DP Ótimo
6. Examinar grafo: Rota destacada em vermelho
7. Ver tabela: Sequência detalhada de paradas

### Caso 2: Teste de Sensibilidade
**Cenário**: Analista quer ver impacto de mais tempo

1. Selecionar "Medium 5"
2. Marcar "Alterar parâmetros padrão"
3. Aumentar tempo de 15.0 para 20.0
4. Calcular
5. Comparar: +2 pacientes atendidos, +80 prioridade

### Caso 3: Comparação de Datasets
**Cenário**: Pesquisador quer comparar algoritmos

1. Testar "Easy 1" → DP Ótimo, 3 pacientes
2. Testar "Hard 10" → Heurística, ? pacientes
3. Observar diferença de métodos e resultados

### Caso 4: Exportação para Relatório
**Cenário**: Gestor precisa documentar decisões

1. Calcular rota para "Medium 6"
2. Clicar "Gerar Nota Clínica (CSV)"
3. Download automático
4. Abrir em Excel/LibreOffice
5. Incluir em relatório gerencial

## Melhorias Futuras (Pós-Hackathon)

### Curto Prazo
- [ ] Exportação em PDF (reportlab)
- [ ] Comparação lado-a-lado de múltiplos cenários
- [ ] Histórico de cálculos na sessão

### Médio Prazo
- [ ] Upload de datasets customizados
- [ ] Editor visual de grafos
- [ ] Simulação "what-if" interativa
- [ ] API REST para integração

### Longo Prazo
- [ ] Mapa geográfico real (Folium/Plotly)
- [ ] Otimização multi-objetivo (tempo + custo + prioridade)
- [ ] Machine Learning para prever tempos
- [ ] Dashboard de analytics histórico

## Debug e Troubleshooting

### Problema: "Nenhuma rota viável"
**Causa**: Budget de tempo muito baixo
**Solução**: Verificar tempos de transporte, aumentar budget

### Problema: Grafo não aparece
**Causa**: Erro no NetworkX ou Matplotlib
**Debug**:
```python
# Verificar versões
import matplotlib
import networkx as nx
print(matplotlib.__version__)
print(nx.__version__)
```

### Problema: Performance lenta em Hard datasets
**Causa**: Muitos nós (>20 pacientes) → Heurística
**Otimização**: Esperada, é o comportamento correto

### Problema: Erro ao carregar CSV
**Causa**: Encoding ou formato inválido
**Debug**:
```bash
file datasets/easy/1/pontos.csv
# Deve retornar: UTF-8 Unicode text
```

## Testes Recomendados

### Teste 1: Carregamento
```bash
# Todos os datasets devem carregar sem erro
for d in easy/{1,2,3} medium/{4,5,6,7} hard/{8,9,10}; do
    echo "Testing $d..."
    # Verificar via interface
done
```

### Teste 2: Algoritmos
- Easy 1-3: DP deve retornar solução ótima
- Medium 4-7: Verificar escolha de algoritmo
- Hard 8-10: Heurística deve ser rápida (<5s)

### Teste 3: UI/UX
- [ ] Métricas atualizam corretamente
- [ ] Grafo é legível e informativo
- [ ] Tabela mostra todos os dados
- [ ] Download CSV funciona
- [ ] Override de parâmetros funciona

## Métricas de Sucesso

### Performance
- Carregamento: <1s
- Cálculo (DP): <3s
- Cálculo (Heurística): <1s
- Renderização grafo: <2s

### Usabilidade
- Cliques até resultado: 1 (apenas "Calcular")
- Tempo para entender interface: <30s
- Taxa de erro do usuário: <5%

### Funcionalidade
- Datasets suportados: 10/10 ✓
- Algoritmos funcionais: 2/2 ✓
- Visualizações: 2/2 ✓
- Exportação: 1/1 ✓

## Contribuindo

Para adicionar novos recursos:

1. **Nova visualização**: Adicionar em `create_graph_visualization`
2. **Novo algoritmo**: Integrar via `calculate_optimal_route`
3. **Nova métrica**: Adicionar em seção de métricas do `main`
4. **Novo formato export**: Criar função similar a `create_route_table`

## Licença e Créditos

Desenvolvido para hackathon de otimização de rotas de ambulância.
Tecnologias: Streamlit, NetworkX, Matplotlib, Pandas.
