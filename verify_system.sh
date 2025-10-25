#!/bin/bash
# Script de verificação completa do sistema

echo "════════════════════════════════════════════════════════════"
echo "🚑 VERIFICAÇÃO COMPLETA DO SISTEMA LAPERS"
echo "════════════════════════════════════════════════════════════"
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de erros
ERRORS=0

# 1. Verificar estrutura de diretórios
echo "📁 Verificando estrutura de diretórios..."
REQUIRED_DIRS=("src" "datasets" "datasets/easy" "datasets/medium" "datasets/hard" ".streamlit")

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir"
    else
        echo -e "  ${RED}✗${NC} $dir (FALTANDO)"
        ERRORS=$((ERRORS+1))
    fi
done
echo ""

# 2. Verificar ficheiros principais
echo "📄 Verificando ficheiros principais..."
REQUIRED_FILES=(
    "src/app.py"
    "src/main.py"
    "src/node.py"
    "src/graph.py"
    "src/dijkstra.py"
    "src/dp.py"
    "requirements.txt"
    "run_app.sh"
    "test_app.py"
    ".streamlit/config.toml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(du -h "$file" | cut -f1)
        echo -e "  ${GREEN}✓${NC} $file ($SIZE)"
    else
        echo -e "  ${RED}✗${NC} $file (FALTANDO)"
        ERRORS=$((ERRORS+1))
    fi
done
echo ""

# 3. Verificar documentação
echo "📚 Verificando documentação..."
DOC_FILES=(
    "README.md"
    "STREAMLIT_GUIDE.md"
    "STREAMLIT_TECHNICAL.md"
    "EXECUTIVE_SUMMARY.md"
    "QUICK_COMMANDS.md"
    "FILE_SUMMARY.md"
    "PRESENTATION_GUIDE.md"
    "INDEX.md"
)

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(du -h "$file" | cut -f1)
        echo -e "  ${GREEN}✓${NC} $file ($SIZE)"
    else
        echo -e "  ${YELLOW}!${NC} $file (opcional)"
    fi
done
echo ""

# 4. Verificar datasets
echo "📊 Verificando datasets..."
DATASET_COUNT=0

for level in easy medium hard; do
    for dataset in datasets/$level/*/; do
        if [ -d "$dataset" ]; then
            DATASET_COUNT=$((DATASET_COUNT+1))
            # Verificar arquivos do dataset
            HAS_ALL=true
            for csv in "pontos.csv" "ruas.csv" "dados_iniciais.csv"; do
                if [ ! -f "$dataset$csv" ]; then
                    HAS_ALL=false
                fi
            done
            
            if [ "$HAS_ALL" = true ]; then
                echo -e "  ${GREEN}✓${NC} $dataset"
            else
                echo -e "  ${YELLOW}!${NC} $dataset (arquivos incompletos)"
            fi
        fi
    done
done

echo -e "  Total: $DATASET_COUNT datasets encontrados"
echo ""

# 5. Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "  ${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "  ${RED}✗${NC} Python3 não encontrado"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 6. Verificar dependências Python
echo "📦 Verificando dependências Python..."
DEPS=("streamlit" "pandas" "numpy" "matplotlib" "networkx")

for dep in "${DEPS[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        VERSION=$(python3 -c "import $dep; print($dep.__version__)" 2>/dev/null)
        echo -e "  ${GREEN}✓${NC} $dep $VERSION"
    else
        echo -e "  ${RED}✗${NC} $dep (NÃO INSTALADO)"
        ERRORS=$((ERRORS+1))
    fi
done
echo ""

# 7. Executar teste automatizado
echo "🧪 Executando testes automatizados..."
if python3 test_app.py > /tmp/lapers_test.log 2>&1; then
    echo -e "  ${GREEN}✓${NC} Todos os testes passaram!"
    # Mostrar resumo
    grep "✅" /tmp/lapers_test.log | head -3
else
    echo -e "  ${RED}✗${NC} Testes falharam. Ver /tmp/lapers_test.log para detalhes"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 8. Verificar permissões
echo "🔑 Verificando permissões..."
if [ -x "run_app.sh" ]; then
    echo -e "  ${GREEN}✓${NC} run_app.sh é executável"
else
    echo -e "  ${YELLOW}!${NC} run_app.sh não é executável (execute: chmod +x run_app.sh)"
fi
echo ""

# 9. Estatísticas
echo "📊 Estatísticas do projeto..."
echo "  Linhas de código (src/app.py): $(wc -l < src/app.py)"
echo "  Total de documentação: $(cat *.md 2>/dev/null | wc -l) linhas"
echo "  Ficheiros Python: $(find src -name "*.py" | wc -l)"
echo "  Datasets: $DATASET_COUNT"
echo ""

# 10. Resultado final
echo "════════════════════════════════════════════════════════════"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ SISTEMA COMPLETAMENTE FUNCIONAL!${NC}"
    echo ""
    echo "🚀 Para executar a aplicação:"
    echo "   streamlit run src/app.py"
    echo ""
    echo "   ou"
    echo ""
    echo "   ./run_app.sh"
else
    echo -e "${RED}⚠️  ENCONTRADOS $ERRORS PROBLEMAS${NC}"
    echo ""
    echo "Para corrigir:"
    echo "  1. Instalar dependências: pip install -r requirements.txt"
    echo "  2. Verificar estrutura de diretórios"
    echo "  3. Executar novamente: ./verify_system.sh"
fi
echo "════════════════════════════════════════════════════════════"
