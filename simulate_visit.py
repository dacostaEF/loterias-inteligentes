#!/usr/bin/env python3
# Script para simular uma visita real ao site

import requests
import time
import json

BASE_URL = "https://www.loteriasinteligente.com.br"

def simulate_real_visit():
    print("🌐 Simulando visita real ao site...")
    
    session = requests.Session()
    
    # Simular User-Agent real
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    try:
        # 1. Acessar a landing page
        print("\n1️⃣ Acessando landing page...")
        response = session.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Landing page carregada")
            
            # Verificar se o script analytics está presente
            if "/a.js" in response.text:
                print("   ✅ Script analytics encontrado")
            else:
                print("   ❌ Script analytics NÃO encontrado")
        
        # 2. Aguardar um pouco para simular tempo na página
        print("\n2️⃣ Simulando tempo na página...")
        time.sleep(3)
        
        # 3. Simular clique em um link com data-analytics
        print("\n3️⃣ Simulando clique em link...")
        
        # Encontrar um link com data-analytics na página
        if 'data-analytics="li:milionaria:cta:palpite_sorte"' in response.text:
            print("   ✅ Link com analytics encontrado")
            
            # Simular navegação para a página de destino
            response2 = session.get(f"{BASE_URL}/dashboard_milionaria")
            print(f"   Status dashboard: {response2.status_code}")
            
        # 4. Simular heartbeat (tempo na página)
        print("\n4️⃣ Simulando heartbeat...")
        
        # Simular dados que o JavaScript enviaria
        heartbeat_data = {
            "event": "hb",
            "path": "/",
            "ref": "",
            "session_id": "simulated-session-123",
            "visitor_id": "simulated-visitor-456",
            "device": "desktop",
            "duration_ms": 3000
        }
        
        # Enviar heartbeat
        hb_response = session.post(
            f"{BASE_URL}/api/track",
            data=json.dumps(heartbeat_data),
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Heartbeat status: {hb_response.status_code}")
        
        if hb_response.status_code == 204:
            print("   ✅ Heartbeat enviado com sucesso")
        else:
            print("   ❌ Erro no heartbeat")
            
    except Exception as e:
        print(f"❌ Erro durante simulação: {e}")

if __name__ == "__main__":
    simulate_real_visit()
