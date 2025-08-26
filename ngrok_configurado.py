#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyngrok import ngrok
import time
import os

def main():
    print("🚀 Configurando ngrok com sua conta...")
    
    # Configurar autenticação (substitua pelo seu token real)
    # Vá para: https://dashboard.ngrok.com/get-started/your-authtoken
    AUTH_TOKEN = "30WTs8FbpWImuKyuTRXcTMQfXhD_2Hiv2hbJKTaeMBqamDt4e"
    
    try:
        # Configurar o token
        ngrok.set_auth_token(AUTH_TOKEN)
        print("✅ Token configurado com sucesso!")
        
        # Criar túnel para a porta 5000 (Flask)
        print("📡 Criando túnel público...")
        public_url = ngrok.connect(5000)
        
        print("✅ TÚNEL CRIADO COM SUCESSO!")
        print(f"🌐 URL PÚBLICA: {public_url}")
        print(f"🔗 Acesse de qualquer lugar: {public_url}")
        print(f"\n📱 Teste no celular: {public_url}")
        print("🌍 Teste de qualquer lugar do mundo!")
        print("⏹️  Pressione Ctrl+C para parar o túnel")
        
        # Manter o túnel ativo
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("\n💡 Para resolver:")
        print("1. Vá para: https://dashboard.ngrok.com/get-started/your-authtoken")
        print("2. Copie o token")
        print("3. Substitua 'SEU_TOKEN_AQUI' pelo token real")
        print("4. Execute novamente")

if __name__ == "__main__":
    main()
