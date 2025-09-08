#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para LIMPAR dados de teste - Mantém apenas configurações
"""

import sqlite3
import os

def limpar_dados_teste():
    """Limpa todos os dados de teste, mantendo apenas configurações."""
    
    print("🧹 LIMPANDO DADOS DE TESTE...")
    print("=" * 50)
    
    db_path = 'database/loterias_simples.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não existe!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Limpar dados de teste
    print("🗑️ Removendo usuários de teste...")
    cursor.execute("DELETE FROM usuarios")
    print("✅ Usuários removidos")
    
    print("🗑️ Removendo códigos de confirmação...")
    cursor.execute("DELETE FROM codigos_confirmacao")
    print("✅ Códigos de confirmação removidos")
    
    print("🗑️ Removendo logs de envio...")
    cursor.execute("DELETE FROM logs_envio")
    print("✅ Logs de envio removidos")
    
    print("🗑️ Removendo pagamentos...")
    cursor.execute("DELETE FROM pagamentos")
    print("✅ Pagamentos removidos")
    
    # RECRIAR usuários master fixos (sempre disponíveis)
    print("👥 Recriando usuários master fixos...")
    
    import hashlib
    
    # Usuários master fixos - SEMPRE recriados
    usuarios_master = [
        ('Master_EF', '01/01/1990', '000.000.000-01', '(11) 99999-0001', 'master_ef@loterias.com', 'Tete&2602'),
        ('Master_SF', '01/01/1990', '000.000.000-02', '(11) 99999-0002', 'master_sf@loterias.com', 'Tete&2602'),
        ('Master_SM', '01/01/1990', '000.000.000-03', '(11) 99999-0003', 'master_sm@loterias.com', 'Tete&2602'),
        ('Master_JJ', '01/01/1990', '000.000.000-04', '(11) 99999-0004', 'master_jj@loterias.com', 'Tete&2602'),
        ('Master_FC', '01/01/1990', '000.000.000-05', '(11) 99999-0005', 'master_fc@loterias.com', 'Tete&2602'),
        ('Master_DC', '01/01/1990', '000.000.000-06', '(11) 99999-0006', 'master_dc@loterias.com', 'Tete&2602')
    ]
    
    for usuario in usuarios_master:
        nome, data_nasc, cpf, telefone, email, senha = usuario
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        # Remover se já existir
        cursor.execute("DELETE FROM usuarios WHERE email = ?", (email,))
        
        # Inserir/recriar usuário master
        cursor.execute('''
            INSERT INTO usuarios (nome_completo, data_nascimento, cpf, telefone, email, senha_hash, tipo_plano)
            VALUES (?, ?, ?, ?, ?, ?, 'Vitalício')
        ''', (nome, data_nasc, cpf, telefone, email, senha_hash))
    
    print("✅ Usuários master fixos recriados")
    print("👤 Master_EF (master_ef@loterias.com): Tete&2602")
    print("👤 Master_SF (master_sf@loterias.com): Tete&2602")
    print("👤 Master_SM (master_sm@loterias.com): Tete&2602")
    print("👤 Master_JJ (master_jj@loterias.com): Tete&2602")
    print("👤 Master_FC (master_fc@loterias.com): Tete&2602")
    print("👤 Master_DC (master_dc@loterias.com): Tete&2602")
    
    # Resetar auto-increment
    print("🔄 Resetando contadores...")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('usuarios', 'codigos_confirmacao', 'logs_envio', 'pagamentos')")
    print("✅ Contadores resetados")
    
    # Commit e fechar
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 50)
    print("🎉 DADOS DE TESTE LIMPOS COM SUCESSO!")
    print("=" * 50)
    print("✅ Usuários removidos")
    print("✅ Códigos de confirmação removidos")
    print("✅ Logs de envio removidos")
    print("✅ Pagamentos removidos")
    print("✅ Contadores resetados")
    print("=" * 50)
    print("📧 Configurações de email mantidas")
    print("📱 Configurações de SMS mantidas")
    print("💎 Planos mantidos")
    print("👤 6 Usuários master recriados")
    print("=" * 50)
    print("🎯 Pronto para novos testes!")
    print("=" * 50)

def mostrar_status():
    """Mostra o status atual do banco."""
    db_path = 'database/loterias_simples.db'
    
    if not os.path.exists(db_path):
        print("❌ Banco de dados não existe!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📊 STATUS DO BANCO DE DADOS:")
    print("=" * 40)
    
    # Contar registros
    tabelas = ['usuarios', 'planos', 'codigos_confirmacao', 'configuracoes_envio', 'logs_envio']
    
    for tabela in tabelas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            print(f"📋 {tabela}: {count} registros")
        except:
            print(f"❌ {tabela}: tabela não existe")
    
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        mostrar_status()
    else:
        print("🚨 ATENÇÃO: Isso vai APAGAR todos os dados de teste!")
        print("📧 Configurações de email e SMS serão mantidas")
        print("💎 Planos serão mantidos")
        resposta = input("Deseja continuar? (s/N): ")
        
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            limpar_dados_teste()
        else:
            print("❌ Operação cancelada.")
