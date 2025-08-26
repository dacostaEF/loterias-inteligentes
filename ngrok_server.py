#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyngrok import ngrok
import time
import os

def main():
    print("🚀 Iniciando ngrok para o Flask...")
    
    # Configurar ngrok (opcional - você pode criar conta gratuita em ngrok.com)
    # ngrok.set_auth_token("SEU_TOKEN_AQUI")  # Descomente se tiver token
    
    try:
        # Criar túnel para a porta 5000
        print("📡 Criando túnel público...")
        public_url = ngrok.connect(5000)
        
        print("✅ TÚNEL CRIADO COM SUCESSO!")
        print(f"🌐 URL PÚBLICA: {public_url}")
        print(f"🔗 Acesse de qualquer lugar: {public_url}")
        print("\n📱 Agora teste no seu celular usando a URL acima!")
        print("⏹️  Pressione Ctrl+C para parar o túnel")
        
        # Manter o túnel ativo
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Parando o túnel...")
        ngrok.kill()
        print("✅ Túnel parado!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Dica: Verifique se o Flask está rodando na porta 5000")

if __name__ == "__main__":
    main()
