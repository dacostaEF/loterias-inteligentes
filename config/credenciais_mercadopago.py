#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Credenciais do Mercado Pago - CONFIGURAÇÃO TEMPORÁRIA
"""

# ============================================================================
# 🔑 SUAS CREDENCIAIS DO MERCADO PAGO
# ============================================================================

# Credenciais de teste
MERCADOPAGO_ACCESS_TOKEN = "dev_24c65fb163bf11ea96500242ac130004"
MERCADOPAGO_PUBLIC_KEY = "dev_24c65fb163bf11ea96500242ac130004"

# Modo de operação (true = sandbox/teste, false = produção)
MERCADOPAGO_SANDBOX = True

# URLs de retorno
MERCADOPAGO_SUCCESS_URL = "http://localhost:5000/pagamento/sucesso"
MERCADOPAGO_FAILURE_URL = "http://localhost:5000/pagamento/cancelado"
MERCADOPAGO_PENDING_URL = "http://localhost:5000/pagamento/pendente"
MERCADOPAGO_WEBHOOK_URL = "http://localhost:5000/webhook/mercadopago"

# Configurações de notificação
SMS_CONFIRMATION_ENABLED = True
EMAIL_CONFIRMATION_ENABLED = True

# ============================================================================
# 📱 CONFIGURAÇÕES DE NOTIFICAÇÃO
# ============================================================================

# Twilio para SMS (já configurado)
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""

# SendGrid para Email (já configurado)
SENDGRID_API_KEY = ""
FROM_EMAIL = "dacosta_ef@hotmail.com"

# ============================================================================
# 🎯 CONFIGURAÇÕES DOS PLANOS
# ============================================================================

PLANOS_MERCADOPAGO = {
    'daily': {
        'nome': 'Plano Diário',
        'preco': 5.00,
        'descricao': 'Acesso diário às funcionalidades premium',
        'duracao_dias': 1
    },
    'monthly': {
        'nome': 'Plano Mensal',
        'preco': 29.90,
        'descricao': 'Acesso mensal às funcionalidades premium',
        'duracao_dias': 30
    },
    'semiannual': {
        'nome': 'Plano Semestral',
        'preco': 149.90,
        'descricao': 'Acesso semestral às funcionalidades premium',
        'duracao_dias': 180
    },
    'annual': {
        'nome': 'Plano Anual',
        'preco': 269.90,
        'descricao': 'Acesso anual às funcionalidades premium',
        'duracao_dias': 365
    },
    'lifetime': {
        'nome': 'Plano Vitalício',
        'preco': 997.00,
        'descricao': 'Acesso vitalício às funcionalidades premium',
        'duracao_dias': 9999  # Vitalício
    }
}

# ============================================================================
# 🔍 VALIDAÇÃO DAS CONFIGURAÇÕES
# ============================================================================

def validar_configuracao():
    """Valida se as configurações estão corretas."""
    erros = []
    
    if not MERCADOPAGO_ACCESS_TOKEN:
        erros.append("MERCADOPAGO_ACCESS_TOKEN não configurado")
    
    if not MERCADOPAGO_PUBLIC_KEY:
        erros.append("MERCADOPAGO_PUBLIC_KEY não configurado")
    
    if SMS_CONFIRMATION_ENABLED and not TWILIO_ACCOUNT_SID:
        erros.append("TWILIO_ACCOUNT_SID não configurado para SMS")
    
    if EMAIL_CONFIRMATION_ENABLED and not SENDGRID_API_KEY:
        erros.append("SENDGRID_API_KEY não configurado para Email")
    
    return erros

# ============================================================================
# 📊 INFORMAÇÕES DE DEBUG
# ============================================================================

def get_config_info():
    """Retorna informações da configuração para debug."""
    return {
        'sandbox_mode': MERCADOPAGO_SANDBOX,
        'has_access_token': bool(MERCADOPAGO_ACCESS_TOKEN),
        'has_public_key': bool(MERCADOPAGO_PUBLIC_KEY),
        'sms_enabled': SMS_CONFIRMATION_ENABLED,
        'email_enabled': EMAIL_CONFIRMATION_ENABLED,
        'webhook_url': MERCADOPAGO_WEBHOOK_URL
    }

if __name__ == "__main__":
    print("🔧 Configuração do Mercado Pago")
    print("=" * 50)
    
    erros = validar_configuracao()
    if erros:
        print("❌ Erros encontrados:")
        for erro in erros:
            print(f"   - {erro}")
    else:
        print("✅ Configuração válida!")
    
    print("\n📊 Informações da configuração:")
    info = get_config_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
