#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configurações de pagamento para Stripe e PagSeguro.
"""

# ============================================================================
# 💳 CONFIGURAÇÕES DE PAGAMENTO
# ============================================================================

# 🧪 MODO TESTE
MODO_TESTE = True

# ============================================================================
# 🌍 STRIPE (Pagamento Internacional)
# ============================================================================

# Chaves de teste do Stripe
STRIPE_PUBLIC_KEY = "pk_test_51ABC123..."  # Chave pública
STRIPE_SECRET_KEY = "sk_test_51ABC123..."  # Chave secreta

# Configurações do Stripe
STRIPE_CURRENCY = "brl"  # Real brasileiro
STRIPE_SUCCESS_URL = "http://localhost:5000/pagamento/sucesso"
STRIPE_CANCEL_URL = "http://localhost:5000/pagamento/cancelado"

# ============================================================================
# 🏦 PAGSEGURO (Pagamento Brasileiro)
# ============================================================================

# Configurações do PagSeguro
PAGSEGURO_EMAIL = "dacosta_ef@hotmail.com"
PAGSEGURO_TOKEN = "seu_token_pagseguro"
PAGSEGURO_SANDBOX = True  # Ambiente de teste

# URLs do PagSeguro
PAGSEGURO_SUCCESS_URL = "http://localhost:5000/pagamento/sucesso"
PAGSEGURO_CANCEL_URL = "http://localhost:5000/pagamento/cancelado"

# ============================================================================
# 💰 PLANOS E PREÇOS
# ============================================================================

PLANOS = {
    'daily': {
        'nome': 'Diário',
        'preco': 9.90,
        'periodo': 'dia',
        'stripe_price_id': 'price_daily_test',
        'pagseguro_id': 'daily_plan'
    },
    'monthly': {
        'nome': 'Mensal',
        'preco': 29.90,
        'periodo': 'mês',
        'stripe_price_id': 'price_monthly_test',
        'pagseguro_id': 'monthly_plan'
    },
    'semestral': {
        'nome': 'Semestral',
        'preco': 149.90,
        'periodo': '6 meses',
        'stripe_price_id': 'price_semestral_test',
        'pagseguro_id': 'semestral_plan'
    },
    'annual': {
        'nome': 'Anual',
        'preco': 299.90,
        'periodo': 'ano',
        'stripe_price_id': 'price_annual_test',
        'pagseguro_id': 'annual_plan'
    },
    'lifetime': {
        'nome': 'Vitalício',
        'preco': 999.90,
        'periodo': 'vitalício',
        'stripe_price_id': 'price_lifetime_test',
        'pagseguro_id': 'lifetime_plan'
    }
}

# ============================================================================
# 🧪 CONFIGURAÇÕES DE TESTE
# ============================================================================

# Cartões de teste do Stripe
CARTOES_TESTE = {
    'visa': '4242424242424242',
    'mastercard': '5555555555554444',
    'amex': '378282246310005',
    'declined': '4000000000000002'  # Cartão recusado
}

# Dados de teste
DADOS_TESTE = {
    'nome': 'João Silva',
    'email': 'teste@exemplo.com',
    'telefone': '21999999999',
    'cpf': '12345678901'
}

if __name__ == '__main__':
    print("💳 CONFIGURAÇÕES DE PAGAMENTO")
    print("=" * 40)
    print(f"🧪 Modo Teste: {MODO_TESTE}")
    print(f"🌍 Stripe: {'Ativo' if STRIPE_PUBLIC_KEY else 'Inativo'}")
    print(f"🏦 PagSeguro: {'Ativo' if PAGSEGURO_EMAIL else 'Inativo'}")
    print(f"💰 Planos: {len(PLANOS)} disponíveis")

