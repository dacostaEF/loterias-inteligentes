#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar o banco de dados SQLite SIMPLES para Loterias Inteligentes
"""

import sqlite3
import os
from datetime import datetime

def create_simple_database():
    """Cria o banco de dados SIMPLES com apenas as tabelas essenciais."""
    
    # Cria o diretório database se não existir
    os.makedirs('database', exist_ok=True)
    
    # Conecta ao banco (cria se não existir)
    conn = sqlite3.connect('database/loterias_simples.db')
    cursor = conn.cursor()
    
    print("🗄️ Criando banco de dados SIMPLES...")
    
    # ============================================================================
    # 👥 TABELA USUÁRIOS - SIMPLES E COMPLETA
    # ============================================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            data_nascimento TEXT,
            cpf TEXT,
            telefone TEXT,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            receber_emails BOOLEAN DEFAULT 1,
            receber_sms BOOLEAN DEFAULT 1,
            aceitou_termos BOOLEAN DEFAULT 1,
            codigo_confirmacao TEXT,
            tipo_plano TEXT DEFAULT 'Free',
            data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_encerramento TIMESTAMP,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Tabela 'usuarios' criada com todas as colunas necessárias")
    
    # ============================================================================
    # 💎 TABELA PLANOS - SIMPLES
    # ============================================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS planos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            preco DECIMAL(10,2) NOT NULL,
            descricao TEXT
        )
    ''')
    print("✅ Tabela 'planos' criada")
    
    # ============================================================================
    # 🔐 TABELA CÓDIGOS DE CONFIRMAÇÃO
    # ============================================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codigos_confirmacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            codigo TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('email', 'sms')),
            status TEXT DEFAULT 'pendente' CHECK (status IN ('pendente', 'validado', 'expirado')),
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_expiracao TIMESTAMP NOT NULL,
            tentativas INTEGER DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    print("✅ Tabela 'codigos_confirmacao' criada")
    
    # ============================================================================
    # 📧 TABELA CONFIGURAÇÕES DE ENVIO
    # ============================================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes_envio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK (tipo IN ('email', 'sms')),
            servico TEXT NOT NULL,
            configuracao TEXT,
            ativo BOOLEAN DEFAULT 1,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Tabela 'configuracoes_envio' criada")
    
    # ============================================================================
    # 📊 TABELA LOGS DE ENVIO
    # ============================================================================
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_envio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tipo TEXT NOT NULL CHECK (tipo IN ('email', 'sms')),
            destinatario TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('enviado', 'erro', 'entregue')),
            mensagem TEXT,
            data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    print("✅ Tabela 'logs_envio' criada")
    
    # ============================================================================
    # 📊 INSERIR PLANOS PADRÃO
    # ============================================================================
    
    # Verificar se já existem planos
    cursor.execute("SELECT COUNT(*) FROM planos")
    if cursor.fetchone()[0] == 0:
        print("💎 Inserindo planos padrão...")
        
        planos_padrao = [
            ('Free', 0.00, 'Plano gratuito com funcionalidades básicas'),
            ('Diário', 5.00, 'Acesso premium por 24 horas'),
            ('Mensal', 29.90, 'Acesso premium por 30 dias'),
            ('Semestral', 149.90, 'Acesso premium por 6 meses'),
            ('Anual', 269.90, 'Acesso premium por 12 meses'),
            ('Vitalício', 997.00, 'Acesso premium para sempre')
        ]
        
        cursor.executemany('''
            INSERT INTO planos (nome, preco, descricao)
            VALUES (?, ?, ?)
        ''', planos_padrao)
        
        print("✅ Planos padrão inseridos")
    
    # ============================================================================
    # 📧 INSERIR CONFIGURAÇÕES DE ENVIO PADRÃO
    # ============================================================================
    
    # Verificar se já existem configurações
    cursor.execute("SELECT COUNT(*) FROM configuracoes_envio")
    if cursor.fetchone()[0] == 0:
        print("📧 Inserindo configurações de envio padrão...")
        
        import json
        
        # Configuração para email (Gmail)
        email_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "email": "dacosta_ef@hotmail.com",
            "senha": "",  # Será preenchida depois
            "destinatario_teste": "dacosta_ef@hotmail.com"
        }
        
        # Configuração para SMS (WhatsApp/Telefone)
        sms_config = {
            "telefone_teste": "21981651234",
            "servico": "whatsapp",
            "api_key": ""  # Será preenchida depois
        }
        
        configuracoes_padrao = [
            ('email', 'gmail', json.dumps(email_config)),
            ('sms', 'whatsapp', json.dumps(sms_config))
        ]
        
        cursor.executemany('''
            INSERT INTO configuracoes_envio (tipo, servico, configuracao)
            VALUES (?, ?, ?)
        ''', configuracoes_padrao)
        
        print("✅ Configurações de envio inseridas")
    
    # ============================================================================
    # 🔍 CRIAR ÍNDICES ESSENCIAIS
    # ============================================================================
    print("🚀 Criando índices essenciais...")
    
    # Índices para usuários
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios (email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_cpf ON usuarios (cpf)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_usuarios_telefone ON usuarios (telefone)')
    
    # Índices para códigos de confirmação
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_codigos_usuario ON codigos_confirmacao (usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_codigos_status ON codigos_confirmacao (status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_codigos_expiracao ON codigos_confirmacao (data_expiracao)')
    
    # Índices para logs de envio
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_usuario ON logs_envio (usuario_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_tipo ON logs_envio (tipo)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_logs_data ON logs_envio (data_envio)')
    
    print("✅ Índices criados")
    
    # Commit das alterações
    conn.commit()
    
    # Verificar dados inseridos
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM planos")
    planos_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM codigos_confirmacao")
    codigos_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM configuracoes_envio")
    configs_count = cursor.fetchone()[0]
    
    print("\n" + "="*60)
    print("🎉 BANCO DE DADOS COMPLETO CRIADO COM SUCESSO!")
    print("="*60)
    print(f"👥 Usuários: {usuarios_count}")
    print(f"💎 Planos: {planos_count}")
    print(f"🔐 Códigos: {codigos_count}")
    print(f"📧 Configurações: {configs_count}")
    print("="*60)
    print("🗄️ Arquivo: database/loterias_simples.db")
    print("✅ Estrutura COMPLETA para cadastro e confirmação!")
    print("📧 Email configurado: dacosta_ef@hotmail.com")
    print("📱 SMS configurado: 21981651234")
    print("="*60)
    
    conn.close()

if __name__ == "__main__":
    create_simple_database()
