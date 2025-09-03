#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serviço de integração com Mercado Pago
"""

import mercadopago
import logging
from datetime import datetime, timedelta
from config.mercadopago_config import (
    MERCADOPAGO_ACCESS_TOKEN,
    MERCADOPAGO_PUBLIC_KEY,
    MERCADOPAGO_SANDBOX,
    MERCADOPAGO_SUCCESS_URL,
    MERCADOPAGO_FAILURE_URL,
    MERCADOPAGO_PENDING_URL,
    PLANOS_MERCADOPAGO,
    METODOS_PAGAMENTO,
    CONFIGURACAO_PARCELAMENTO
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MercadoPagoService:
    """Serviço para integração com Mercado Pago."""
    
    def __init__(self):
        """Inicializar o serviço."""
        self.sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        self.public_key = MERCADOPAGO_PUBLIC_KEY
        self.sandbox = MERCADOPAGO_SANDBOX
        
        logger.info(f"🔧 MercadoPagoService inicializado - Sandbox: {self.sandbox}")
    
    def criar_preferencia_pagamento(self, plano_id, usuario_id, dados_usuario):
        """
        Criar preferência de pagamento no Mercado Pago.
        
        Args:
            plano_id (str): ID do plano selecionado
            usuario_id (int): ID do usuário
            dados_usuario (dict): Dados do usuário
            
        Returns:
            dict: Resposta do Mercado Pago com URL de pagamento
        """
        try:
            # Buscar dados do plano
            plano = PLANOS_MERCADOPAGO.get(plano_id)
            if not plano:
                raise ValueError(f"Plano {plano_id} não encontrado")
            
            # Preparar dados da preferência
            preference_data = {
                "items": [
                    {
                        "title": plano['nome'],
                        "description": plano['descricao'],
                        "quantity": 1,
                        "unit_price": plano['preco'],
                        "currency_id": "BRL"
                    }
                ],
                "payer": {
                    "name": dados_usuario.get('nome'),
                    "email": dados_usuario.get('email'),
                    "identification": {
                        "type": "CPF",
                        "number": dados_usuario.get('cpf', '').replace('.', '').replace('-', '')
                    },
                    "phone": {
                        "area_code": dados_usuario.get('telefone', '')[:2],
                        "number": dados_usuario.get('telefone', '')[2:]
                    }
                },
                "back_urls": {
                    "success": MERCADOPAGO_SUCCESS_URL,
                    "failure": MERCADOPAGO_FAILURE_URL,
                    "pending": MERCADOPAGO_PENDING_URL
                },
                "auto_return": "approved",
                "external_reference": f"usuario_{usuario_id}_plano_{plano_id}",
                "notification_url": "https://seu-dominio.com/webhook/mercadopago",
                "payment_methods": {
                    "excluded_payment_methods": [],
                    "excluded_payment_types": [],
                    "installments": CONFIGURACAO_PARCELAMENTO['max_parcelas']
                },
                "metadata": {
                    "usuario_id": usuario_id,
                    "plano_id": plano_id,
                    "plano_nome": plano['nome'],
                    "plano_preco": plano['preco'],
                    "duracao_dias": plano['duracao_dias']
                }
            }
            
            # Criar preferência
            logger.info(f"🔄 Criando preferência para usuário {usuario_id}, plano {plano_id}")
            result = self.sdk.preference().create(preference_data)
            
            if result["status"] == 201:
                logger.info(f"✅ Preferência criada com sucesso: {result['response']['id']}")
                return {
                    "success": True,
                    "preference_id": result["response"]["id"],
                    "init_point": result["response"]["init_point"],
                    "sandbox_init_point": result["response"]["sandbox_init_point"]
                }
            else:
                logger.error(f"❌ Erro ao criar preferência: {result}")
                return {
                    "success": False,
                    "error": "Erro ao criar preferência de pagamento"
                }
                
        except Exception as e:
            logger.error(f"❌ Erro no MercadoPagoService: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def verificar_pagamento(self, payment_id):
        """
        Verificar status de um pagamento.
        
        Args:
            payment_id (str): ID do pagamento
            
        Returns:
            dict: Status do pagamento
        """
        try:
            logger.info(f"🔍 Verificando pagamento: {payment_id}")
            result = self.sdk.payment().get(payment_id)
            
            if result["status"] == 200:
                payment = result["response"]
                return {
                    "success": True,
                    "payment_id": payment["id"],
                    "status": payment["status"],
                    "status_detail": payment["status_detail"],
                    "external_reference": payment["external_reference"],
                    "transaction_amount": payment["transaction_amount"],
                    "date_approved": payment.get("date_approved"),
                    "metadata": payment.get("metadata", {})
                }
            else:
                logger.error(f"❌ Erro ao verificar pagamento: {result}")
                return {
                    "success": False,
                    "error": "Erro ao verificar pagamento"
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ao verificar pagamento: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def processar_webhook(self, webhook_data):
        """
        Processar webhook do Mercado Pago.
        
        Args:
            webhook_data (dict): Dados do webhook
            
        Returns:
            dict: Resultado do processamento
        """
        try:
            # Extrair informações do webhook
            action = webhook_data.get("action")
            data_id = webhook_data.get("data", {}).get("id")
            
            logger.info(f"📨 Webhook recebido - Action: {action}, ID: {data_id}")
            
            if action == "payment.created":
                # Pagamento criado
                return self._processar_pagamento_criado(data_id)
            elif action == "payment.updated":
                # Pagamento atualizado
                return self._processar_pagamento_atualizado(data_id)
            else:
                logger.info(f"ℹ️ Ação não processada: {action}")
                return {"success": True, "message": "Ação não processada"}
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar webhook: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _processar_pagamento_criado(self, payment_id):
        """Processar pagamento criado."""
        logger.info(f"🆕 Processando pagamento criado: {payment_id}")
        return {"success": True, "message": "Pagamento criado processado"}
    
    def _processar_pagamento_atualizado(self, payment_id):
        """Processar pagamento atualizado."""
        logger.info(f"🔄 Processando pagamento atualizado: {payment_id}")
        
        # Verificar status do pagamento
        payment_info = self.verificar_pagamento(payment_id)
        
        if payment_info["success"]:
            status = payment_info["status"]
            
            if status == "approved":
                logger.info(f"✅ Pagamento aprovado: {payment_id}")
                return self._ativar_plano_usuario(payment_info)
            elif status == "rejected":
                logger.info(f"❌ Pagamento rejeitado: {payment_id}")
                return {"success": True, "message": "Pagamento rejeitado"}
            elif status == "pending":
                logger.info(f"⏳ Pagamento pendente: {payment_id}")
                return {"success": True, "message": "Pagamento pendente"}
            else:
                logger.info(f"ℹ️ Status não tratado: {status}")
                return {"success": True, "message": f"Status: {status}"}
        
        return payment_info
    
    def _ativar_plano_usuario(self, payment_info):
        """
        Ativar plano do usuário após pagamento aprovado.
        
        Args:
            payment_info (dict): Informações do pagamento
            
        Returns:
            dict: Resultado da ativação
        """
        try:
            metadata = payment_info.get("metadata", {})
            usuario_id = metadata.get("usuario_id")
            plano_id = metadata.get("plano_id")
            plano_nome = metadata.get("plano_nome")
            plano_preco = metadata.get("plano_preco")
            duracao_dias = metadata.get("duracao_dias")
            
            if not usuario_id or not plano_id:
                raise ValueError("Dados do usuário ou plano não encontrados")
            
            logger.info(f"🎯 Ativando plano {plano_id} para usuário {usuario_id}")
            
            # Aqui você implementaria a lógica para ativar o plano no banco de dados
            # Por exemplo:
            # - Atualizar status do usuário
            # - Definir data de expiração
            # - Registrar pagamento
            
            # Por enquanto, vamos simular a ativação
            logger.info(f"✅ Plano ativado com sucesso para usuário {usuario_id}")
            
            # Enviar notificações de confirmação
            self._enviar_notificacoes_confirmacao(
                usuario_id, plano_nome, plano_preco
            )
            
            # Enviar notificações para o administrador (você)
            self._enviar_notificacoes_admin(
                payment_info, plano_nome, plano_preco
            )
            
            return {
                "success": True,
                "message": "Plano ativado com sucesso",
                "usuario_id": usuario_id,
                "plano_id": plano_id,
                "plano_nome": plano_nome,
                "plano_preco": plano_preco,
                "duracao_dias": duracao_dias
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao ativar plano: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _enviar_notificacoes_confirmacao(self, usuario_id, plano_nome, plano_preco):
        """
        Enviar notificações de confirmação de pagamento.
        
        Args:
            usuario_id (int): ID do usuário
            plano_nome (str): Nome do plano
            plano_preco (float): Preço do plano
        """
        try:
            from services.notification_service import notification_service
            
            # Por enquanto, vamos usar dados de exemplo
            # Em produção, você buscaria os dados reais do usuário no banco de dados
            nome_usuario = "Usuário Teste"  # Buscar do banco
            telefone = "21981651234"  # Buscar do banco
            email = "dacosta_ef@hotmail.com"  # Buscar do banco
            
            logger.info(f"📨 Enviando notificações para usuário {usuario_id}")
            
            # Enviar confirmações
            resultado = notification_service.enviar_confirmacao_plano_ativado(
                telefone=telefone,
                email=email,
                nome_usuario=nome_usuario,
                plano_nome=plano_nome,
                valor=plano_preco
            )
            
            if resultado["success"]:
                logger.info(f"✅ Notificações enviadas com sucesso para usuário {usuario_id}")
            else:
                logger.warning(f"⚠️ Algumas notificações falharam para usuário {usuario_id}")
                
        except Exception as e:
            logger.error(f"❌ Erro ao enviar notificações: {str(e)}")
    
    def _enviar_notificacoes_admin(self, payment_info, plano_nome, plano_preco):
        """
        Enviar notificações para o administrador sobre novo pagamento.
        
        Args:
            payment_info (dict): Informações do pagamento
            plano_nome (str): Nome do plano
            plano_preco (float): Preço do plano
        """
        try:
            from services.notification_service import notification_service
            from datetime import datetime
            
            # Preparar dados para notificação
            dados_pagamento = {
                'nome_usuario': "Usuário Teste",  # Buscar do banco
                'email_usuario': "dacosta_ef@hotmail.com",  # Buscar do banco
                'telefone_usuario': "21981651234",  # Buscar do banco
                'plano_nome': plano_nome,
                'valor': plano_preco,
                'data_pagamento': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'payment_id': payment_info.get("payment_id", "N/A")
            }
            
            logger.info(f"📨 Enviando notificações para admin sobre pagamento {dados_pagamento['payment_id']}")
            
            # Enviar notificações para você
            resultado = notification_service.enviar_notificacao_admin_pagamento(dados_pagamento)
            
            if resultado["success"]:
                logger.info(f"✅ Notificações para admin enviadas com sucesso")
            else:
                logger.warning(f"⚠️ Algumas notificações para admin falharam")
                
        except Exception as e:
            logger.error(f"❌ Erro ao enviar notificações para admin: {str(e)}")
    
    def get_public_key(self):
        """Retornar chave pública para o frontend."""
        return self.public_key
    
    def is_sandbox(self):
        """Verificar se está em modo sandbox."""
        return self.sandbox
    
    def get_metodos_pagamento(self):
        """Retornar métodos de pagamento disponíveis."""
        return METODOS_PAGAMENTO
    
    def get_configuracao_parcelamento(self):
        """Retornar configuração de parcelamento."""
        return CONFIGURACAO_PARCELAMENTO
    
    def calcular_parcelas(self, valor, plano_id):
        """
        Calcular opções de parcelamento para um valor.
        
        Args:
            valor (float): Valor do plano
            plano_id (str): ID do plano
            
        Returns:
            list: Lista de opções de parcelamento
        """
        try:
            parcelas = []
            config = CONFIGURACAO_PARCELAMENTO
            max_parcelas = min(config['max_parcelas'], int(valor / config['minimo_parcela']))
            
            for i in range(1, max_parcelas + 1):
                valor_parcela = valor / i
                
                # Verificar se tem juros
                tem_juros = i > config['parcelas_sem_juros']
                juros = config['juros_parcelamento'] if tem_juros else 0
                
                if tem_juros and juros > 0:
                    valor_total = valor * (1 + juros)
                    valor_parcela = valor_total / i
                else:
                    valor_total = valor
                
                parcelas.append({
                    'parcelas': i,
                    'valor_parcela': round(valor_parcela, 2),
                    'valor_total': round(valor_total, 2),
                    'tem_juros': tem_juros,
                    'juros': juros,
                    'texto': f"{i}x de R$ {valor_parcela:.2f}" + (" (sem juros)" if not tem_juros else f" (com {juros*100:.1f}% de juros)")
                })
            
            return parcelas
            
        except Exception as e:
            logger.error(f"❌ Erro ao calcular parcelas: {str(e)}")
            return []

# Instância global do serviço
mercadopago_service = MercadoPagoService()
