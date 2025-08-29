#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script SIMPLIFICADO para criar banco de dados focado apenas em:
- Usuários (com todos os campos do cadastro)
- Planos 
- Assinaturas/Pagamentos
"""

import sqlite3
import bcrypt
import json
import os

# Configuração do banco
DATABASE = 'loterias_simples.db'
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE)

def create_connection():
    """Cria conexão com o banco SQLite"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error as e:
        print(f"❌ Erro ao conectar: {e}")
        return None

def create_tables(conn):
    """Cria apenas as tabelas essenciais"""
    try:
        cursor = conn.cursor()
        
        print("🔨 Criando tabelas essenciais...")

        # 1. TABELA USUARIOS (com todos os campos do cadastro)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_completo VARCHAR(255) NOT NULL,
                data_nascimento DATE,
                cpf VARCHAR(14) UNIQUE,
                telefone_celular VARCHAR(15),
                email VARCHAR(255) UNIQUE NOT NULL,
                senha_hash VARCHAR(255) NOT NULL,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'ativo',
                receber_emails BOOLEAN DEFAULT 1,
                receber_sms BOOLEAN DEFAULT 1,
                aceitou_termos BOOLEAN DEFAULT 0
            );
        """)
        print("✅ Tabela 'usuarios' criada")

        # 2. TABELA PLANOS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                duracao_dias INTEGER NOT NULL,
                descricao TEXT
            );
        """)
        print("✅ Tabela 'planos' criada")

        # 3. TABELA ASSINATURAS (inclui pagamento)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assinaturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                plano_id INTEGER NOT NULL,
                data_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_expiracao DATETIME,
                status VARCHAR(20) DEFAULT 'pendente',
                valor_pago DECIMAL(10,2),
                metodo_pagamento VARCHAR(50),
                id_transacao VARCHAR(255),
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (plano_id) REFERENCES planos (id)
            );
        """)
        print("✅ Tabela 'assinaturas' criada")

        # Índices para performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_cpf ON usuarios(cpf);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assinaturas_usuario ON assinaturas(usuario_id);")
        
        conn.commit()
        print("\n🎉 Tabelas essenciais criadas com sucesso!")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        conn.rollback()

def insert_planos(conn):
    """Insere planos básicos"""
    try:
        cursor = conn.cursor()
        
        # Verifica se já existem planos
        cursor.execute("SELECT COUNT(*) FROM planos;")
        if cursor.fetchone()[0] == 0:
            print("\n📋 Inserindo planos...")
            
            planos = [
                ("Free", 0.00, 99999, "Acesso básico: +Milionária, Quina, Lotomania"),
                ("Mensal", 19.90, 30, "Acesso completo por 1 mês"),
                ("Semestral", 99.90, 180, "Acesso completo por 6 meses"),
                ("Anual", 179.90, 365, "Acesso completo por 1 ano"),
                ("Vitalício", 499.90, 99999, "Acesso completo para sempre")
            ]
            
            cursor.executemany("""
                INSERT INTO planos (nome, valor, duracao_dias, descricao)
                VALUES (?, ?, ?, ?);
            """, planos)
            
            conn.commit()
            print("✅ Planos inseridos com sucesso!")
        else:
            print("ℹ️ Planos já existem")
            
    except sqlite3.Error as e:
        print(f"❌ Erro ao inserir planos: {e}")

def create_usuario_teste(conn):
    """Cria usuário de teste"""
    try:
        cursor = conn.cursor()
        
        # Verifica se já existe
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = 'teste@loterias.com';")
        if cursor.fetchone()[0] == 0:
            print("\n👤 Criando usuário de teste...")
            
            senha_hash = bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute("""
                INSERT INTO usuarios (nome_completo, email, senha_hash, status, receber_emails, receber_sms, aceitou_termos)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, ("Usuário Teste", "teste@loterias.com", senha_hash.decode('utf-8'), "ativo", 1, 1, 1))
            
            conn.commit()
            print("✅ Usuário teste: teste@loterias.com / 123456")
        else:
            print("ℹ️ Usuário teste já existe")
            
    except sqlite3.Error as e:
        print(f"❌ Erro ao criar usuário: {e}")

def mostrar_info(conn):
    """Mostra informações do banco"""
    try:
        cursor = conn.cursor()
        
        print("\n📊 INFORMAÇÕES DO BANCO:")
        print("=" * 40)
        
        # Contar registros
        tables = ['usuarios', 'planos', 'assinaturas']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"📋 {table.capitalize()}: {count} registros")
        
        # Mostrar planos
        cursor.execute("SELECT nome, valor, duracao_dias FROM planos;")
        plans = cursor.fetchall()
        
        print("\n💎 PLANOS DISPONÍVEIS:")
        for plan in plans:
            nome, valor, dias = plan
            if valor == 0:
                print(f"  🆓 {nome}: Gratuito")
            else:
                print(f"  💰 {nome}: R$ {valor:.2f} ({dias} dias)")
        
        print(f"\n🗄️ Banco criado em: {DATABASE_PATH}")
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao mostrar info: {e}")

def main():
    """Função principal"""
    print("🚀 CRIANDO BANCO SIMPLIFICADO PARA LOTERIAS")
    print("=" * 50)
    
    conn = create_connection()
    if not conn:
        print("❌ Erro na conexão")
        return
    
    try:
        create_tables(conn)
        insert_planos(conn)
        create_usuario_teste(conn)
        mostrar_info(conn)
        
        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. ✅ Banco simplificado criado!")
        print("2. 🔧 Integrar com app.py")
        print("3. 🧪 Testar cadastro/login")
        print("4. 💳 Implementar pagamentos")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()
        print(f"\n🔒 Conexão fechada")

if __name__ == '__main__':
    main()
