#!/usr/bin/env python3
"""
Script para corrigir a estrutura do banco de dados dos bolões
"""

from app import app
from analytics_models import db
import sqlite3
import json
from datetime import datetime, timedelta

def fix_database_schema():
    """Corrige a estrutura da tabela boloes"""
    
    with app.app_context():
        print("🔧 Corrigindo estrutura do banco de dados...")
        
        # Conectar diretamente ao SQLite
        db_path = 'instance/li.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Verificar estrutura atual da tabela boloes
            cursor.execute("PRAGMA table_info(boloes)")
            colunas = cursor.fetchall()
            colunas_existentes = [col[1] for col in colunas]
            
            print(f"📋 Colunas existentes na tabela boloes: {colunas_existentes}")
            
            # Lista de colunas que devem existir
            colunas_necessarias = {
                'nivel': 'TEXT',
                'probabilidade': 'TEXT'
            }
            
            # Adicionar colunas ausentes
            for coluna, tipo in colunas_necessarias.items():
                if coluna not in colunas_existentes:
                    print(f"➕ Adicionando coluna: {coluna}")
                    cursor.execute(f"ALTER TABLE boloes ADD COLUMN {coluna} {tipo}")
                else:
                    print(f"✅ Coluna {coluna} já existe")
            
            # Commit das alterações
            conn.commit()
            print("✅ Estrutura da tabela atualizada!")
            
            # Agora vamos recriar os dados usando o SQLAlchemy
            print("\n🚀 Recriando dados dos bolões...")
            
            # Limpar dados antigos se existirem
            cursor.execute("DELETE FROM boloes")
            cursor.execute("DELETE FROM participantes_bolao WHERE 1=1")
            cursor.execute("DELETE FROM historico_boloes WHERE 1=1")
            conn.commit()
            
            # Fechar conexão SQLite para usar SQLAlchemy
            conn.close()
            
            # Importar modelos após correção
            from boloes_models import Bolao, HistoricoBolao
            
            # Dados dos bolões para criar
            boloes_dados = [
                # QUINA
                {
                    'codigo': 'LI-QN-007',
                    'nome': 'Grupo Inteligente QN-001',
                    'loteria': 'quina',
                    'nivel': 'basico',
                    'valor_cota': 8.00,
                    'total_cotas': 20,
                    'cotas_minimas': 15,
                    'cotas_vendidas': 18,
                    'status': 'almost',
                    'probabilidade': 'Alta',
                    'numeros': [12, 23, 34, 45, 67],
                    'estrategia': 'Análise Estatística Avançada'
                },
                {
                    'codigo': 'LI-QN-008',
                    'nome': 'Grupo Inteligente QN-002',
                    'loteria': 'quina',
                    'nivel': 'basico',
                    'valor_cota': 6.00,
                    'total_cotas': 25,
                    'cotas_minimas': 20,
                    'cotas_vendidas': 15,
                    'status': 'forming',
                    'probabilidade': 'Muito Alta',
                    'numeros': [12, 33, 34, 45, 67],
                    'estrategia': 'Padrões de Frequência'
                },
                # MEGA SENA
                {
                    'codigo': 'LI-MS-005',
                    'nome': 'Grupo Inteligente MS-001',
                    'loteria': 'megasena',
                    'nivel': 'intermediario',
                    'valor_cota': 25.00,
                    'total_cotas': 15,
                    'cotas_minimas': 12,
                    'cotas_vendidas': 14,
                    'status': 'almost',
                    'probabilidade': 'Alta',
                    'numeros': [7, 14, 23, 35, 42, 58],
                    'estrategia': 'IA + Machine Learning'
                },
                # LOTOFÁCIL
                {
                    'codigo': 'LI-LF-003',
                    'nome': 'Grupo Inteligente LF-001',
                    'loteria': 'lotofacil',
                    'nivel': 'basico',
                    'valor_cota': 12.00,
                    'total_cotas': 25,
                    'cotas_minimas': 20,
                    'cotas_vendidas': 22,
                    'status': 'almost',
                    'probabilidade': 'Muito Alta',
                    'numeros': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25],
                    'estrategia': 'Sequência Otimizada'
                },
                # MILIONÁRIA
                {
                    'codigo': 'LI-MF-004',
                    'nome': 'Grupo Inteligente MF-001',
                    'loteria': 'milionaria',
                    'nivel': 'master',
                    'valor_cota': 15.00,
                    'total_cotas': 20,
                    'cotas_minimas': 15,
                    'cotas_vendidas': 17,
                    'status': 'almost',
                    'probabilidade': 'Muito Alta',
                    'numeros': [7, 15, 23, 31, 42, 49],
                    'trevos': [2, 5],
                    'estrategia': 'Análise IA + Padrões Matemáticos'
                }
            ]
            
            # Criar cada bolão
            for dados in boloes_dados:
                try:
                    # Criar números em formato JSON
                    numeros_json = json.dumps({
                        'numeros': dados['numeros'],
                        'trevos': dados.get('trevos', [])
                    })
                    
                    # Calcular data de sorteio
                    if dados['loteria'] == 'megasena':
                        data_sorteio = datetime.now() + timedelta(days=3)
                    elif dados['loteria'] == 'quina':
                        data_sorteio = datetime.now() + timedelta(days=1)
                    elif dados['loteria'] == 'lotofacil':
                        data_sorteio = datetime.now() + timedelta(days=2)
                    else:  # milionaria
                        data_sorteio = datetime.now() + timedelta(days=5)
                    
                    # Criar bolão
                    bolao = Bolao(
                        codigo=dados['codigo'],
                        nome=dados['nome'],
                        loteria=dados['loteria'],
                        nivel=dados['nivel'],
                        valor_cota=dados['valor_cota'],
                        total_cotas=dados['total_cotas'],
                        cotas_minimas=dados['cotas_minimas'],
                        cotas_vendidas=dados['cotas_vendidas'],
                        status=dados['status'],
                        probabilidade=dados['probabilidade'],
                        numeros_escolhidos=numeros_json,
                        estrategia_usada=dados['estrategia'],
                        data_sorteio=data_sorteio,
                        ativo=True
                    )
                    
                    db.session.add(bolao)
                    db.session.flush()  # Para ter o ID
                    
                    # Criar entrada no histórico
                    historico = HistoricoBolao(
                        bolao_id=bolao.id,
                        usuario_id=1,  # Admin
                        acao='created',
                        descricao=f'Bolão {bolao.codigo} criado para {bolao.loteria}',
                        dados_extras=json.dumps({
                            'nivel': dados['nivel'],
                            'estrategia': dados['estrategia']
                        })
                    )
                    
                    db.session.add(historico)
                    
                    print(f"  ✅ {dados['codigo']} - {dados['nome']}")
                    print(f"     Números: {dados['numeros']}")
                    if 'trevos' in dados:
                        print(f"     Trevos: {dados['trevos']}")
                    print(f"     Cotas: {dados['cotas_vendidas']}/{dados['total_cotas']}")
                    print(f"     Status: {dados['status']}")
                    
                except Exception as e:
                    print(f"  ❌ Erro ao criar bolão {dados['codigo']}: {e}")
                    db.session.rollback()
                    return
            
            # Salvar tudo
            try:
                db.session.commit()
                print(f"\n🎉 Sucesso! Criados {len(boloes_dados)} bolões!")
                
                # Mostrar resumo
                for loteria in ['quina', 'megasena', 'lotofacil', 'milionaria']:
                    count = Bolao.query.filter(Bolao.loteria == loteria).count()
                    if count > 0:
                        print(f"   {loteria.title()}: {count} bolões")
                        
            except Exception as e:
                print(f"❌ Erro ao salvar: {e}")
                db.session.rollback()
                
        except Exception as e:
            print(f"❌ Erro ao corrigir estrutura: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()

if __name__ == "__main__":
    fix_database_schema()
