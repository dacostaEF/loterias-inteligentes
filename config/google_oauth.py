# -*- coding: utf-8 -*-
"""
Configuração do Google OAuth para Loterias Inteligentes
"""

# Configurações do Google OAuth
GOOGLE_OAUTH_CONFIG = {
    'client_id': 'SEU_CLIENT_ID_AQUI',  # Substitua pelo seu Client ID do Google
    'client_secret': 'SEU_CLIENT_SECRET_AQUI',  # Substitua pelo seu Client Secret
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
SECRET_KEY = 'sua_chave_secreta_aqui_muito_segura_12345'  # Mude para uma chave segura em produção
