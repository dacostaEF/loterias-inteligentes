#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração simples para conexão com o banco de dados SQLite.
"""

import sqlite3
import os

# Configuração do banco
DATABASE = 'loterias_simples.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE)

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row  # Para retornar dicionários
        return conn
    except sqlite3.Error as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def test_connection():
    """Testa a conexão com o banco"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            conn.close()
            return True
        return False
    except Exception as e:
        print(f"❌ Erro no teste de conexão: {e}")
        return False

if __name__ == '__main__':
    # Teste das funções
    print("🧪 TESTANDO CONFIGURAÇÃO DO BANCO")
    print("=" * 40)
    
    if test_connection():
        print("✅ Conexão com banco funcionando")
        print(f"📁 Banco localizado em: {DATABASE_PATH}")
    else:
        print("❌ Erro na conexão com banco")
