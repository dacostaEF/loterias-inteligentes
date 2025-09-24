#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para popular o banco de dados com bolões iniciais
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from boloes_models import (
    Bolao, ParticipanteBolao, HistoricoBolao,
    criar_bolao_milionaria, criar_bolao_lotofacil, 
    criar_bolao_megasena, criar_bolao_quina
)
from datetime import datetime, timedelta

def popular_boloes_iniciais():
    """Popula o banco com bolões iniciais"""
    
    with app.app_context():
        try:
            # Criar tabelas se não existirem
            print("🔨 Verificando e criando tabelas...")
            db.create_all()
            print("✅ Tabelas verificadas/criadas!")
            
            # Verificar se já existem bolões
            try:
                if Bolao.query.count() > 0:
                    print("⚠️ Já existem bolões no banco. Pulando criação...")
                    return
            except Exception as e:
                print(f"⚠️ Erro ao verificar bolões existentes (primeira vez?): {e}")
                # Continuar mesmo assim para criar os primeiros bolões
            
            print("🚀 Criando bolões iniciais...")
            
            # 🎯 MILIONÁRIA - 2 Bolões Inteligentes
            boloes_milionaria = [
                {
                    'codigo': 'LI-MF-001',
                    'nome': 'Grupo Inteligente MF-001',
                    'valor_cota': 15.00,
                    'total_cotas': 20,
                    'cotas_minimas': 15,
                    'probabilidade': 'Muito Alta',
                    'cotas_vendidas': 8,
                    'numeros': [3, 7, 15, 23, 35, 42],
                    'trevos': [2, 5]
                },
                {
                    'codigo': 'LI-MF-002',
                    'nome': 'Grupo Inteligente MF-002',
                    'valor_cota': 18.00,
                    'total_cotas': 15,
                    'cotas_minimas': 12,
                    'probabilidade': 'Boa',
                    'cotas_vendidas': 13,
                    'numeros': [9, 14, 21, 28, 31, 47],
                    'trevos': [1, 4]
                }
            ]
            
            # 🎯 LOTOFÁCIL - 2 Bolões Inteligentes
            boloes_lotofacil = [
                {
                    'codigo': 'LI-LF-001',
                    'nome': 'Grupo Inteligente LF-001',
                    'valor_cota': 12.00,
                    'total_cotas': 25,
                    'cotas_minimas': 20,
                    'probabilidade': 'Muito Alta',
                    'cotas_vendidas': 22,
                    'numeros': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
                },
                {
                    'codigo': 'LI-LF-002',
                    'nome': 'Grupo Inteligente LF-002',
                    'valor_cota': 10.00,
                    'total_cotas': 20,
                    'cotas_minimas': 16,
                    'probabilidade': 'Alta',
                    'cotas_vendidas': 11,
                    'numeros': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
                }
            ]
            
            # 🎯 MEGA SENA - 2 Bolões Inteligentes
            boloes_megasena = [
                {
                    'codigo': 'LI-MS-001',
                    'nome': 'Grupo Inteligente MS-001',
                    'valor_cota': 25.00,
                    'total_cotas': 15,
                    'cotas_minimas': 12,
                    'probabilidade': 'Boa',
                    'cotas_vendidas': 9,
                    'numeros': [7, 14, 23, 35, 42, 58]
                },
                {
                    'codigo': 'LI-MS-002',
                    'nome': 'Grupo Inteligente MS-002',
                    'valor_cota': 30.00,
                    'total_cotas': 12,
                    'cotas_minimas': 10,
                    'probabilidade': 'Média',
                    'cotas_vendidas': 10,
                    'numeros': [5, 18, 27, 33, 49, 56]
                }
            ]
            
            # 🎯 QUINA - 2 Bolões Inteligentes
            boloes_quina = [
                {
                    'codigo': 'LI-QN-001',
                    'nome': 'Grupo Inteligente QN-001',
                    'valor_cota': 8.00,
                    'total_cotas': 20,
                    'cotas_minimas': 16,
                    'probabilidade': 'Alta',
                    'cotas_vendidas': 18,
                    'numeros': [12, 23, 34, 45, 67]
                },
                {
                    'codigo': 'LI-QN-002',
                    'nome': 'Grupo Inteligente QN-002',
                    'valor_cota': 6.00,
                    'total_cotas': 25,
                    'cotas_minimas': 20,
                    'probabilidade': 'Muito Alta',
                    'cotas_vendidas': 15,
                    'numeros': [8, 19, 28, 41, 72]
                }
            ]
            
            # Criar bolões da Milionária
            for dados in boloes_milionaria:
                bolao = criar_bolao_milionaria(
                    dados['codigo'],
                    dados['nome'],
                    dados['valor_cota'],
                    dados['total_cotas'],
                    dados['cotas_minimas'],
                    dados['probabilidade']
                )
                bolao.cotas_vendidas = dados['cotas_vendidas']
                
                # Adicionar números escolhidos e trevos
                numeros_aposta = {
                    'numeros': dados['numeros'],
                    'trevos': dados['trevos']
                }
                bolao.numeros_escolhidos = numeros_aposta
                bolao.estrategia_usada = "Análise Estatística Inteligente"
                
                # Definir status baseado nas cotas vendidas
                if bolao.cotas_vendidas >= bolao.cotas_minimas:
                    bolao.status = 'almost'
                else:
                    bolao.status = 'forming'
                
                db.session.add(bolao)
                print(f"✅ Criado bolão {dados['codigo']} - Milionária - Números: {dados['numeros']} Trevos: {dados['trevos']}")
            
            # Criar bolões da Lotofácil
            for dados in boloes_lotofacil:
                bolao = criar_bolao_lotofacil(
                    dados['codigo'],
                    dados['nome'],
                    dados['valor_cota'],
                    dados['total_cotas'],
                    dados['cotas_minimas'],
                    dados['probabilidade']
                )
                bolao.cotas_vendidas = dados['cotas_vendidas']
                
                # Adicionar números escolhidos
                numeros_aposta = {
                    'numeros': dados['numeros']
                }
                bolao.numeros_escolhidos = numeros_aposta
                bolao.estrategia_usada = "Análise Estatística Inteligente"
                
                # Definir status baseado nas cotas vendidas
                if bolao.cotas_vendidas >= bolao.cotas_minimas:
                    bolao.status = 'almost'
                else:
                    bolao.status = 'forming'
                
                db.session.add(bolao)
                print(f"✅ Criado bolão {dados['codigo']} - Lotofácil - Números: {dados['numeros']}")
            
            # Criar bolões da Mega Sena
            for dados in boloes_megasena:
                bolao = criar_bolao_megasena(
                    dados['codigo'],
                    dados['nome'],
                    dados['valor_cota'],
                    dados['total_cotas'],
                    dados['cotas_minimas'],
                    dados['probabilidade']
                )
                bolao.cotas_vendidas = dados['cotas_vendidas']
                
                # Adicionar números escolhidos
                numeros_aposta = {
                    'numeros': dados['numeros']
                }
                bolao.numeros_escolhidos = numeros_aposta
                bolao.estrategia_usada = "Análise Estatística Inteligente"
                
                # Definir status baseado nas cotas vendidas
                if bolao.cotas_vendidas >= bolao.cotas_minimas:
                    bolao.status = 'almost'
                else:
                    bolao.status = 'forming'
                
                db.session.add(bolao)
                print(f"✅ Criado bolão {dados['codigo']} - Mega Sena - Números: {dados['numeros']}")
            
            # Criar bolões da Quina
            for dados in boloes_quina:
                bolao = criar_bolao_quina(
                    dados['codigo'],
                    dados['nome'],
                    dados['valor_cota'],
                    dados['total_cotas'],
                    dados['cotas_minimas'],
                    dados['probabilidade']
                )
                bolao.cotas_vendidas = dados['cotas_vendidas']
                
                # Adicionar números escolhidos
                numeros_aposta = {
                    'numeros': dados['numeros']
                }
                bolao.numeros_escolhidos = numeros_aposta
                bolao.estrategia_usada = "Análise Estatística Inteligente"
                
                # Definir status baseado nas cotas vendidas
                if bolao.cotas_vendidas >= bolao.cotas_minimas:
                    bolao.status = 'almost'
                else:
                    bolao.status = 'forming'
                
                db.session.add(bolao)
                print(f"✅ Criado bolão {dados['codigo']} - Quina - Números: {dados['numeros']}")
            
            # Commit das alterações
            db.session.commit()
            
            print(f"\n🎉 Sucesso! Criados {len(boloes_milionaria + boloes_lotofacil + boloes_megasena + boloes_quina)} bolões iniciais")
            print("📊 Resumo:")
            print(f"   - Milionária: {len(boloes_milionaria)} bolões")
            print(f"   - Lotofácil: {len(boloes_lotofacil)} bolões")
            print(f"   - Mega Sena: {len(boloes_megasena)} bolões")
            print(f"   - Quina: {len(boloes_quina)} bolões")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao criar bolões: {e}")
            raise

if __name__ == "__main__":
    popular_boloes_iniciais()

