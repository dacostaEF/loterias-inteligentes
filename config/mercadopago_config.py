#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração do Mercado Pago
"""

import os
# from dotenv import load_dotenv  # Comentado pois não temos essa dependência

# Carregar variáveis de ambiente
# load_dotenv()  # Comentado pois não temos essa dependência

# ============================================================================
# 🔑 CONFIGURAÇÕES MERCADO PAGO
# ============================================================================

# Credenciais do Mercado Pago
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN', 'TEST-12345678901234567890123456789012-12345678-abcdefgh-12345678-abcdefgh')
MERCADOPAGO_PUBLIC_KEY = os.getenv('MERCADOPAGO_PUBLIC_KEY', 'TEST-12345678901234567890123456789012-12345678-abcdefgh-12345678-abcdefgh')

# Modo de operação (sandbox para testes, production para produção)
MERCADOPAGO_SANDBOX = os.getenv('MERCADOPAGO_SANDBOX', 'true').lower() == 'true'

# URLs de retorno
MERCADOPAGO_SUCCESS_URL = os.getenv('MERCADOPAGO_SUCCESS_URL', 'http://localhost:5000/pagamento/sucesso')
MERCADOPAGO_FAILURE_URL = os.getenv('MERCADOPAGO_FAILURE_URL', 'http://localhost:5000/pagamento/cancelado')
MERCADOPAGO_PENDING_URL = os.getenv('MERCADOPAGO_PENDING_URL', 'http://localhost:5000/pagamento/pendente')

# Webhook URL (para notificações automáticas)
MERCADOPAGO_WEBHOOK_URL = os.getenv('MERCADOPAGO_WEBHOOK_URL', 'http://localhost:5000/webhook/mercadopago')

# Configurações de notificação
SMS_CONFIRMATION_ENABLED = os.getenv('SMS_CONFIRMATION_ENABLED', 'true').lower() == 'true'
EMAIL_CONFIRMATION_ENABLED = os.getenv('EMAIL_CONFIRMATION_ENABLED', 'true').lower() == 'true'

# ============================================================================
# 📱 CONFIGURAÇÕES DE NOTIFICAÇÃO
# ============================================================================

# Twilio para SMS (já configurado)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')

# SendGrid para Email (já configurado)
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'dacosta_ef@hotmail.com')

# ============================================================================
# 🎯 CONFIGURAÇÕES DOS PLANOS
# ============================================================================

# 🔐 CONTROLE DE ACESSO POR PLANO
ACESSO_POR_PLANO = {
    'Free': {
        'loterias': [],  # Usuário free não acessa bolões
        'limite_apostas': 0,
        'nome_display': 'Gratuito'
    },
    'daily': {
        'loterias': ['quina'],  # Acesso apenas à Quina
        'limite_apostas': 5,
        'nome_display': 'Diário'
    },
    'monthly': {
        'loterias': ['quina', 'lotofacil'],  # Acesso à Quina e Lotofácil
        'limite_apostas': 20,
        'nome_display': 'Mensal'
    },
    'semiannual': {
        'loterias': ['quina', 'lotofacil', 'megasena'],  # Sem Milionária
        'limite_apostas': 50,
        'nome_display': 'Semestral'
    },
    'annual': {
        'loterias': ['quina', 'lotofacil', 'megasena', 'milionaria'],  # Todas
        'limite_apostas': 100,
        'nome_display': 'Anual'
    },
    'lifetime': {
        'loterias': ['quina', 'lotofacil', 'megasena', 'milionaria'],  # Todas + benefícios
        'limite_apostas': -1,  # Ilimitado
        'nome_display': 'Vitalício'
    }
}

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
# 💳 CONFIGURAÇÕES DE PAGAMENTO
# ============================================================================

# Métodos de pagamento disponíveis
METODOS_PAGAMENTO = {
    'pix': {
        'nome': 'PIX',
        'descricao': 'Pagamento instantâneo via PIX',
        'icone': '🏦',
        'aprovacao': 'instantanea',
        'taxa': 0.0  # Sem taxa para o comprador
    },
    'cartao_credito': {
        'nome': 'Cartão de Crédito',
        'descricao': 'Visa, Mastercard, Elo, American Express',
        'icone': '💳',
        'aprovacao': 'imediata',
        'parcelamento': True,
        'max_parcelas': 12
    },
    'cartao_debito': {
        'nome': 'Cartão de Débito',
        'descricao': 'Débito direto na conta',
        'icone': '💳',
        'aprovacao': 'imediata',
        'parcelamento': False
    },
    'boleto': {
        'nome': 'Boleto Bancário',
        'descricao': 'Pagamento em qualquer banco',
        'icone': '📄',
        'aprovacao': '3_dias_uteis',
        'vencimento': 3
    }
}

# Configurações de parcelamento
CONFIGURACAO_PARCELAMENTO = {
    'minimo_parcela': 5.00,  # Valor mínimo por parcela
    'max_parcelas': 12,      # Máximo de parcelas
    'juros_parcelamento': 0.0,  # Juros para parcelamento (0% = sem juros)
    'parcelas_sem_juros': 3   # Primeiras X parcelas sem juros
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

# ============================================================================
# 🔐 FUNÇÕES DE CONTROLE DE ACESSO
# ============================================================================

def verificar_acesso_loteria(plano_usuario, loteria):
    """Verifica se o usuário tem acesso a uma loteria específica."""
    if not plano_usuario:
        plano_usuario = 'Free'
    
    permissoes = ACESSO_POR_PLANO.get(plano_usuario, ACESSO_POR_PLANO['Free'])
    return loteria in permissoes['loterias']

def get_loterias_permitidas(plano_usuario):
    """Retorna a lista de loterias que o usuário pode acessar."""
    if not plano_usuario:
        plano_usuario = 'Free'
    
    permissoes = ACESSO_POR_PLANO.get(plano_usuario, ACESSO_POR_PLANO['Free'])
    return permissoes['loterias']

def get_loterias_bloqueadas(plano_usuario):
    """Retorna a lista de loterias que o usuário NÃO pode acessar."""
    todas_loterias = ['quina', 'lotofacil', 'megasena', 'milionaria']
    permitidas = get_loterias_permitidas(plano_usuario)
    return [lot for lot in todas_loterias if lot not in permitidas]

def get_proximo_plano_para_loteria(loteria, plano_atual='Free'):
    """Retorna o próximo plano que dá acesso a uma loteria específica."""
    planos_ordem = ['daily', 'monthly', 'semiannual', 'annual', 'lifetime']
    
    for plano in planos_ordem:
        if verificar_acesso_loteria(plano, loteria):
            return plano
    
    return 'annual'  # Fallback para plano que tem tudo

def get_info_upgrade_loteria(loteria, plano_atual='Free'):
    """Retorna informações sobre upgrade necessário para acessar uma loteria."""
    if verificar_acesso_loteria(plano_atual, loteria):
        return None  # Já tem acesso
    
    proximo_plano = get_proximo_plano_para_loteria(loteria, plano_atual)
    
    return {
        'loteria': loteria,
        'plano_atual': plano_atual,
        'plano_necessario': proximo_plano,
        'info_plano': PLANOS_MERCADOPAGO.get(proximo_plano, {}),
        'acesso_plano': ACESSO_POR_PLANO.get(proximo_plano, {})
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
    
    print("\n🔐 Teste de Acesso por Plano:")
    for plano in ['Free', 'daily', 'monthly', 'annual']:
        print(f"\n   {plano}: {get_loterias_permitidas(plano)}")
        for loteria in ['quina', 'lotofacil', 'megasena', 'milionaria']:
            acesso = "✅" if verificar_acesso_loteria(plano, loteria) else "❌"
            print(f"     {loteria}: {acesso}")
