#!/usr/bin/env python3
"""
Debug da API de bolões - testar manualmente
"""

from app import app
from analytics_models import db
from boloes_models import Bolao
import json

def testar_api_boloes():
    with app.app_context():
        print("🔍 TESTANDO API BOLÕES...")
        
        # Testar rota diretamente
        from routes_boloes import bp_boloes
        from flask import Flask
        
        test_app = Flask(__name__)
        test_app.config.from_object('config')
        test_app.register_blueprint(bp_boloes)
        
        # Simular requisição
        with test_app.test_client() as client:
            # Testar endpoint de listagem
            response = client.get('/api/boloes/listar?loteria=quina')
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.get_json()}")
            
            # Testar endpoint de listagem geral
            response2 = client.get('/api/boloes/listar')
            print(f"Status Code (all): {response2.status_code}")
            print(f"Response (all): {response2.get_json()}")

def testar_banco_direto():
    with app.app_context():
        print("\n🔍 TESTANDO BANCO DIRETO...")
        
        # Contar bolões
        total = Bolao.query.count()
        print(f"Total bolões: {total}")
        
        # Listar bolões da Quina
        boloes_quina = Bolao.query.filter(Bolao.loteria == 'quina').all()
        print(f"Bolões Quina: {len(boloes_quina)}")
        
        for bolao in boloes_quina:
            print(f"  - {bolao.codigo}: {bolao.nome} ({bolao.status})")
            
        # Testar JSON structure esperado pela API
        if boloes_quina:
            bolao = boloes_quina[0]
            try:
                resultado = {
                    'id': bolao.id,
                    'codigo': bolao.codigo,
                    'nome': bolao.nome,
                    'loteria': bolao.loteria,
                    'valor_cota': float(bolao.valor_cota),
                    'total_cotas': bolao.total_cotas,
                    'cotas_vendidas': bolao.cotas_vendidas,
                    'cotas_restantes': bolao.cotas_restantes,
                    'percentual_preenchido': round(bolao.percentual_preenchido, 1),
                    'status': bolao.status,
                    'probabilidade': bolao.probabilidade,
                    'pode_fechar': bolao.pode_fechar
                }
                print(f"JSON seria: {json.dumps(resultado, indent=2)}")
            except Exception as e:
                print(f"ERRO ao montar JSON: {e}")

if __name__ == "__main__":
    testar_banco_direto()
    print("\n" + "="*50)
    testar_api_boloes()
