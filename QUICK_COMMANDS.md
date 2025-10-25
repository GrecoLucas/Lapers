# 🚑 Comandos Rápidos - Streamlit App

## Instalação e Configuração

### Instalar Dependências
```bash
pip install -r requirements.txt
```

### Verificar Instalação
```bash
python3 test_app.py
```

## Execução

### Método 1: Streamlit direto
```bash
streamlit run src/app.py
```

### Método 2: Script shell
```bash
./run_app.sh
```

### Método 3: Com ambiente virtual explícito
```bash
source .venv/bin/activate
streamlit run src/app.py
```

## Durante o Desenvolvimento

### Limpar cache do Streamlit
```bash
streamlit cache clear
```

### Ver logs detalhados
```bash
streamlit run src/app.py --logger.level=debug
```

### Executar em porta diferente
```bash
streamlit run src/app.py --server.port=8502
```

### Desabilitar auto-reload (economia de recursos)
```bash
streamlit run src/app.py --server.fileWatcherType=none
```

## Verificações de Qualidade

### Verificar sintaxe Python
```bash
python3 -m py_compile src/app.py
```

### Listar imports
```bash
grep -E "^import |^from " src/app.py
```

### Contar linhas de código
```bash
wc -l src/app.py
```

## Testes de Datasets

### Testar dataset Easy 1
```bash
# Verificar arquivos
ls -lh datasets/easy/1/

# Ver conteúdo
head datasets/easy/1/*.csv
```

### Verificar todos os datasets
```bash
for level in easy medium hard; do
    for dir in datasets/$level/*/; do
        echo "Verificando $dir"
        ls $dir
    done
done
```

## Exportação e Compartilhamento

### Criar ZIP do projeto (sem venv)
```bash
zip -r lapers_app.zip . -x "*.venv/*" "*__pycache__/*" "*.git/*"
```

### Gerar requirements.txt atualizado
```bash
pip freeze > requirements.txt
```

### Criar screenshot da aplicação (usando navegador)
```bash
# 1. Abrir aplicação
streamlit run src/app.py

# 2. No navegador: F12 → Console
# 3. Executar:
# window.print()
```

## Debug e Troubleshooting

### Ver versões das bibliotecas
```bash
python3 -c "
import streamlit
import pandas
import matplotlib
import networkx
print(f'Streamlit: {streamlit.__version__}')
print(f'Pandas: {pandas.__version__}')
print(f'Matplotlib: {matplotlib.__version__}')
print(f'NetworkX: {networkx.__version__}')
"
```

### Verificar uso de memória
```bash
# Durante execução, em outro terminal:
ps aux | grep streamlit
```

### Matar processo do Streamlit
```bash
# Se travar
pkill -f streamlit
```

### Reiniciar com cache limpo
```bash
streamlit cache clear && streamlit run src/app.py
```

## Customização

### Alterar tema (editar .streamlit/config.toml)
```toml
[theme]
primaryColor = "#dc143c"      # Vermelho emergência
backgroundColor = "#ffffff"     # Branco
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Desabilitar menu do Streamlit
```python
# Adicionar em app.py:
st.set_page_config(
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Sistema de Otimização de Rotas v1.0"
    }
)
```

## Performance

### Profiling de performance
```bash
python3 -m cProfile -s cumtime test_app.py
```

### Verificar tamanho de cache
```bash
du -sh ~/.streamlit/cache
```

## Produção

### Executar em background (produção)
```bash
nohup streamlit run src/app.py &
```

### Ver logs em tempo real
```bash
tail -f nohup.out
```

### Parar aplicação em background
```bash
ps aux | grep streamlit
kill <PID>
```

## Apresentação no Hackathon

### Preparação (5 min antes)
```bash
# 1. Limpar cache
streamlit cache clear

# 2. Testar dataset exemplo
python3 test_app.py

# 3. Iniciar aplicação
streamlit run src/app.py

# 4. Abrir navegador em http://localhost:8501
```

### Fluxo de Demo (2 min)
```
1. Mostrar seleção de dataset (Easy 1)
2. Mostrar preview automático
3. Clicar "Calcular Rota Ótima"
4. Explicar métricas (30s)
5. Mostrar grafo (30s)
6. Mostrar tabela detalhada (30s)
7.Mostrar Funcionalidade Upload
8. [Opcional] Mudar para Hard 10
9. [Opcional] Override de parâmetros
10. [Opcional] Exportar CSV
```

### Pontos de Destaque
- ✅ "Interface zero-config, funciona imediatamente"
- ✅ "Algoritmo adaptativo: DP para pequenos, Heurística para grandes"
- ✅ "Visualização profissional do grafo com rota destacada"
- ✅ "Performance <5s para qualquer dataset"

## Comandos Git (se aplicável)

### Commit das mudanças
```bash
git add src/app.py requirements.txt .streamlit/
git commit -m "feat: Add Streamlit interface with graph visualization"
```

### Ver diferenças
```bash
git diff src/app.py
```

## Atalhos Úteis

### Recarregar página do Streamlit
- Navegador: `R` ou `Ctrl+R`
- Streamlit: Detecta mudanças automaticamente

### Parar execução
- Terminal: `Ctrl+C`

### Fullscreen do grafo
- Clicar no ícone de expansão no canto da figura

---

## 🎯 Comando Final para Hackathon

```bash
# Setup completo em 1 linha:
pip install -r requirements.txt && python3 test_app.py && streamlit run src/app.py
```

**Tempo total**: ~30 segundos
**Status**: ✅ PRONTO!
