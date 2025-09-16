#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

print("🔍 Testando carregamento de dados da Quina...")

try:
    from services.data_loader import carregar_dados_quina_app
    print("✅ Import do data_loader OK")
    
    df = carregar_dados_quina_app()
    print(f"✅ DataFrame carregado: {df is not None and not df.empty}")
    
    if df is not None and not df.empty:
        print(f"📊 Shape: {df.shape}")
        print(f"📋 Colunas: {list(df.columns)}")
        print("📄 Primeiras 3 linhas:")
        print(df.head(3))
    else:
        print("❌ DataFrame vazio ou None")
        
except Exception as e:
    print(f"❌ Erro ao carregar dados: {e}")
    import traceback
    traceback.print_exc()

print("\n🔍 Testando função de análise de frequência...")

try:
    from funcoes.quina.funcao_analise_de_frequencia_quina import analisar_frequencia_quina
    print("✅ Import da função de análise OK")
    
    if df is not None and not df.empty:
        resultado = analisar_frequencia_quina(df_quina=df, qtd_concursos=50)
        print(f"✅ Análise executada: {resultado is not None}")
        
        if resultado and 'numeros_quentes_frios' in resultado:
            quentes = resultado['numeros_quentes_frios'].get('numeros_quentes', [])
            frios = resultado['numeros_quentes_frios'].get('numeros_frios', [])
            secos = resultado['numeros_quentes_frios'].get('numeros_secos', [])
            
            print(f"🔥 Números quentes (primeiros 5): {quentes[:5]}")
            print(f"❄️ Números frios (primeiros 5): {frios[:5]}")
            print(f"⚡ Números secos (primeiros 5): {secos[:5]}")
        else:
            print("❌ numeros_quentes_frios não encontrado no resultado")
            print(f"📋 Chaves disponíveis: {list(resultado.keys()) if resultado else 'None'}")
    else:
        print("❌ Não é possível testar análise sem dados")
        
except Exception as e:
    print(f"❌ Erro na análise: {e}")
    import traceback
    traceback.print_exc()

print("\n🔍 Testando API endpoint...")

try:
    from app import app
    print("✅ Import do app OK")
    
    with app.test_client() as client:
        response = client.get('/api/analise-frequencia-quina?qtd_concursos=50')
        print(f"📡 Status da API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"📋 Chaves da resposta: {list(data.keys())}")
            
            if 'numeros_quentes_frios' in data:
                quentes = data['numeros_quentes_frios'].get('numeros_quentes', [])
                frios = data['numeros_quentes_frios'].get('numeros_frios', [])
                secos = data['numeros_quentes_frios'].get('numeros_secos', [])
                
                print(f"🔥 API - Números quentes (primeiros 5): {quentes[:5]}")
                print(f"❄️ API - Números frios (primeiros 5): {frios[:5]}")
                print(f"⚡ API - Números secos (primeiros 5): {secos[:5]}")
            else:
                print("❌ numeros_quentes_frios não encontrado na resposta da API")
        else:
            print(f"❌ Erro na API: {response.get_data(as_text=True)}")
            
except Exception as e:
    print(f"❌ Erro ao testar API: {e}")
    import traceback
    traceback.print_exc()

