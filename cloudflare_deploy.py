#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
import sys
import re

def main():
    print("🚀 Iniciando deploy com Cloudflare Tunnel...")
    print("=" * 50)
    print("1. Verificando se o servidor Flask está rodando...")
    
    # Verificar se o servidor está rodando
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
        if '5000' not in result.stdout:
            print("⚠️ Servidor Flask não está rodando. Iniciando...")
            flask_process = subprocess.Popen([sys.executable, "app.py"],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
            time.sleep(3)
        else:
            print("✅ Servidor Flask já está rodando!")
    except Exception as e:
        print(f"❌ Erro ao verificar servidor: {e}")
        return
    
    print("2. Criando túnel público com Cloudflare...")
    print("=" * 50)
    
    try:
        # Executar cloudflared tunnel
        tunnel_process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', 'http://localhost:5000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("⏳ Aguardando criação do túnel...")
        time.sleep(5)
        
        # Tentar ler a saída para obter a URL
        output, error = tunnel_process.communicate(timeout=10)
        
        if tunnel_process.returncode == 0:
            # Procurar pela URL na saída
            url_match = re.search(r'https://[a-zA-Z0-9\-\.]+\.trycloudflare\.com', output)
            if url_match:
                public_url = url_match.group(0)
                print("✅ SITE PUBLICADO COM SUCESSO!")
                print("=" * 50)
                print(f"🌐 URL Pública: {public_url}")
                print("=" * 50)
                print("📱 Seu filho nos EUA pode acessar de qualquer lugar!")
                print("🇺🇸 Filho nos EUA: Acesse a URL acima")
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
                    print("\n🛑 Parando túnel...")
                    tunnel_process.terminate()
                    print("✅ Túnel parado!")
            else:
                print("❌ Não foi possível obter a URL do túnel")
                print("Saída:", output)
                print("Erro:", error)
        else:
            print("❌ Erro ao criar túnel")
            print("Erro:", error)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("💡 Alternativa: Use o IP local se estiver na mesma rede")
        print("🌐 URL Local: http://192.168.0.9:5000")

if __name__ == "__main__":
    main() 