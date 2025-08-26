#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import socket

def get_local_ip():
    try:
        # Conectar a um endereço externo para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def main():
    PORT = 8080
    local_ip = get_local_ip()
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print("🚀 Servidor de teste HTTP iniciado!")
        print(f"🌐 IP Local: {local_ip}")
        print(f"🔗 URL Local: http://{local_ip}:{PORT}")
        print(f"🔗 URL Localhost: http://127.0.0.1:{PORT}")
        print(f"\n📱 Teste no celular: http://{local_ip}:{PORT}")
        print("⏹️  Pressione Ctrl+C para parar")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Parando servidor...")
            httpd.shutdown()
            print("✅ Servidor parado!")

if __name__ == "__main__":
    main()
