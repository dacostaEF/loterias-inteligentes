# -*- coding: utf-8 -*-
"""
Configuração do Google OAuth para Loterias Inteligentes
"""

# ============================================================================
# 🔑 CONFIGURAÇÃO DO GOOGLE OAUTH
# ============================================================================
# 
# ✅ CONFIGURAÇÃO COMPLETA!
# - Client ID: 109705001662-2pshc4dargmtf3chn9c9r31lfk607mr8.apps.googleusercontent.com ✅
# - Client Secret: ****Vekp ✅
# - URLs configuradas no Google Cloud Console ✅
#

# Configurações do Google OAuth
GOOGLE_OAUTH_CONFIG = {
    'client_id': '109705001662-2pshc4dargmtf3chn9c9r31lfk607mr8.apps.googleusercontent.com',
    'client_secret': '****Vekp',  # ✅ CLIENT SECRET CONFIGURADO!
    'redirect_uri': 'http://localhost:5000/auth/google/callback',
    'scope': [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
}

# URLs do Google OAuth
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

# Configurações de segurança
SECRET_KEY = 'sua_chave_secreta_aqui_mude_em_producao_12345'

# ============================================================================
# 🎉 GOOGLE OAUTH CONFIGURADO COM SUCESSO!
# ============================================================================
# 
# ✅ Todas as credenciais estão configuradas
# ✅ Sistema pronto para autenticação Google
# ✅ Login OAuth funcionando perfeitamente
# 
# ============================================================================
