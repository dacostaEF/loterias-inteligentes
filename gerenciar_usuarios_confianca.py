#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para gerenciar usuários de confiança
"""

import sys
import os
import hashlib
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar configuração do banco
from database.db_config import get_db_connection

def listar_usuarios_confianca():
    """Lista todos os usuários de confiança."""
    conn = get_db_connection()
    if not conn:
        print("❌ Erro ao conectar ao banco!")
        return
    
    cursor = conn.cursor()
    
    print("👥 USUÁRIOS DE CONFIANÇA:")
    print("=" * 80)
    
    cursor.execute("""
        SELECT id, nome_completo, email, nivel, ativo, data_criacao, ultimo_acesso, criado_por, observacoes
        FROM usuarios_confianca
        ORDER BY data_criacao DESC
    """)
    
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("❌ Nenhum usuário de confiança encontrado!")
        return
    
    for usuario in usuarios:
        id_user, nome, email, nivel, ativo, data_criacao, ultimo_acesso, criado_por, obs = usuario
        
        status = "✅ Ativo" if ativo else "❌ Inativo"
        ultimo = ultimo_acesso.strftime("%d/%m/%Y %H:%M") if ultimo_acesso else "Nunca"
        
        print(f"ID: {id_user}")
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Nível: {nivel}")
        print(f"Status: {status}")
        print(f"Criado em: {data_criacao.strftime('%d/%m/%Y %H:%M')}")
        print(f"Último acesso: {ultimo}")
        print(f"Criado por: {criado_por}")
        print(f"Observações: {obs or 'Nenhuma'}")
        print("-" * 80)
    
    conn.close()

def adicionar_usuario_confianca():
    """Adiciona um novo usuário de confiança."""
    print("\n➕ ADICIONAR USUÁRIO DE CONFIANÇA")
    print("=" * 50)
    
    nome = input("Nome completo: ").strip()
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    nivel = input("Nível (CONFIANCA/VIP/PARTNER): ").strip().upper()
    criado_por = input("Criado por (seu nome): ").strip()
    obs = input("Observações (opcional): ").strip()
    
    if not all([nome, email, senha, nivel]):
        print("❌ Todos os campos obrigatórios devem ser preenchidos!")
        return
    
    if nivel not in ['CONFIANCA', 'VIP', 'PARTNER']:
        print("❌ Nível deve ser CONFIANCA, VIP ou PARTNER!")
        return
    
    conn = get_db_connection()
    if not conn:
        print("❌ Erro ao conectar ao banco!")
        return
    
    cursor = conn.cursor()
    
    # Verificar se email já existe
    cursor.execute("SELECT id FROM usuarios_confianca WHERE email = ?", (email,))
    if cursor.fetchone():
        print("❌ Email já existe!")
        conn.close()
        return
    
    # Hash da senha
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    # Inserir usuário
    cursor.execute("""
        INSERT INTO usuarios_confianca (nome_completo, email, senha_hash, nivel, criado_por, observacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, email, senha_hash, nivel, criado_por, obs))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Usuário {nome} adicionado com sucesso!")
    print(f"📧 Email: {email}")
    print(f"🔑 Senha: {senha}")
    print(f"👤 Nível: {nivel}")

def remover_usuario_confianca():
    """Remove um usuário de confiança."""
    print("\n🗑️ REMOVER USUÁRIO DE CONFIANÇA")
    print("=" * 50)
    
    email = input("Email do usuário a ser removido: ").strip()
    
    if not email:
        print("❌ Email é obrigatório!")
        return
    
    conn = get_db_connection()
    if not conn:
        print("❌ Erro ao conectar ao banco!")
        return
    
    cursor = conn.cursor()
    
    # Verificar se usuário existe
    cursor.execute("SELECT nome_completo FROM usuarios_confianca WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    
    if not usuario:
        print("❌ Usuário não encontrado!")
        conn.close()
        return
    
    confirmar = input(f"Tem certeza que deseja remover {usuario[0]}? (s/N): ").strip().lower()
    
    if confirmar in ['s', 'sim', 'y', 'yes']:
        cursor.execute("DELETE FROM usuarios_confianca WHERE email = ?", (email,))
        conn.commit()
        print(f"✅ Usuário {usuario[0]} removido com sucesso!")
    else:
        print("❌ Operação cancelada!")
    
    conn.close()

def alterar_senha_usuario():
    """Altera a senha de um usuário de confiança."""
    print("\n🔑 ALTERAR SENHA DE USUÁRIO")
    print("=" * 50)
    
    email = input("Email do usuário: ").strip()
    nova_senha = input("Nova senha: ").strip()
    
    if not all([email, nova_senha]):
        print("❌ Email e nova senha são obrigatórios!")
        return
    
    conn = get_db_connection()
    if not conn:
        print("❌ Erro ao conectar ao banco!")
        return
    
    cursor = conn.cursor()
    
    # Verificar se usuário existe
    cursor.execute("SELECT nome_completo FROM usuarios_confianca WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    
    if not usuario:
        print("❌ Usuário não encontrado!")
        conn.close()
        return
    
    # Hash da nova senha
    nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
    
    # Atualizar senha
    cursor.execute("UPDATE usuarios_confianca SET senha_hash = ? WHERE email = ?", (nova_senha_hash, email))
    conn.commit()
    conn.close()
    
    print(f"✅ Senha alterada com sucesso para {usuario[0]}!")
    print(f"🔑 Nova senha: {nova_senha}")

def menu_principal():
    """Menu principal do gerenciador."""
    while True:
        print("\n" + "=" * 60)
        print("🔐 GERENCIADOR DE USUÁRIOS DE CONFIANÇA")
        print("=" * 60)
        print("1. 👥 Listar usuários")
        print("2. ➕ Adicionar usuário")
        print("3. 🗑️ Remover usuário")
        print("4. 🔑 Alterar senha")
        print("5. ❌ Sair")
        print("=" * 60)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            listar_usuarios_confianca()
        elif opcao == '2':
            adicionar_usuario_confianca()
        elif opcao == '3':
            remover_usuario_confianca()
        elif opcao == '4':
            alterar_senha_usuario()
        elif opcao == '5':
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    menu_principal()
