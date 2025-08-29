# 🗄️ Banco de Dados - Sistema de Loterias (SIMPLIFICADO)

## 📋 Visão Geral

Este diretório contém a estrutura **SIMPLIFICADA** para criar e gerenciar o banco de dados SQLite do sistema de loterias.

## 🚀 Como Usar

### 1. **Instalar Dependências**
```bash
pip install bcrypt
```

### 2. **Criar o Banco de Dados**
```bash
cd database
python create_database_simples.py
```

## 🏗️ Estrutura do Banco (SIMPLIFICADA)

### **Tabela: `usuarios`**
- **id**: Chave primária
- **nome_completo**: Nome completo do usuário
- **data_nascimento**: Data de nascimento
- **cpf**: CPF único
- **telefone_celular**: Telefone para contato
- **email**: Email único (usado para login)
- **senha_hash**: Senha criptografada com bcrypt
- **data_cadastro**: Data de criação da conta
- **status**: ativo/bloqueado
- **receber_emails**: Se aceita receber emails
- **receber_sms**: Se aceita receber SMS
- **aceitou_termos**: Se aceitou os termos de uso

### **Tabela: `planos`**
- **id**: Chave primária
- **nome**: Nome do plano (Free, Mensal, etc.)
- **valor**: Preço em reais
- **duracao_dias**: Duração em dias
- **descricao**: Descrição do plano

### **Tabela: `assinaturas`**
- **id**: Chave primária
- **usuario_id**: Referência ao usuário
- **plano_id**: Referência ao plano
- **data_inicio**: Data de início da assinatura
- **data_expiracao**: Data de expiração
- **status**: pendente/ativa/expirada
- **valor_pago**: Valor efetivamente pago
- **metodo_pagamento**: PIX/cartão/boleto
- **id_transacao**: ID da transação no gateway

## 💎 Planos Disponíveis

### **🆓 Free (Gratuito)**
- Acesso a 3 loterias: +Milionária, Quina, Lotomania
- Dashboard básico

### **💰 Mensal - R$ 19,90**
- Acesso completo por 30 dias
- Todas as loterias e funcionalidades

### **💰 Semestral - R$ 99,90**
- Acesso completo por 180 dias
- Todas as loterias e funcionalidades

### **💰 Anual - R$ 179,90**
- Acesso completo por 365 dias
- Todas as loterias e funcionalidades

### **💰 Vitalício - R$ 499,90**
- Acesso completo para sempre
- Todas as loterias e funcionalidades

## 🔧 Funcionalidades

### **Criptografia de Senhas**
- Todas as senhas são criptografadas com bcrypt
- Hash único para cada usuário
- Segurança máxima para dados sensíveis

### **Controle de Acesso**
- Verificação automática de assinaturas
- Bloqueio de rotas premium
- Sistema de níveis baseado em planos

## 📁 Arquivos

- **`create_database_simples.py`**: Script para criar o banco e tabelas
- **`README.md`**: Esta documentação

## 🧪 Usuário de Teste

Após executar `create_database_simples.py`, será criado um usuário de teste:
- **Email**: teste@loterias.com
- **Senha**: 123456
- **Nível**: Free

## 🚨 Importante

- **Backup**: Sempre faça backup do arquivo `loterias_simples.db`
- **Produção**: Em produção, migre para PostgreSQL/MySQL
- **Segurança**: Nunca commite senhas ou chaves no Git
- **Testes**: Use sempre o usuário de teste para desenvolvimento

## 🔄 Próximos Passos

1. ✅ Banco de dados criado
2. 🔧 Integrar com app.py
3. 🧪 Testar cadastro e login de usuários
4. 💳 Implementar sistema de pagamento
5. 🚀 Deploy para testes
