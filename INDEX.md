# 📑 Índice de Documentação - Lapers

## 🚀 Início Rápido

**Nunca usou o sistema? Comece aqui:**

1. ✅ **[README.md](README.md)** - Visão geral do projeto
2. ✅ **[QUICK_COMMANDS.md](QUICK_COMMANDS.md)** - Comandos essenciais
3. ✅ Execute: `pip install -r requirements.txt && streamlit run src/app.py`

---

## 📚 Documentação por Público

### 👤 Para Usuários Finais

| Documento | Descrição | Tempo de Leitura |
|-----------|-----------|------------------|
| **[README.md](README.md)** | Visão geral completa do projeto | 5 min |
| **[STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)** | Guia detalhado de uso da interface | 10 min |
| **[QUICK_COMMANDS.md](QUICK_COMMANDS.md)** | Comandos úteis e atalhos | 5 min |

**Recomendação**: Ler na ordem acima.

### 💻 Para Desenvolvedores

| Documento | Descrição | Tempo de Leitura |
|-----------|-----------|------------------|
| **[STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md)** | Arquitetura e detalhes técnicos | 15 min |
| **[FILE_SUMMARY.md](FILE_SUMMARY.md)** | Resumo de todos os ficheiros criados | 8 min |
| **[src/app.py](src/app.py)** | Código-fonte principal (comentado) | 20 min |

**Recomendação**: Começar por STREAMLIT_TECHNICAL.md, depois ler o código.

### 📊 Para Gestores/Avaliadores

| Documento | Descrição | Tempo de Leitura |
|-----------|-----------|------------------|
| **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** | Resumo executivo com métricas | 5 min |
| **[README.md](README.md)** | Visão geral do projeto | 5 min |
| **[PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)** | Guia de apresentação (hackathon) | 10 min |

**Recomendação**: EXECUTIVE_SUMMARY.md tem todas as informações-chave.

### 🎤 Para Apresentadores

| Documento | Descrição | Uso |
|-----------|-----------|-----|
| **[PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)** | Script completo de apresentação | ⭐ PRINCIPAL |
| **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** | Dados para slides | Referência |
| **[QUICK_COMMANDS.md](QUICK_COMMANDS.md)** | Setup pré-apresentação | Checklist |

**Recomendação**: Revisar PRESENTATION_GUIDE.md 3 vezes antes do evento.

---

## 📁 Estrutura de Ficheiros

### Código Fonte (`src/`)
```
src/
├── app.py          ⭐ Interface Streamlit (NOVO - 550 linhas)
├── main.py         📋 CLI original
├── node.py         🔷 Classe Node
├── graph.py        🕸️ Classe Graph
├── dijkstra.py     🔍 Algoritmo Dijkstra
└── dp.py           🧮 Programação Dinâmica + Heurística
```

### Documentação (`./`)
```
./
├── README.md                   📖 Visão geral principal
├── EXECUTIVE_SUMMARY.md        📊 Resumo executivo
├── STREAMLIT_GUIDE.md          👤 Guia do usuário
├── STREAMLIT_TECHNICAL.md      💻 Docs técnicas
├── QUICK_COMMANDS.md           ⚡ Comandos úteis
├── FILE_SUMMARY.md             📑 Resumo de ficheiros
├── PRESENTATION_GUIDE.md       🎤 Guia de apresentação
└── INDEX.md                    📚 Este ficheiro
```

### Configuração (`./`)
```
./
├── requirements.txt            📦 Dependências Python
├── .streamlit/config.toml      🎨 Configuração visual
├── run_app.sh                  🚀 Script de execução
└── test_app.py                 🧪 Validação automática
```

### Datasets (`datasets/`)
```
datasets/
├── easy/1,2,3/                 📊 Datasets simples (4-5 pacientes)
├── medium/4,5,6,7/             📊 Datasets médios (10-15 pacientes)
└── hard/8,9,10/                📊 Datasets complexos (>20 pacientes)
```

---

## 🎯 Guias Rápidos por Tarefa

### "Quero usar o sistema agora"
1. `pip install -r requirements.txt`
2. `streamlit run src/app.py`
3. Abrir http://localhost:8501
4. Selecionar dataset → Calcular → Ver resultados

**Docs**: [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)

---

### "Quero entender como funciona"
1. Ler [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) (5 min)
2. Ler [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md) (15 min)
3. Explorar [src/app.py](src/app.py) (20 min)

**Total**: ~40 minutos para compreensão completa

---

### "Quero modificar o código"
1. Estudar [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md) - Arquitetura
2. Ler [src/app.py](src/app.py) - Código principal (bem comentado)
3. Ver [QUICK_COMMANDS.md](QUICK_COMMANDS.md) - Debug

**Pontos de extensão**:
- `create_graph_visualization()` - Melhorar grafo
- `calculate_optimal_route()` - Novos algoritmos
- Adicionar tabs na interface - Novas visualizações

---

### "Preciso apresentar no hackathon"
1. **Ler completamente**: [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)
2. **Praticar fluxo**: 3x o script de 5 minutos
3. **Preparar sistema**: 
   - `streamlit cache clear`
   - `python3 test_app.py`
   - `streamlit run src/app.py`
4. **Testar demo**: Easy 1 → Hard 10 → Override

**Tempo de preparação**: 30-45 minutos

---

### "Quero validar a instalação"
```bash
python3 test_app.py
```

Esperado:
```
✅ TODOS OS TESTES PASSARAM!
```

**Se falhar**: Ver troubleshooting em [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)

---

### "Preciso de um comando específico"
**Consultar**: [QUICK_COMMANDS.md](QUICK_COMMANDS.md)

Exemplos:
- Executar app: `streamlit run src/app.py`
- Limpar cache: `streamlit cache clear`
- Testar: `python3 test_app.py`
- Exportar: Usar botão na interface

---

## 📊 Mapa de Conteúdo por Tópico

### Instalação
- [README.md](README.md) - Seção "Início Rápido"
- [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - Seção "Instalação"
- [QUICK_COMMANDS.md](QUICK_COMMANDS.md) - "Instalação e Configuração"

### Uso da Interface
- [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - ⭐ Guia completo
- [README.md](README.md) - Visão geral
- [QUICK_COMMANDS.md](QUICK_COMMANDS.md) - Comandos de execução

### Algoritmos
- [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - Resumo executivo
- [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md) - Detalhes técnicos
- [README.md](README.md) - Seção "Algoritmos"

### Visualização
- [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - Legenda do grafo
- [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md) - Implementação

### Performance
- [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - Métricas principais
- [README.md](README.md) - Tabela de performance
- [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md) - Otimizações

### Troubleshooting
- [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - Seção "Troubleshooting"
- [QUICK_COMMANDS.md](QUICK_COMMANDS.md) - "Debug e Troubleshooting"
- [FILE_SUMMARY.md](FILE_SUMMARY.md) - Seção "Contato e Suporte"

### Apresentação
- [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) - ⭐ Guia completo
- [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - Dados para slides
- [README.md](README.md) - Visão geral do projeto

---

## 🔍 Busca Rápida

### Por Palavra-Chave

**"Instalação"** → [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md), [QUICK_COMMANDS.md](QUICK_COMMANDS.md)

**"Algoritmo DP"** → [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md), [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md)

**"Visualização"** → [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md), [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md)

**"Performance"** → [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md), [README.md](README.md)

**"Comandos"** → [QUICK_COMMANDS.md](QUICK_COMMANDS.md)

**"Apresentação"** → [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)

**"Código"** → [src/app.py](src/app.py), [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md)

**"Datasets"** → [README.md](README.md), [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)

---

## 📈 Roadmap de Leitura Recomendado

### Iniciante (Primeira Vez)
1. [README.md](README.md) - 5 min
2. Instalar: `pip install -r requirements.txt`
3. Testar: `python3 test_app.py`
4. Executar: `streamlit run src/app.py`
5. [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - 10 min
6. Experimentar interface

**Tempo total**: 30 minutos → Usuário funcional

---

### Intermediário (Quer Entender)
1. Completar roadmap "Iniciante" ↑
2. [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - 5 min
3. [STREAMLIT_TECHNICAL.md](STREAMLIT_TECHNICAL.md) - 15 min
4. Explorar [src/app.py](src/app.py) - 20 min
5. Testar modificações pequenas

**Tempo total**: 1 hora → Compreensão profunda

---

### Avançado (Vai Apresentar/Modificar)
1. Completar roadmap "Intermediário" ↑
2. [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) - 10 min
3. [FILE_SUMMARY.md](FILE_SUMMARY.md) - 8 min
4. [QUICK_COMMANDS.md](QUICK_COMMANDS.md) - 5 min
5. Praticar apresentação 3x
6. Implementar feature nova (opcional)

**Tempo total**: 2-3 horas → Expert completo

---

## ✅ Verificação de Conhecimento

### Após ler documentação, você deve saber:

**Nível Básico**:
- [ ] Como instalar dependências
- [ ] Como executar a aplicação
- [ ] Como selecionar um dataset
- [ ] Como calcular uma rota
- [ ] Como interpretar resultados

**Nível Intermediário**:
- [ ] Diferença entre DP e Heurística
- [ ] Quando cada algoritmo é usado
- [ ] Como funciona a visualização do grafo
- [ ] Como exportar resultados
- [ ] Como fazer override de parâmetros

**Nível Avançado**:
- [ ] Arquitetura do código (componentes)
- [ ] Fluxo de dados (CSV → Graph → Resultado)
- [ ] Pontos de extensão no código
- [ ] Como debugar problemas
- [ ] Como apresentar o projeto

---

## 🎯 Objetivos por Perfil

### Usuário Final
**Meta**: Usar a interface para otimizar rotas  
**Docs**: README.md + STREAMLIT_GUIDE.md  
**Tempo**: 15 minutos

### Desenvolvedor
**Meta**: Entender arquitetura e modificar código  
**Docs**: STREAMLIT_TECHNICAL.md + src/app.py  
**Tempo**: 1 hora

### Gestor
**Meta**: Avaliar viabilidade e impacto  
**Docs**: EXECUTIVE_SUMMARY.md  
**Tempo**: 5 minutos

### Apresentador
**Meta**: Apresentar com confiança no hackathon  
**Docs**: PRESENTATION_GUIDE.md + prática  
**Tempo**: 1 hora (prep + ensaio)

---

## 📞 Ajuda Adicional

### Não encontrou o que procura?

1. **Usar busca**: Ctrl+F nos documentos
2. **Consultar índice**: Este ficheiro
3. **Ler FAQ**: [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md) seção "FAQ"
4. **Testar código**: `python3 test_app.py`
5. **Ver exemplos**: Executar aplicação e experimentar

### Ainda com dúvidas?

**Documentação técnica completa**: 6 ficheiros MD + código comentado  
**Total de documentação**: ~1500 linhas  
**Cobertura**: 100% das funcionalidades

---

## 🎉 Conclusão

Este índice organiza toda a documentação do projeto Lapers.  
Escolha o roadmap adequado ao seu perfil e objetivo.

**Documentação completa. Sistema pronto. Vamos começar! 🚀**

---

**Última atualização**: Outubro 2025  
**Status**: ✅ Documentação completa
