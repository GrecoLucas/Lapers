# 🚑 LAPERS - Guia Rápido de 1 Minuto

## 🎯 O Que É?
Sistema web de otimização de rotas de ambulância que maximiza prioridade de atendimentos.

## ⚡ Começar AGORA (3 comandos)
```bash
pip install -r requirements.txt
python3 test_app.py
streamlit run src/app.py
```
**Acesse**: http://localhost:8501

## 📁 Ficheiros Principais
- `src/app.py` - Interface Streamlit (660 linhas) ⭐
- `README.md` - Visão geral completa
- `PRESENTATION_GUIDE.md` - Script de apresentação

## 🎓 Algoritmos
- **DP Ótimo** (≤20 pacientes) - Solução perfeita
- **Heurística** (>20 pacientes) - Rápida e eficiente
- **Dijkstra** - Caminhos mais curtos

## 📊 Performance
- Carregamento: <1s
- Cálculo: <5s
- Total: <5s ✅

## 🎯 Demo (2 min)
1. Selecionar "Easy 1"
2. Clicar "Calcular"
3. Ver grafo + métricas
4. [Opcional] Testar "Hard 10"

## 📚 Documentação (escolha 1)
- **Usuários** → STREAMLIT_GUIDE.md
- **Desenvolvedores** → STREAMLIT_TECHNICAL.md
- **Gestores** → EXECUTIVE_SUMMARY.md
- **Apresentadores** → PRESENTATION_GUIDE.md

## ✅ Verificar
```bash
./verify_system.sh
```

## 🏆 Destaques
- ✅ 10 datasets suportados
- ✅ Interface zero-config
- ✅ Visualização profissional
- ✅ Performance <5s
- ✅ 2166 linhas de documentação

## 🆘 Ajuda Rápida
**Problema**: Dependências faltando  
**Solução**: `pip install -r requirements.txt`

**Problema**: Erro ao executar  
**Solução**: `python3 test_app.py` (diagnóstico)

**Problema**: Cache desatualizado  
**Solução**: `streamlit cache clear`

## 📞 Mais Informações
Ver INDEX.md para índice completo de documentação.

---

**Status**: ✅ PRONTO  
**Comando**: `streamlit run src/app.py`  
**GO!** 🚀
