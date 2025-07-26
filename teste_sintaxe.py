#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import sys

def verificar_sintaxe(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Tenta compilar o código
        ast.parse(codigo)
        print(f"✅ Sintaxe do arquivo {arquivo} está correta!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe em {arquivo}:")
        print(f"   Linha {e.lineno}: {e.text}")
        print(f"   Erro: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar {arquivo}: {e}")
        return False

if __name__ == "__main__":
    print("=== VERIFICAÇÃO DE SINTAXE ===")
    verificar_sintaxe('app.py') 