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

def create_user_simple(nome_completo, email, senha, data_nascimento=None, cpf=None, telefone=None, receber_emails=True, receber_sms=True, aceitou_termos=True, plano='Free'):
    """Cria um novo usuário no banco SIMPLES com todos os campos do modal."""
    try:
        conn = get_db_connection()
        if not conn: return None
        cursor = conn.cursor()
        
        # Verificar se usuário já existe
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            print(f"⚠️ Usuário já existe: {email} (ID: {existing_user[0]})")
            conn.close()
            return existing_user[0]  # Retorna o ID do usuário existente
        
        # Hash da senha
        import hashlib
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        # Inserir usuário COMPLETO com todos os campos
        cursor.execute("""
            INSERT INTO usuarios (
                nome_completo, email, senha_hash, data_nascimento, cpf, telefone,
                receber_emails, receber_sms, aceitou_termos, tipo_plano, data_criacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            nome_completo, email, senha_hash, data_nascimento, cpf, telefone,
            receber_emails, receber_sms, aceitou_termos, plano
        ))
        
        user_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        print(f"✅ Usuário COMPLETO criado com sucesso: {email} (ID: {user_id})")
        return user_id
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário COMPLETO: {e}")
        if conn: conn.close()
        return None

# ============================================================================
# 🔐 FUNÇÕES PARA CÓDIGOS DE CONFIRMAÇÃO
# ============================================================================

def gerar_codigo_confirmacao(usuario_id, tipo='email'):
    """Gera um código de confirmação de 6 dígitos para o usuário."""
    try:
        import random
        import datetime
        
        conn = get_db_connection()
        if not conn: return None
        cursor = conn.cursor()
        
        # Gerar código de 6 dígitos
        codigo = str(random.randint(100000, 999999))
        
        # Data de expiração (10 minutos)
        data_expiracao = datetime.datetime.now() + datetime.timedelta(minutes=10)
        
        # Inserir código no banco
        cursor.execute("""
            INSERT INTO codigos_confirmacao (usuario_id, codigo, tipo, data_expiracao)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, codigo, tipo, data_expiracao))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Código gerado: {codigo} para usuário {usuario_id} ({tipo})")
        return codigo
        
    except Exception as e:
        print(f"❌ Erro ao gerar código: {e}")
        if conn: conn.close()
        return None

def validar_codigo_confirmacao(usuario_id, codigo, tipo='email'):
    """Valida um código de confirmação."""
    try:
        import datetime
        
        conn = get_db_connection()
        if not conn: return False
        cursor = conn.cursor()
        
        # Buscar código válido (independente do tipo)
        cursor.execute("""
            SELECT id, tentativas, tipo FROM codigos_confirmacao 
            WHERE usuario_id = ? AND codigo = ? 
            AND status = 'pendente' AND data_expiracao > ?
        """, (usuario_id, codigo, datetime.datetime.now()))
        
        resultado = cursor.fetchone()
        
        if resultado:
            # Código válido - marcar como validado
            cursor.execute("""
                UPDATE codigos_confirmacao 
                SET status = 'validado' 
                WHERE id = ?
            """, (resultado[0],))
            
            conn.commit()
            conn.close()
            print(f"✅ Código validado com sucesso para usuário {usuario_id}")
            return True
        else:
            # Código inválido - incrementar tentativas
            cursor.execute("""
                UPDATE codigos_confirmacao 
                SET tentativas = tentativas + 1 
                WHERE usuario_id = ? AND tipo = ? AND status = 'pendente'
            """, (usuario_id, tipo))
            
            conn.commit()
            conn.close()
            print(f"❌ Código inválido para usuário {usuario_id}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao validar código: {e}")
        if conn: conn.close()
        return False

def obter_configuracao_envio(tipo):
    """Obtém a configuração de envio para email ou SMS."""
    try:
        conn = get_db_connection()
        if not conn: return None
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT servico, configuracao FROM configuracoes_envio 
            WHERE tipo = ? AND ativo = 1
        """, (tipo,))
        
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            import json
            config = json.loads(resultado[1])
            config['servico'] = resultado[0]
            return config
        
        return None
        
    except Exception as e:
        print(f"❌ Erro ao obter configuração: {e}")
        if conn: conn.close()
        return None

if __name__ == '__main__':
    # Teste das funções
    print("🧪 TESTANDO CONFIGURAÇÃO DO BANCO")
    print("=" * 40)
    
    if test_connection():
        print("✅ Conexão com banco funcionando")
        print(f"📁 Banco localizado em: {DATABASE_PATH}")
    else:
        print("❌ Erro na conexão com banco")

