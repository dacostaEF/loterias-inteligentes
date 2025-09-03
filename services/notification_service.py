#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serviço de notificações (SMS e Email)
"""

import logging
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config.mercadopago_config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    SENDGRID_API_KEY,
    FROM_EMAIL
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    """Serviço para envio de notificações via SMS e Email."""
    
    def __init__(self):
        """Inicializar o serviço."""
        self.twilio_client = None
        self.sendgrid_client = None
        
        # Configurar Twilio se disponível
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            try:
                self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                logger.info("✅ Twilio configurado com sucesso")
            except Exception as e:
                logger.error(f"❌ Erro ao configurar Twilio: {str(e)}")
        
        # Configurar SendGrid se disponível
        if SENDGRID_API_KEY:
            try:
                self.sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)
                logger.info("✅ SendGrid configurado com sucesso")
            except Exception as e:
                logger.error(f"❌ Erro ao configurar SendGrid: {str(e)}")
    
    def enviar_sms_pagamento_aprovado(self, telefone, nome_usuario, plano_nome, valor):
        """
        Enviar SMS de confirmação de pagamento aprovado.
        
        Args:
            telefone (str): Número do telefone
            nome_usuario (str): Nome do usuário
            plano_nome (str): Nome do plano
            valor (float): Valor pago
            
        Returns:
            dict: Resultado do envio
        """
        if not self.twilio_client:
            logger.warning("⚠️ Twilio não configurado - SMS não enviado")
            return {"success": False, "error": "Twilio não configurado"}
        
        try:
            # Formatar telefone (adicionar +55 se necessário)
            if not telefone.startswith('+'):
                telefone = f"+55{telefone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')}"
            
            # Mensagem do SMS
            mensagem = f"""🎉 {nome_usuario}, seu pagamento foi aprovado!

✅ Plano: {plano_nome}
💰 Valor: R$ {valor:.2f}
🔓 Acesso liberado imediatamente!

Aproveite suas funcionalidades premium!
Loterias Inteligentes"""
            
            # Enviar SMS
            message = self.twilio_client.messages.create(
                body=mensagem,
                from_=TWILIO_PHONE_NUMBER,
                to=telefone
            )
            
            logger.info(f"✅ SMS enviado com sucesso para {telefone} - SID: {message.sid}")
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar SMS: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def enviar_email_pagamento_aprovado(self, email, nome_usuario, plano_nome, valor):
        """
        Enviar email de confirmação de pagamento aprovado.
        
        Args:
            email (str): Email do usuário
            nome_usuario (str): Nome do usuário
            plano_nome (str): Nome do plano
            valor (float): Valor pago
            
        Returns:
            dict: Resultado do envio
        """
        if not self.sendgrid_client:
            logger.warning("⚠️ SendGrid não configurado - Email não enviado")
            return {"success": False, "error": "SendGrid não configurado"}
        
        try:
            # Conteúdo do email
            subject = "🎉 Pagamento Aprovado - Loterias Inteligentes"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Pagamento Aprovado</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .success {{ color: #28a745; font-size: 24px; font-weight: bold; }}
                    .info {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745; }}
                    .button {{ display: inline-block; background: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Pagamento Aprovado!</h1>
                        <p>Loterias Inteligentes</p>
                    </div>
                    <div class="content">
                        <p>Olá <strong>{nome_usuario}</strong>,</p>
                        
                        <div class="success">✅ Seu pagamento foi aprovado com sucesso!</div>
                        
                        <div class="info">
                            <h3>📋 Detalhes do Pagamento:</h3>
                            <p><strong>Plano:</strong> {plano_nome}</p>
                            <p><strong>Valor:</strong> R$ {valor:.2f}</p>
                            <p><strong>Status:</strong> Aprovado</p>
                            <p><strong>Acesso:</strong> Liberado imediatamente</p>
                        </div>
                        
                        <p>🎯 Seu acesso às funcionalidades premium foi liberado! Agora você pode:</p>
                        <ul>
                            <li>✅ Acessar análises estatísticas avançadas</li>
                            <li>✅ Usar geradores inteligentes</li>
                            <li>✅ Visualizar relatórios detalhados</li>
                            <li>✅ Aproveitar todas as funcionalidades premium</li>
                        </ul>
                        
                        <p style="text-align: center; margin: 30px 0;">
                            <a href="http://localhost:5000" class="button">🚀 Acessar Agora</a>
                        </p>
                        
                        <p>Obrigado por escolher as Loterias Inteligentes!</p>
                        
                        <div class="footer">
                            <p>Este é um email automático. Não responda a esta mensagem.</p>
                            <p>Loterias Inteligentes - Sistema de Análise de Loterias</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Criar email
            message = Mail(
                from_email=FROM_EMAIL,
                to_emails=email,
                subject=subject,
                html_content=html_content
            )
            
            # Enviar email
            response = self.sendgrid_client.send(message)
            
            logger.info(f"✅ Email enviado com sucesso para {email} - Status: {response.status_code}")
            return {
                "success": True,
                "status_code": response.status_code,
                "message_id": response.headers.get('X-Message-Id')
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar email: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def enviar_confirmacao_plano_ativado(self, telefone, email, nome_usuario, plano_nome, valor):
        """
        Enviar confirmação completa (SMS + Email) de plano ativado.
        
        Args:
            telefone (str): Número do telefone
            email (str): Email do usuário
            nome_usuario (str): Nome do usuário
            plano_nome (str): Nome do plano
            valor (float): Valor pago
            
        Returns:
            dict: Resultado dos envios
        """
        resultados = {
            "sms": {"success": False},
            "email": {"success": False}
        }
        
        # Enviar SMS
        if telefone:
            resultados["sms"] = self.enviar_sms_pagamento_aprovado(
                telefone, nome_usuario, plano_nome, valor
            )
        
        # Enviar Email
        if email:
            resultados["email"] = self.enviar_email_pagamento_aprovado(
                email, nome_usuario, plano_nome, valor
            )
        
        # Verificar se pelo menos um foi enviado
        sucesso_total = resultados["sms"]["success"] or resultados["email"]["success"]
        
        return {
            "success": sucesso_total,
            "sms": resultados["sms"],
            "email": resultados["email"]
        }
    
    def enviar_notificacao_admin_pagamento(self, dados_pagamento):
        """
        Enviar notificação para o administrador sobre novo pagamento.
        
        Args:
            dados_pagamento (dict): Dados do pagamento
            
        Returns:
            dict: Resultado dos envios
        """
        try:
            # Dados do pagamento
            nome_usuario = dados_pagamento.get('nome_usuario', 'Usuário')
            email_usuario = dados_pagamento.get('email_usuario', '')
            telefone_usuario = dados_pagamento.get('telefone_usuario', '')
            plano_nome = dados_pagamento.get('plano_nome', '')
            valor = dados_pagamento.get('valor', 0)
            data_pagamento = dados_pagamento.get('data_pagamento', '')
            payment_id = dados_pagamento.get('payment_id', '')
            
            # Seus dados (você receberá as notificações)
            seu_telefone = "21981651234"  # Seu telefone
            seu_email = "dacosta_ef@hotmail.com"  # Seu email
            
            resultados = {
                "sms_admin": {"success": False},
                "email_admin": {"success": False}
            }
            
            # Enviar SMS para você
            if self.twilio_client:
                sms_result = self._enviar_sms_admin(
                    seu_telefone, nome_usuario, plano_nome, valor, payment_id
                )
                resultados["sms_admin"] = sms_result
            
            # Enviar Email para você
            if self.sendgrid_client:
                email_result = self._enviar_email_admin(
                    seu_email, dados_pagamento
                )
                resultados["email_admin"] = email_result
            
            # Verificar se pelo menos um foi enviado
            sucesso_total = resultados["sms_admin"]["success"] or resultados["email_admin"]["success"]
            
            logger.info(f"📨 Notificações para admin enviadas: {sucesso_total}")
            
            return {
                "success": sucesso_total,
                "sms_admin": resultados["sms_admin"],
                "email_admin": resultados["email_admin"]
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar notificações para admin: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _enviar_sms_admin(self, telefone_admin, nome_usuario, plano_nome, valor, payment_id):
        """Enviar SMS para o administrador."""
        try:
            # Formatar telefone
            if not telefone_admin.startswith('+'):
                telefone_admin = f"+55{telefone_admin.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')}"
            
            # Mensagem para você
            mensagem = f"""💰 NOVO PAGAMENTO RECEBIDO!

👤 Cliente: {nome_usuario}
📦 Plano: {plano_nome}
💵 Valor: R$ {valor:.2f}
🆔 ID: {payment_id}
⏰ Agora: {data_pagamento}

✅ Liberar acesso no sistema!
Loterias Inteligentes"""
            
            # Enviar SMS
            message = self.twilio_client.messages.create(
                body=mensagem,
                from_=TWILIO_PHONE_NUMBER,
                to=telefone_admin
            )
            
            logger.info(f"✅ SMS para admin enviado - SID: {message.sid}")
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar SMS para admin: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _enviar_email_admin(self, email_admin, dados_pagamento):
        """Enviar email para o administrador."""
        try:
            # Conteúdo do email para você
            subject = "💰 NOVO PAGAMENTO RECEBIDO - Loterias Inteligentes"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Novo Pagamento Recebido</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .alert {{ color: #28a745; font-size: 24px; font-weight: bold; }}
                    .info {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #28a745; }}
                    .button {{ display: inline-block; background: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>💰 NOVO PAGAMENTO RECEBIDO!</h1>
                        <p>Loterias Inteligentes - Admin</p>
                    </div>
                    <div class="content">
                        <div class="alert">✅ Pagamento Aprovado!</div>
                        
                        <div class="info">
                            <h3>📋 Detalhes do Pagamento:</h3>
                            <p><strong>👤 Cliente:</strong> {dados_pagamento.get('nome_usuario', 'N/A')}</p>
                            <p><strong>📧 Email:</strong> {dados_pagamento.get('email_usuario', 'N/A')}</p>
                            <p><strong>📱 Telefone:</strong> {dados_pagamento.get('telefone_usuario', 'N/A')}</p>
                            <p><strong>📦 Plano:</strong> {dados_pagamento.get('plano_nome', 'N/A')}</p>
                            <p><strong>💵 Valor:</strong> R$ {dados_pagamento.get('valor', 0):.2f}</p>
                            <p><strong>🆔 Payment ID:</strong> {dados_pagamento.get('payment_id', 'N/A')}</p>
                            <p><strong>⏰ Data:</strong> {dados_pagamento.get('data_pagamento', 'N/A')}</p>
                        </div>
                        
                        <p>🎯 <strong>AÇÃO NECESSÁRIA:</strong></p>
                        <ul>
                            <li>✅ Verificar pagamento no Mercado Pago</li>
                            <li>✅ Liberar acesso do usuário</li>
                            <li>✅ Ativar plano no sistema</li>
                            <li>✅ Confirmar funcionamento</li>
                        </ul>
                        
                        <p style="text-align: center; margin: 30px 0;">
                            <a href="https://www.mercadopago.com.br/developers" class="button">🔍 Verificar no Mercado Pago</a>
                        </p>
                        
                        <div class="footer">
                            <p>Este é um email automático do sistema de pagamentos.</p>
                            <p>Loterias Inteligentes - Sistema de Análise de Loterias</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Criar email
            message = Mail(
                from_email=FROM_EMAIL,
                to_emails=email_admin,
                subject=subject,
                html_content=html_content
            )
            
            # Enviar email
            response = self.sendgrid_client.send(message)
            
            logger.info(f"✅ Email para admin enviado - Status: {response.status_code}")
            return {
                "success": True,
                "status_code": response.status_code,
                "message_id": response.headers.get('X-Message-Id')
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar email para admin: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def testar_configuracao(self):
        """Testar se as configurações estão funcionando."""
        status = {
            "twilio": bool(self.twilio_client),
            "sendgrid": bool(self.sendgrid_client)
        }
        
        logger.info(f"📊 Status das configurações: {status}")
        return status

# Instância global do serviço
notification_service = NotificationService()
