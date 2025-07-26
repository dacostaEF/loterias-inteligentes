#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    
    print("=== TESTE DE ROTAS ===")
    print(f"Rotas registradas:")
    
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"  {rule.rule} - {rule.methods}")
    
    print("\n=== VERIFICANDO ROTA ESPECÍFICA ===")
    matriz_route = None
    for rule in app.url_map.iter_rules():
        if 'matriz-visual' in rule.rule:
            matriz_route = rule
            break
    
    if matriz_route:
        print(f"✅ Rota matriz-visual encontrada: {matriz_route.rule}")
        print(f"   Métodos: {matriz_route.methods}")
    else:
        print("❌ Rota matriz-visual NÃO encontrada!")
        
except Exception as e:
    print(f"❌ Erro ao carregar app: {e}")
    import traceback
    traceback.print_exc() 