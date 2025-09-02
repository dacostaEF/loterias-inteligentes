#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configurações de envio para SMS e Email.
"""

# ============================================================================
# 🔐 CONFIGURAÇÕES DE ENVIO - SMS E EMAIL
# ============================================================================

# 📱 TWILIO (SMS)
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"

# 📧 SENDGRID (EMAIL)
SENDGRID_API_KEY = "your_sendgrid_api_key"
SENDGRID_FROM_EMAIL = "dacosta_ef@hotmail.com"
SENDGRID_FROM_NAME = "Loterias Inteligentes"

# 📧 SMTP ALTERNATIVO (Gmail/Hotmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "dacosta_ef@hotmail.com"
SMTP_PASSWORD = "your_app_password"

# 🧪 MODO TESTE
MODO_TESTE = True

# 📱 NÚMEROS DE TESTE
NUMERO_TESTE_SMS = "21981651234"
EMAIL_TESTE = "dacosta_ef@hotmail.com"

