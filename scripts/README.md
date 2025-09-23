# Scripts do Sistema

Esta pasta contém scripts utilitários para gerenciamento e manutenção do sistema.

## Estrutura

### `diagnostico/`
Scripts de diagnóstico do sistema:
- `lotofacil_distribuicao.py` - Análise de distribuição Lotofácil
- `lotofacil_estatisticas_avancadas.py` - Estatísticas avançadas Lotofácil

### `limpar_dados_DB.py`
Script para limpeza e reset do banco de dados, mantendo apenas os usuários master essenciais.

## Como usar

```bash
# Limpar banco de dados
python scripts/limpar_dados_DB.py

# Executar diagnósticos
python scripts/diagnostico/lotofacil_distribuicao.py
python scripts/diagnostico/lotofacil_estatisticas_avancadas.py
```


