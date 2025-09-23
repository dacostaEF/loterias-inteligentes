#!/usr/bin/env python3
# Script para testar o sistema de analytics

import requests
import json

# URL base do site
BASE_URL = "https://www.loteriasinteligente.com.br"

def test_analytics():
    print("🧪 Testando sistema de analytics...")
    
    # Teste 1: Verificar se o endpoint /a.js está funcionando
    print("\n1️⃣ Testando endpoint /a.js...")
    try:
        response = requests.get(f"{BASE_URL}/a.js")
        print(f"   Status: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('content-type')}")
        print(f"   Tamanho: {len(response.text)} bytes")
        if response.status_code == 200:
            print("   ✅ Endpoint /a.js funcionando")
        else:
            print("   ❌ Endpoint /a.js com problema")
    except Exception as e:
        print(f"   ❌ Erro ao acessar /a.js: {e}")
    
    # Teste 2: Simular uma requisição de analytics
    print("\n2️⃣ Testando endpoint /api/track...")
    try:
        test_data = {
            "event": "pageview",
            "path": "/test",
            "ref": "https://google.com",
            "session_id": "test-session-123",
            "visitor_id": "test-visitor-456",
            "device": "desktop",
            "duration_ms": 5000
        }
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/track",
            data=json.dumps(test_data),
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 204:
            print("   ✅ Endpoint /api/track funcionando")
        else:
            print("   ❌ Endpoint /api/track com problema")
            
    except Exception as e:
        print(f"   ❌ Erro ao testar /api/track: {e}")
    
    # Teste 3: Verificar se a página landing carrega o analytics
    print("\n3️⃣ Testando página landing...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if "/a.js" in response.text:
            print("   ✅ Script /a.js incluído na landing page")
        else:
            print("   ❌ Script /a.js NÃO encontrado na landing page")
            
        if "data-analytics" in response.text:
            print("   ✅ Atributos data-analytics encontrados")
        else:
            print("   ❌ Atributos data-analytics NÃO encontrados")
            
    except Exception as e:
        print(f"   ❌ Erro ao testar landing page: {e}")

if __name__ == "__main__":
    test_analytics()
