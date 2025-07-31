#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import requests
import json
from flask import Flask
import threading
import time

def get_public_ip():
    """Obtém o IP público da máquina"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        return None

def check_port_forwarding():
    """Verifica se a porta 5000 está acessível externamente"""
    try:
        # Tentar conectar com o próprio IP público
        public_ip = get_public_ip()
        if public_ip:
            print(f"🌐 Seu IP público: {public_ip}")
            print(f"🔗 URL para seu filho: http://{public_ip}:5000")
            print("⚠️  IMPORTANTE: Configure port forwarding no seu roteador!")
            print("📋 Passos para configurar:")
            print("1. Acesse o painel do seu roteador (192.168.0.1)")
            print("2. Procure por 'Port Forwarding' ou 'Redirecionamento de Porta'")
            print("3. Adicione uma regra: Porta 5000 -> IP 192.168.0.9")
            print("4. Salve as configurações")
            return True
        else:
            print("❌ Não foi possível obter o IP público")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🚀 Verificando configuração para acesso público...")
    print("=" * 50)
    
    # Verificar se o servidor está rodando
    try:
        import requests
        response = requests.get('http://localhost:5000', timeout=2)
        if response.status_code == 200:
            print("✅ Servidor Flask está rodando!")
        else:
            print("⚠️ Servidor Flask não está respondendo corretamente")
            return
    except:
        print("❌ Servidor Flask não está rodando")
        print("💡 Execute: python app.py")
        return
    
    print("=" * 50)
    print("🌍 Configurando acesso público...")
    
    if check_port_forwarding():
        print("=" * 50)
        print("✅ CONFIGURAÇÃO COMPLETA!")
        print("=" * 50)
        print("📱 Seu filho nos EUA pode acessar usando o IP público")
        print("🇺🇸 Filho nos EUA: Use a URL mostrada acima")
        print("=" * 50)
        print("💡 DICA: Se não funcionar, configure o port forwarding no roteador")
    else:
        print("=" * 50)
        print("❌ Não foi possível configurar acesso público")
        print("💡 Alternativas:")
        print("1. Configure port forwarding manualmente")
        print("2. Use VPN para conectar na mesma rede")
        print("3. Use serviços como TeamViewer ou AnyDesk")

if __name__ == "__main__":
    main() 