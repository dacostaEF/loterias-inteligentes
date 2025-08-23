#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyngrok import ngrok
import subprocess
import time
import sys

def main():
    print("🚀 Iniciando deploy temporário com Ngrok...")
    print("=" * 50)
    print("1. Iniciando servidor Flask...")
    flask_process = subprocess.Popen([sys.executable, "app.py"],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    time.sleep(3)
    print("2. Criando túnel público...")
    public_url = ngrok.connect(5000)
    print("=" * 50)
    print("✅ SITE PUBLICADO COM SUCESSO!")
    print("=" * 50)
    print(f"🌐 URL Pública: {public_url}")
    print("=" * 50)
    print("📱 Seus filhos podem acessar de qualquer lugar!")
    print("🇺🇸 Filho nos EUA: Acesse a URL acima")
    print("🇧🇷 Filho em São Paulo: Acesse a URL acima")
    print("=" * 50)
    print("⚠️  IMPORTANTE:")
    print("- Este túnel é temporário")
    print("- Funciona apenas enquanto este script estiver rodando")
    print("- Para parar: Ctrl+C")
    print("=" * 50)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Parando servidor...")
        ngrok.kill()
        flask_process.terminate()
        print("✅ Servidor parado!")

if __name__ == "__main__":
    main() 