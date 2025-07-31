#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

print("=== TESTE DE PATH ===")
print(f"Diretório atual: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Testar se o arquivo Excel existe
excel_path = "LoteriasExcel/Milionária_edt.xlsx"
print(f"\nArquivo Excel existe? {os.path.exists(excel_path)}")

# Testar import
try:
    print("\nTentando importar...")
    from funcoes.milionaria.MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
    print("✅ Import OK")
    
    print("\nTentando carregar dados...")
    df = carregar_dados_milionaria()
    print(f"✅ Dados carregados: {len(df)} linhas")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc() 