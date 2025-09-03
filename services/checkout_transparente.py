#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serviço de Checkout Transparente do Mercado Pago
"""

import mercadopago
import logging
from datetime import datetime
from config.mercadopago_config import (
    MERCADOPAGO_ACCESS_TOKEN,
    MERCADOPAGO_PUBLIC_KEY,
    PLANOS_MERCADOPAGO
)

logger = logging.getLogger(__name__)

class CheckoutTransparente:
    """Serviço para Checkout Transparente do Mercado Pago."""
    
    def __init__(self):
        """Inicializar o serviço."""
        self.sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        self.public_key = MERCADOPAGO_PUBLIC_KEY
    
    def criar_pagamento_cartao(self, dados_pagamento):
        """
        Criar pagamento com cartão de crédito/débito.
        
        Args:
            dados_pagamento (dict): Dados do pagamento
            
        Returns:
            dict: Resultado do pagamento
        """
        try:
            # Preparar dados do pagamento
            payment_data = {
                "transaction_amount": dados_pagamento['valor'],
                "description": dados_pagamento['descricao'],
                "payment_method_id": dados_pagamento['metodo_pagamento'],
                "installments": dados_pagamento.get('parcelas', 1),
                "payer": {
                    "email": dados_pagamento['email'],
                    "identification": {
                        "type": "CPF",
                        "number": dados_pagamento['cpf']
                    }
                },
                "token": dados_pagamento['token'],
                "external_reference": dados_pagamento['external_reference']
            }
            
            # Criar pagamento
            result = self.sdk.payment().create(payment_data)
            
            if result["status"] == 201:
                # Gerar comprovante
                comprovante = self._gerar_comprovante_cartao(result["response"], dados_pagamento)
                
                return {
                    "success": True,
                    "payment_id": result["response"]["id"],
                    "status": result["response"]["status"],
                    "status_detail": result["response"]["status_detail"],
                    "comprovante": comprovante
                }
            else:
                return {
                    "success": False,
                    "error": "Erro ao processar pagamento"
                }
                
        except Exception as e:
            logger.error(f"❌ Erro no checkout transparente: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def criar_pagamento_pix(self, dados_pagamento):
        """
        Criar pagamento via PIX com QR Code.
        
        Args:
            dados_pagamento (dict): Dados do pagamento
            
        Returns:
            dict: Resultado do pagamento
        """
        try:
            # Preparar dados do pagamento PIX
            payment_data = {
                "transaction_amount": dados_pagamento['valor'],
                "description": dados_pagamento['descricao'],
                "payment_method_id": "pix",
                "payer": {
                    "email": dados_pagamento['email'],
                    "identification": {
                        "type": "CPF",
                        "number": dados_pagamento['cpf']
                    }
                },
                "external_reference": dados_pagamento['external_reference'],
                "notification_url": "https://seu-dominio.com/webhook/mercadopago"
            }
            
            # Criar pagamento
            result = self.sdk.payment().create(payment_data)
            
            if result["status"] == 201:
                payment_response = result["response"]
                
                # Extrair dados do PIX
                point_of_interaction = payment_response.get("point_of_interaction", {})
                transaction_data = point_of_interaction.get("transaction_data", {})
                
                qr_code = transaction_data.get("qr_code")
                qr_code_base64 = transaction_data.get("qr_code_base64")
                
                logger.info(f"✅ PIX criado - ID: {payment_response['id']}, Status: {payment_response['status']}")
                
                # Gerar comprovante
                comprovante = self._gerar_comprovante_pix(payment_response, dados_pagamento)
                
                return {
                    "success": True,
                    "payment_id": payment_response["id"],
                    "status": payment_response["status"],
                    "qr_code": qr_code,
                    "qr_code_base64": qr_code_base64,
                    "comprovante": comprovante,
                    "pix_data": {
                        "qr_code": qr_code,
                        "qr_code_base64": qr_code_base64,
                        "payment_id": payment_response["id"]
                    }
                }
            else:
                logger.error(f"❌ Erro ao criar PIX: {result}")
                return {
                    "success": False,
                    "error": "Erro ao processar pagamento PIX"
                }
                
        except Exception as e:
            logger.error(f"❌ Erro no PIX: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _gerar_comprovante_pix(self, payment_response, dados_pagamento):
        """
        Gerar comprovante de pagamento PIX.
        
        Args:
            payment_response (dict): Resposta do pagamento
            dados_pagamento (dict): Dados do pagamento
            
        Returns:
            dict: Dados do comprovante
        """
        try:
            from datetime import datetime
            
            # Dados do comprovante
            comprovante = {
                "tipo": "PIX",
                "status": "PENDENTE",
                "payment_id": payment_response["id"],
                "valor": dados_pagamento['valor'],
                "descricao": dados_pagamento['descricao'],
                "cliente": {
                    "nome": dados_pagamento.get('nome', 'Cliente'),
                    "email": dados_pagamento['email'],
                    "cpf": dados_pagamento['cpf']
                },
                "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "data_vencimento": (datetime.now() + timedelta(minutes=30)).strftime("%d/%m/%Y %H:%M:%S"),
                "instrucoes": [
                    "1. Escaneie o QR Code com seu app do banco",
                    "2. Confirme o pagamento no app",
                    "3. Aguarde a confirmação automática",
                    "4. Você receberá um email de confirmação"
                ],
                "observacoes": [
                    "• Pagamento válido por 30 minutos",
                    "• Após o vencimento, será necessário gerar novo PIX",
                    "• Em caso de dúvidas, entre em contato conosco"
                ]
            }
            
            logger.info(f"✅ Comprovante PIX gerado para pagamento {payment_response['id']}")
            return comprovante
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar comprovante: {str(e)}")
            return {
                "tipo": "PIX",
                "status": "ERRO",
                "erro": str(e)
            }
    
    def _gerar_comprovante_cartao(self, payment_response, dados_pagamento):
        """
        Gerar comprovante de pagamento com cartão.
        
        Args:
            payment_response (dict): Resposta do pagamento
            dados_pagamento (dict): Dados do pagamento
            
        Returns:
            dict: Dados do comprovante
        """
        try:
            from datetime import datetime
            
            # Dados do comprovante
            comprovante = {
                "tipo": "CARTÃO",
                "status": payment_response["status"],
                "payment_id": payment_response["id"],
                "valor": dados_pagamento['valor'],
                "descricao": dados_pagamento['descricao'],
                "cliente": {
                    "nome": dados_pagamento.get('nome', 'Cliente'),
                    "email": dados_pagamento['email'],
                    "cpf": dados_pagamento['cpf']
                },
                "cartao": {
                    "ultimos_digitos": "****",
                    "bandeira": "Visa/Mastercard",
                    "parcelas": dados_pagamento.get('parcelas', 1)
                },
                "data_pagamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "instrucoes": [
                    "1. Pagamento processado com sucesso",
                    "2. Você receberá um email de confirmação",
                    "3. Seu plano foi ativado automaticamente",
                    "4. Aproveite suas funcionalidades premium!"
                ]
            }
            
            logger.info(f"✅ Comprovante cartão gerado para pagamento {payment_response['id']}")
            return comprovante
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar comprovante: {str(e)}")
            return {
                "tipo": "CARTÃO",
                "status": "ERRO",
                "erro": str(e)
            }

# Instância global
checkout_transparente = CheckoutTransparente()
