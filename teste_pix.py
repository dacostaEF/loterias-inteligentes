#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste de criação de PIX
"""

from services.checkout_transparente import checkout_transparente
import json

def testar_pix():
    """Testar criação de PIX."""
    print("🔄 Testando criação de PIX...")
    
    # Dados de teste
    dados_teste = {
        'valor': 5.00,
        'descricao': 'Teste PIX - Plano Diário',
        'email': 'dacosta_ef@hotmail.com',
        'cpf': '12345678901',
        'external_reference': 'teste_pix_123'
    }
    
    try:
        resultado = checkout_transparente.criar_pagamento_pix(dados_teste)
        
        print("📊 Resultado:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
        if resultado.get('success'):
            print("\n✅ PIX criado com sucesso!")
            print(f"🆔 Payment ID: {resultado.get('payment_id')}")
            print(f"📊 Status: {resultado.get('status')}")
            
            if resultado.get('qr_code'):
                print(f"🏦 QR Code: {resultado.get('qr_code')[:50]}...")
            else:
                print("❌ QR Code não foi gerado!")
                
            if resultado.get('comprovante'):
                print("📄 Comprovante gerado!")
            else:
                print("❌ Comprovante não foi gerado!")
        else:
            print(f"❌ Erro: {resultado.get('error')}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")

if __name__ == "__main__":
    testar_pix()



