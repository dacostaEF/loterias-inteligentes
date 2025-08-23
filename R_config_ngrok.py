#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyngrok import ngrok
import os

def configurar_ngrok():
    print("🔧 Configurando authtoken do Ngrok...")
    authtoken = "30WTs8FbpWImuKyuTRXcTMQfXhD_2Hiv2hbJKTaeMBqamDt4e"
    ngrok.set_auth_token(authtoken)
    print("✅ Authtoken configurado com sucesso!")
    print("🚀 Agora você pode usar o ngrok_deploy.py")
    try:
        print("🧪 Testando conexão...")
        tunnels = ngrok.get_ngrok_process().api_url
        print("✅ Conexão testada com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro no teste: {e}")

if __name__ == "__main__":
    configurar_ngrok() 