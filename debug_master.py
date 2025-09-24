#!/usr/bin/env python3

import sqlite3

def verificar_usuarios_master():
    try:
        conn = sqlite3.connect('database/loterias_simples.db')
        cursor = conn.cursor()
        
        print("=== USUÁRIOS MASTER ===")
        cursor.execute("SELECT id, email, tipo_plano FROM usuarios WHERE email LIKE '%master%'")
        masters = cursor.fetchall()
        
        for row in masters:
            print(f"ID: {row[0]}, Email: {row[1]}, Plano: {row[2]}")
        
        print("\n=== TODOS OS USUÁRIOS ===")
        cursor.execute("SELECT id, email, tipo_plano FROM usuarios LIMIT 10")
        todos = cursor.fetchall()
        
        for row in todos:
            print(f"ID: {row[0]}, Email: {row[1]}, Plano: {row[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    verificar_usuarios_master()
