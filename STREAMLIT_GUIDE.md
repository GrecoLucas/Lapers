# 🚑 Interface Streamlit - Guia de Uso

## Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

ou individualmente:
```bash
pip install streamlit pandas numpy matplotlib networkx
```

## Execução

A partir da raiz do projeto, execute:

```bash
streamlit run src/app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

## Funcionalidades

### 1. Seleção de Dataset
- Use o dropdown na sidebar para escolher entre os 10 datasets disponíveis (Easy 1-3, Medium 4-7, Hard 8-10)
- O preview mostra automaticamente: número de hospitais, pacientes e tempo disponível

### 2. Configuração (Opcional)
- Marque "Alterar parâmetros padrão" para customizar:
  - Hospital inicial
  - Tempo total disponível

### 3. Cálculo da Rota
- Clique no botão "🚀 CALCULAR ROTA ÓTIMA"
- O sistema escolhe automaticamente:
  - **DP Ótimo** para ≤20 pacientes
  - **Heurística Gananciosa** para >20 pacientes

### 4. Visualização dos Resultados

#### Métricas Principais:
- **Prioridade Total**: Soma das prioridades atendidas
- **Tempo Usado**: Tempo consumido vs disponível
- **Pacientes Atendidos**: Quantidade de pacientes resgatados
- **Método**: Algoritmo utilizado

#### Abas:
- **🗺️ Visualização do Grafo**: 
  - Nós coloridos por tipo e prioridade
  - Arestas da rota destacadas em vermelho
  - Labels com tempos de transporte
  
- **📋 Detalhes da Rota**:
  - Tabela sequencial de atendimentos
  - Tempos acumulados
  - Resumo da operação

### 5. Exportação
- Botão "📥 Gerar Nota Clínica (CSV)" para download do relatório

## Estrutura do Código

```python
src/app.py
├── Configuração da página (st.set_page_config)
├── Constantes e mapeamento de datasets
├── Funções de carregamento (@st.cache_data)
├── Funções de otimização (reutiliza dp.py)
├── Funções de visualização (NetworkX + Matplotlib)
└── Interface principal (main)
```

## Legenda do Grafo

- 🏥 **Quadrado Vermelho**: Hospital
- **Círculos Coloridos**: Pacientes
  - Verde: Prioridade ≤10
  - Amarelo: Prioridade 11-20
  - Laranja: Prioridade 21-30
  - Vermelho: Prioridade >30
- **Arestas Vermelhas Grossas**: Rota escolhida
- **Arestas Cinzas**: Outras conexões

## Troubleshooting

### Erro ao carregar dataset
- Verifique se todos os arquivos CSV existem na pasta do dataset
- Confirme encoding UTF-8 nos arquivos

### Visualização não aparece
- Instale matplotlib: `pip install matplotlib`
- Verifique versão do streamlit: `streamlit version`

### Performance lenta
- Datasets grandes (Hard) podem demorar mais
- O cache do Streamlit otimiza recarregamentos

## Desenvolvimento Durante Hackathon

Tempo estimado de implementação: **2-3 horas**

Checklist:
- [x] Estrutura básica da interface
- [x] Carregamento de datasets
- [x] Integração com algoritmos existentes
- [x] Visualização do grafo
- [x] Tabela de resultados
- [x] Exportação de dados
- [ ] PDF com reportlab (tarefa extra opcional)

## Comandos Úteis

```bash
# Executar em modo desenvolvimento (recarrega automaticamente)
streamlit run src/app.py

# Limpar cache
streamlit cache clear

# Versão do Streamlit
streamlit version
```

## Notas Técnicas

- **Cache**: `@st.cache_data` otimiza carregamento de datasets
- **Session State**: Mantém resultados entre interações
- **Layout Wide**: Melhor visualização do grafo
- **Paths Relativos**: Usa `Path(__file__).parent.parent` para compatibilidade
