#!/usr/bin/env python3
"""
Script para popular bolões com nova estrutura LI
Loterias Inteligentes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # Importar o app para ter contexto
from analytics_models import db
from boloes_models import (
    Bolao, ParticipanteBolao, HistoricoBolao,
    criar_bolao_inteligente, gerar_codigo_bolao
)
from datetime import datetime, timedelta


def popular_boloes_iniciais():
    """Popula o banco com bolões iniciais usando códigos LI"""
    
    with app.app_context():  # Criar contexto da aplicação
        print("🚀 Criando tabelas...")
        try:
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            return
        
        print("\n🎯 Criando bolões com códigos Loterias Inteligentes...")
        
        # MILIONÁRIA - 3 níveis
        boloes_milionaria = [
        {
            'nivel': 'basico',
            'nome': 'Grupo Básico Milionária',
            'valor_cota': 12.00,
            'total_cotas': 20,
            'cotas_minimas': 15,
            'cotas_vendidas': 8,
            'numeros': [7, 15, 23, 31, 42, 49],
            'trevos': [2, 5],
            'estrategia': 'Números mais sorteados + análise básica'
        },
        {
            'nivel': 'intermediario',
            'nome': 'Grupo Intermediário Milionária',
            'valor_cota': 18.00,
            'total_cotas': 15,
            'cotas_minimas': 12,
            'cotas_vendidas': 13,
            'numeros': [9, 14, 21, 28, 35, 47],
            'trevos': [1, 4],
            'estrategia': 'Padrões matemáticos + sequências otimizadas'
        },
        {
            'nivel': 'master',
            'nome': 'Grupo Master Milionária',
            'valor_cota': 25.00,
            'total_cotas': 12,
            'cotas_minimas': 10,
            'cotas_vendidas': 11,
            'numeros': [3, 11, 19, 27, 38, 44],
            'trevos': [3, 6],
            'estrategia': 'IA + Machine Learning + análise completa'
        }
    ]
    
    # LOTOFÁCIL - 3 níveis
    boloes_lotofacil = [
        {
            'nivel': 'basico',
            'nome': 'Grupo Básico Lotofácil',
            'valor_cota': 8.00,
            'total_cotas': 25,
            'cotas_minimas': 20,
            'cotas_vendidas': 22,
            'numeros': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
            'estrategia': 'Sequência ímpar clássica'
        },
        {
            'nivel': 'intermediario',
            'nome': 'Grupo Intermediário Lotofácil',
            'valor_cota': 12.00,
            'total_cotas': 20,
            'cotas_minimas': 15,
            'cotas_vendidas': 18,
            'numeros': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25],
            'estrategia': 'Análise de frequência e distribuição'
        },
        {
            'nivel': 'master',
            'nome': 'Grupo Master Lotofácil',
            'valor_cota': 15.00,
            'total_cotas': 18,
            'cotas_minimas': 12,
            'cotas_vendidas': 16,
            'numeros': [1, 4, 7, 10, 13, 16, 19, 22, 25, 3, 6, 9, 12],
            'estrategia': 'IA preditiva + padrões avançados'
        }
    ]
    
    # MEGA SENA - 3 níveis  
    boloes_megasena = [
        {
            'nivel': 'basico',
            'nome': 'Grupo Básico Mega Sena',
            'valor_cota': 10.00,
            'total_cotas': 18,
            'cotas_minimas': 15,
            'cotas_vendidas': 16,
            'numeros': [9, 18, 27, 35, 42, 58],
            'estrategia': 'Números quentes + análise básica'
        },
        {
            'nivel': 'intermediario',
            'nome': 'Grupo Intermediário Mega Sena',
            'valor_cota': 15.00,
            'total_cotas': 15,
            'cotas_minimas': 12,
            'cotas_vendidas': 14,
            'numeros': [5, 14, 23, 32, 46, 55],
            'estrategia': 'Distribuição otimizada por dezenas'
        },
        {
            'nivel': 'master',
            'nome': 'Grupo Master Mega Sena',
            'valor_cota': 20.00,
            'total_cotas': 12,
            'cotas_minimas': 10,
            'cotas_vendidas': 11,
            'numeros': [7, 16, 29, 38, 47, 59],
            'estrategia': 'Algoritmo inteligente + predição IA'
        }
    ]
    
    # QUINA - 3 níveis
    boloes_quina = [
        {
            'nivel': 'basico',
            'nome': 'Grupo Básico Quina',
            'valor_cota': 6.00,
            'total_cotas': 30,
            'cotas_minimas': 25,
            'cotas_vendidas': 28,
            'numeros': [12, 23, 34, 45, 67],
            'estrategia': 'Números equilibrados por faixa'
        },
        {
            'nivel': 'intermediario',
            'nome': 'Grupo Intermediário Quina',
            'valor_cota': 9.00,
            'total_cotas': 25,
            'cotas_minimas': 20,
            'cotas_vendidas': 23,
            'numeros': [8, 19, 26, 37, 54],
            'estrategia': 'Análise de padrões e sequências'
        },
        {
            'nivel': 'master',
            'nome': 'Grupo Master Quina',
            'valor_cota': 12.00,
            'total_cotas': 20,
            'cotas_minimas': 15,
            'cotas_vendidas': 19,
            'numeros': [3, 15, 28, 41, 69],
            'estrategia': 'Sistema inteligente de predição'
        }
    ]
    
    # Criar bolões para cada loteria
    loterias_data = [
        ('milionaria', boloes_milionaria),
        ('lotofacil', boloes_lotofacil),
        ('megasena', boloes_megasena),
        ('quina', boloes_quina)
    ]
    
    for loteria, dados_boloes in loterias_data:
        print(f"\n🎲 Criando bolões para {loteria.upper()}:")
        
        for dados in dados_boloes:
            try:
                # Criar bolão
                bolao = criar_bolao_inteligente(
                    loteria=loteria,
                    nivel=dados['nivel'],
                    nome=dados['nome'],
                    valor_cota=dados['valor_cota'],
                    total_cotas=dados['total_cotas'],
                    cotas_minimas=dados['cotas_minimas'],
                    numeros=dados['numeros'],
                    trevos=dados.get('trevos'),
                    estrategia=dados['estrategia']
                )
                
                # Definir cotas vendidas
                bolao.cotas_vendidas = dados['cotas_vendidas']
                
                # Definir data de sorteio (próximos dias)
                if loteria == 'megasena':
                    # Próxima quarta ou sábado
                    bolao.data_sorteio = datetime.now() + timedelta(days=3)
                elif loteria == 'lotofacil':
                    # Segunda a sábado
                    bolao.data_sorteio = datetime.now() + timedelta(days=1)
                elif loteria == 'quina':
                    # Segunda a sábado
                    bolao.data_sorteio = datetime.now() + timedelta(days=2)
                elif loteria == 'milionaria':
                    # Quarta e sábado
                    bolao.data_sorteio = datetime.now() + timedelta(days=4)
                
                db.session.add(bolao)
                db.session.commit()
                
                print(f"  ✅ {bolao.codigo} - {bolao.nome}")
                print(f"     Números: {bolao.get_numeros_escolhidos()}")
                if bolao.get_trevos_escolhidos():
                    print(f"     Trevos: {bolao.get_trevos_escolhidos()}")
                print(f"     Cotas: {bolao.cotas_vendidas}/{bolao.total_cotas}")
                print(f"     Valor/cota: R$ {bolao.valor_cota}")
                
                # Registrar no histórico
                historico = HistoricoBolao(
                    bolao_id=bolao.id,
                    usuario_id=1,  # Admin
                    acao='criado',
                    descricao=f'Bolão {bolao.codigo} criado para {loteria}',
                    dados_extras=f'{{"nivel": "{dados["nivel"]}", "estrategia": "{dados["estrategia"]}"}}'
                )
                db.session.add(historico)
                
            except Exception as e:
                print(f"  ❌ Erro ao criar bolão {dados['nivel']}: {e}")
                db.session.rollback()
    
    try:
        db.session.commit()
        print(f"\n🎉 Sucesso! Bolões criados com códigos Loterias Inteligentes!")
        
        # Mostrar resumo
        total_boloes = Bolao.query.count()
        print(f"\n📊 RESUMO:")
        print(f"   Total de bolões: {total_boloes}")
        
        for loteria in ['milionaria', 'lotofacil', 'megasena', 'quina']:
            count = Bolao.query.filter(Bolao.loteria == loteria).count()
            print(f"   {loteria.title()}: {count} bolões")
            
    except Exception as e:
        print(f"❌ Erro final: {e}")
        db.session.rollback()


if __name__ == "__main__":
    popular_boloes_iniciais()
