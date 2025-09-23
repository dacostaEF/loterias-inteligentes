#!/usr/bin/env python3
# Script para testar diferentes formas de enviar dados para /api/track

import requests
import json

BASE_URL = "https://www.loteriasinteligente.com.br"

def test_different_formats():
    print("🧪 Testando diferentes formatos de envio para /api/track...")
    
    test_data = {
        "event": "pageview",
        "path": "/test",
        "session_id": "test-session-123",
        "visitor_id": "test-visitor-456",
        "device": "desktop"
    }
    
    # Teste 1: JSON com Content-Type correto
    print("\n1️⃣ Testando JSON com Content-Type application/json...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/track",
            data=json.dumps(test_data),
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # Teste 2: JSON sem Content-Type (como sendBeacon pode enviar)
    print("\n2️⃣ Testando JSON sem Content-Type...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/track",
            data=json.dumps(test_data)
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # Teste 3: Form data
    print("\n3️⃣ Testando Form data...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/track",
            data=test_data
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # Teste 4: Texto simples
    print("\n4️⃣ Testando texto simples...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/track",
            data="event=pageview&path=/test&session_id=test-123"
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Erro: {e}")

if __name__ == "__main__":
    test_different_formats()
