#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import sys

def verificar_usuarios_master():
    """Verifica se os usuários master existem no banco de dados."""
    try:
        conn = sqlite3.connect('database/loterias_inteligentes.db')
        cursor = conn.cursor()
        
        print("🔍 Verificando usuários master no banco de dados...")
        print("=" * 60)
        
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if not cursor.fetchone():
            print("❌ Tabela 'usuarios' não existe!")
            return
        
        # Verificar estrutura da tabela
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = cursor.fetchall()
        print("📋 Estrutura da tabela 'usuarios':")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        print()
        
        # Buscar usuários master
        cursor.execute("SELECT id, email, level FROM usuarios WHERE email LIKE '%master%'")
        users = cursor.fetchall()
        
        print(f"👥 Usuários master encontrados: {len(users)}")
        if users:
            for user in users:
                print(f"  ✅ ID: {user[0]}, Email: {user[1]}, Level: {user[2]}")
        else:
            print("  ❌ Nenhum usuário master encontrado!")
        
        print()
        
        # Verificar todos os usuários
        cursor.execute("SELECT id, email, level FROM usuarios ORDER BY id")
        all_users = cursor.fetchall()
        
        print(f"📊 Total de usuários no banco: {len(all_users)}")
        if all_users:
            print("👤 Todos os usuários:")
            for user in all_users:
                print(f"  - ID: {user[0]}, Email: {user[1]}, Level: {user[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar banco de dados: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verificar_usuarios_master()

