#!/usr/bin/env python3
"""
Teste rápido para verificar se os bolões estão funcionando
"""

from app import app
from analytics_models import db
from boloes_models import Bolao
import json

def testar_boloes():
    with app.app_context():
        print("🔍 TESTANDO BOLÕES...")
        
        # Verificar quantos bolões temos
        total = Bolao.query.count()
        print(f"📊 Total de bolões no banco: {total}")
        
        if total == 0:
            print("❌ Nenhum bolão encontrado!")
            return
        
        # Listar todos os bolões
        boloes = Bolao.query.all()
        print("\n🎯 BOLÕES ENCONTRADOS:")
        print("-" * 50)
        
        for bolao in boloes:
            print(f"🎲 {bolao.codigo} - {bolao.nome}")
            print(f"   Loteria: {bolao.loteria}")
            print(f"   Cotas: {bolao.cotas_vendidas}/{bolao.total_cotas}")
            print(f"   Valor/cota: R$ {bolao.valor_cota}")
            print(f"   Status: {bolao.status}")
            print(f"   Probabilidade: {bolao.probabilidade}")
            
            # Mostrar números
            if bolao.numeros_escolhidos:
                try:
                    numeros = json.loads(bolao.numeros_escolhidos)
                    print(f"   Números: {numeros.get('numeros', [])}")
                    if numeros.get('trevos'):
                        print(f"   Trevos: {numeros.get('trevos', [])}")
                except:
                    print(f"   Números: {bolao.numeros_escolhidos}")
            print()
        
        # Testar por loteria
        print("📈 BOLÕES POR LOTERIA:")
        for loteria in ['quina', 'megasena', 'lotofacil', 'milionaria']:
            count = Bolao.query.filter(Bolao.loteria == loteria).count()
            if count > 0:
                print(f"   {loteria.title()}: {count} bolões")
        
        print("\n✅ TESTE CONCLUÍDO!")

if __name__ == "__main__":
    testar_boloes()
