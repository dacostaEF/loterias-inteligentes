# Scripts do Sistema

Esta pasta contém scripts utilitários para gerenciamento e manutenção do sistema.

## Estrutura

### `teste/`
Scripts de teste e verificação:
- `verificar_usuarios_master.py` - Verifica usuários master no banco
- `verificar_usuarios.py` - Verifica usuários gerais
- `gerenciar_usuarios_confianca.py` - Gerenciamento de usuários de confiança
- `teste_pix.py` - Teste de integração PIX

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

# Verificar usuários master
python scripts/teste/verificar_usuarios_master.py
```
