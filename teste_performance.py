#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pandas as pd
import os

def testar_carregamento_milionaria():
    """Testa o tempo de carregamento dos dados da +Milionária"""
    print("🔍 Testando carregamento +Milionária...")
    
    start_time = time.time()
    
    try:
        # Testar carregamento direto do Excel
        excel_file = 'LoteriasExcel/Milionária_edt.xlsx'
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
            print(f"✅ Excel carregado em {time.time() - start_time:.2f}s")
            print(f"   - Linhas: {len(df)}")
            print(f"   - Colunas: {df.columns.tolist()}")
        else:
            print(f"❌ Arquivo não encontrado: {excel_file}")
            return False
    except Exception as e:
        print(f"❌ Erro ao carregar +Milionária: {e}")
        return False
    
    return True

def testar_carregamento_megasena():
    """Testa o tempo de carregamento dos dados da Mega Sena"""
    print("\n🔍 Testando carregamento Mega Sena...")
    
    start_time = time.time()
    
    try:
        # Testar carregamento direto do Excel
        excel_file = 'LoteriasExcel/MegaSena_edt.xlsx'
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
            print(f"✅ Excel carregado em {time.time() - start_time:.2f}s")
            print(f"   - Linhas: {len(df)}")
            print(f"   - Colunas: {df.columns.tolist()}")
        else:
            print(f"❌ Arquivo não encontrado: {excel_file}")
            return False
    except Exception as e:
        print(f"❌ Erro ao carregar Mega Sena: {e}")
        return False
    
    return True

def testar_funcao_carregamento_megasena():
    """Testa a função específica de carregamento da Mega Sena"""
    print("\n🔍 Testando função de carregamento Mega Sena...")
    
    start_time = time.time()
    
    try:
        from funcoes.megasena.MegasenaFuncaCarregaDadosExcel_MS import carregar_dados_megasena
        df = carregar_dados_megasena()
        print(f"✅ Função executada em {time.time() - start_time:.2f}s")
        print(f"   - Linhas: {len(df)}")
        print(f"   - Colunas: {df.columns.tolist()}")
    except Exception as e:
        print(f"❌ Erro na função de carregamento: {e}")
        return False
    
    return True

def testar_analise_frequencia_megasena():
    """Testa a análise de frequência da Mega Sena"""
    print("\n🔍 Testando análise de frequência Mega Sena (limitado a 500)...")
    
    start_time = time.time()
    
    try:
        from funcoes.megasena.funcao_analise_de_frequencia_MS import analisar_frequencia
        from funcoes.megasena.MegasenaFuncaCarregaDadosExcel_MS import carregar_dados_megasena
        
        # Carregar dados
        df = carregar_dados_megasena(limite_concursos=500)
        print(f"   - Dados carregados em {time.time() - start_time:.2f}s")
        
        # Executar análise
        analise_start = time.time()
        resultado = analisar_frequencia(df_megasena=df, qtd_concursos=50)
        print(f"   - Análise executada em {time.time() - analise_start:.2f}s")
        
        print(f"✅ Análise completa em {time.time() - start_time:.2f}s")
        print(f"   - Resultado: {type(resultado)}")
        if resultado:
            print(f"   - Chaves: {list(resultado.keys())}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Iniciando testes de performance...")
    print("=" * 50)
    
    # Teste 1: Carregamento +Milionária
    testar_carregamento_milionaria()
    
    # Teste 2: Carregamento Mega Sena
    testar_carregamento_megasena()
    
    # Teste 3: Função de carregamento Mega Sena
    testar_funcao_carregamento_megasena()
    
    # Teste 4: Análise de frequência Mega Sena
    testar_analise_frequencia_megasena()
    
    print("\n" + "=" * 50)
    print("✅ Testes concluídos!") 