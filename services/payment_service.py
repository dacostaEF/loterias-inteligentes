#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serviço de pagamento para Stripe e PagSeguro.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configurações
from config.payment_config import *

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaymentService:
    """Serviço para processamento de pagamentos."""
    
    def __init__(self):
        self.modo_teste = MODO_TESTE
        self.planos = PLANOS
    
    def criar_sessao_stripe(self, plano_id, usuario_id, usuario_email):
        """Cria uma sessão de pagamento no Stripe."""
        try:
            if self.modo_teste:
                # Modo teste - simular criação de sessão
                logger.info(f"🧪 [TESTE] Sessão Stripe criada para plano {plano_id}")
                return {
                    'success': True,
                    'session_id': f'test_session_{plano_id}_{usuario_id}',
                    'url': f'http://localhost:5000/pagamento/teste?plano={plano_id}',
                    'modo': 'teste'
                }
            
            # Modo produção - Stripe real
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY
            
            plano = self.planos.get(plano_id)
            if not plano:
                return {'success': False, 'error': 'Plano não encontrado'}
            
            # Criar sessão de checkout
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': STRIPE_CURRENCY,
                        'product_data': {
                            'name': f"Plano {plano['nome']} - Loterias Inteligentes",
                        },
                        'unit_amount': int(plano['preco'] * 100),  # Stripe usa centavos
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=STRIPE_SUCCESS_URL + f'?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=STRIPE_CANCEL_URL,
                customer_email=usuario_email,
                metadata={
                    'usuario_id': usuario_id,
                    'plano_id': plano_id
                }
            )
            
            logger.info(f"✅ Sessão Stripe criada: {session.id}")
            return {
                'success': True,
                'session_id': session.id,
                'url': session.url,
                'modo': 'producao'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar sessão Stripe: {e}")
            return {
                'success': False,
                'error': str(e),
                'modo': 'erro'
            }
    
    def criar_pagamento_pagseguro(self, plano_id, usuario_id, usuario_dados):
        """Cria um pagamento no PagSeguro."""
        try:
            if self.modo_teste:
                # Modo teste - simular criação de pagamento
                logger.info(f"🧪 [TESTE] Pagamento PagSeguro criado para plano {plano_id}")
                return {
                    'success': True,
                    'payment_id': f'test_payment_{plano_id}_{usuario_id}',
                    'url': f'http://localhost:5000/pagamento/teste?plano={plano_id}',
                    'modo': 'teste'
                }
            
            # Modo produção - PagSeguro real
            from pagseguro import PagSeguro
            
            plano = self.planos.get(plano_id)
            if not plano:
                return {'success': False, 'error': 'Plano não encontrado'}
            
            # Configurar PagSeguro
            pg = PagSeguro(
                email=PAGSEGURO_EMAIL,
                token=PAGSEGURO_TOKEN,
                sandbox=PAGSEGURO_SANDBOX
            )
            
            # Criar pagamento
            payment = pg.create_payment(
                id=f"plano_{plano_id}_{usuario_id}",
                description=f"Plano {plano['nome']} - Loterias Inteligentes",
                amount=plano['preco'],
                currency='BRL'
            )
            
            # Adicionar dados do comprador
            payment.sender = {
                'name': usuario_dados.get('nome', 'Usuário'),
                'email': usuario_dados.get('email'),
                'phone': usuario_dados.get('telefone'),
                'documents': [{
                    'type': 'CPF',
                    'value': usuario_dados.get('cpf')
                }]
            }
            
            # Processar pagamento
            response = payment.submit()
            
            logger.info(f"✅ Pagamento PagSeguro criado: {response.code}")
            return {
                'success': True,
                'payment_id': response.code,
                'url': response.payment_link,
                'modo': 'producao'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar pagamento PagSeguro: {e}")
            return {
                'success': False,
                'error': str(e),
                'modo': 'erro'
            }
    
    def validar_pagamento(self, payment_id, gateway='stripe'):
        """Valida se um pagamento foi aprovado."""
        try:
            if self.modo_teste:
                # Modo teste - simular validação
                logger.info(f"🧪 [TESTE] Pagamento {payment_id} validado")
                return {
                    'success': True,
                    'status': 'approved',
                    'amount': 29.90,
                    'modo': 'teste'
                }
            
            if gateway == 'stripe':
                return self._validar_stripe(payment_id)
            elif gateway == 'pagseguro':
                return self._validar_pagseguro(payment_id)
            else:
                return {'success': False, 'error': 'Gateway inválido'}
                
        except Exception as e:
            logger.error(f"❌ Erro ao validar pagamento: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _validar_stripe(self, session_id):
        """Valida pagamento no Stripe."""
        try:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY
            
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                return {
                    'success': True,
                    'status': 'approved',
                    'amount': session.amount_total / 100,
                    'customer_email': session.customer_email,
                    'metadata': session.metadata
                }
            else:
                return {
                    'success': False,
                    'status': session.payment_status
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ao validar Stripe: {e}")
            return {'success': False, 'error': str(e)}
    
    def _validar_pagseguro(self, transaction_id):
        """Valida pagamento no PagSeguro."""
        try:
            from pagseguro import PagSeguro
            
            pg = PagSeguro(
                email=PAGSEGURO_EMAIL,
                token=PAGSEGURO_TOKEN,
                sandbox=PAGSEGURO_SANDBOX
            )
            
            transaction = pg.get_transaction(transaction_id)
            
            if transaction.status == '3':  # Pago
                return {
                    'success': True,
                    'status': 'approved',
                    'amount': float(transaction.gross_amount),
                    'customer_email': transaction.sender.email
                }
            else:
                return {
                    'success': False,
                    'status': transaction.status
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ao validar PagSeguro: {e}")
            return {'success': False, 'error': str(e)}
    
    def ativar_plano_usuario(self, usuario_id, plano_id, payment_id):
        """Ativa o plano para o usuário após pagamento aprovado."""
        try:
            from database.db_config import get_db_connection
            
            conn = get_db_connection()
            if not conn: return False
            
            cursor = conn.cursor()
            
            # Calcular data de expiração
            plano = self.planos.get(plano_id)
            if not plano:
                return False
            
            data_abertura = datetime.now()
            
            if plano_id == 'daily':
                data_encerramento = data_abertura + timedelta(days=1)
            elif plano_id == 'monthly':
                data_encerramento = data_abertura + timedelta(days=30)
            elif plano_id == 'semestral':
                data_encerramento = data_abertura + timedelta(days=180)
            elif plano_id == 'annual':
                data_encerramento = data_abertura + timedelta(days=365)
            elif plano_id == 'lifetime':
                data_encerramento = None  # Vitalício
            else:
                data_encerramento = data_abertura + timedelta(days=30)
            
            # Atualizar usuário
            cursor.execute("""
                UPDATE usuarios 
                SET tipo_plano = ?, data_abertura = ?, data_encerramento = ?
                WHERE id = ?
            """, (plano_id, data_abertura, data_encerramento, usuario_id))
            
            # Registrar pagamento
            cursor.execute("""
                INSERT INTO pagamentos (usuario_id, plano_id, payment_id, status, valor, data_pagamento)
                VALUES (?, ?, ?, 'aprovado', ?, ?)
            """, (usuario_id, plano_id, payment_id, plano['preco'], data_abertura))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Plano {plano_id} ativado para usuário {usuario_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao ativar plano: {e}")
            if conn: conn.close()
            return False

# Instância global do serviço
payment_service = PaymentService()

if __name__ == '__main__':
    # Teste do serviço
    print("💳 TESTANDO SERVIÇO DE PAGAMENTO")
    print("=" * 40)
    
    # Teste criação de sessão
    print("\n🌍 Testando Stripe...")
    resultado_stripe = payment_service.criar_sessao_stripe('monthly', 1, 'teste@exemplo.com')
    print(f"Resultado Stripe: {resultado_stripe}")
    
    # Teste criação de pagamento
    print("\n🏦 Testando PagSeguro...")
    resultado_pagseguro = payment_service.criar_pagamento_pagseguro('monthly', 1, {
        'nome': 'João Silva',
        'email': 'teste@exemplo.com',
        'telefone': '21999999999',
        'cpf': '12345678901'
    })
    print(f"Resultado PagSeguro: {resultado_pagseguro}")

