#!/usr/bin/env python3
"""
Teste simples da API de bolões
"""

import requests
import json

def testar_api_local():
    """Testa a API local"""
    try:
        print("🔍 Testando API de bolões...")
        
        # URL local
        url = "http://localhost:5000/api/boloes/listar?loteria=quina"
        
        print(f"📡 Fazendo requisição para: {url}")
        
        response = requests.get(url, timeout=5)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Resposta recebida:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get('success') and data.get('boloes'):
                print(f"🎯 {len(data['boloes'])} bolões encontrados!")
                for bolao in data['boloes']:
                    print(f"  - {bolao.get('codigo')}: {bolao.get('nome')}")
            else:
                print("❌ Nenhum bolão na resposta")
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Não conseguiu conectar - servidor pode estar parado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    testar_api_local()
