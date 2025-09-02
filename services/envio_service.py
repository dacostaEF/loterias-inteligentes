#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Serviço de envio real de SMS e Email com códigos de confirmação.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar configurações
from config.env_config import *

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnvioService:
    """Serviço para envio de SMS e Email."""
    
    def __init__(self):
        self.modo_teste = MODO_TESTE
        self.numero_teste = NUMERO_TESTE_SMS
        self.email_teste = EMAIL_TESTE
    
    def enviar_sms(self, numero, codigo, nome_usuario="Usuário"):
        """Envia SMS com código de confirmação."""
        try:
            if self.modo_teste:
                # Modo teste - simular envio
                logger.info(f"🧪 [TESTE] SMS enviado para {numero}: Código {codigo}")
                return {
                    'success': True,
                    'message': f'SMS de teste enviado para {numero}',
                    'codigo': codigo,
                    'modo': 'teste'
                }
            
            # Modo produção - Twilio
            from twilio.rest import Client
            
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            
            mensagem = f"""
🎯 Loterias Inteligentes

Olá {nome_usuario}!

Seu código de confirmação é: {codigo}

Este código expira em 10 minutos.

Não compartilhe este código com ninguém.
            """.strip()
            
            message = client.messages.create(
                body=mensagem,
                from_=TWILIO_PHONE_NUMBER,
                to=numero
            )
            
            logger.info(f"✅ SMS enviado via Twilio: {message.sid}")
            return {
                'success': True,
                'message': 'SMS enviado com sucesso',
                'codigo': codigo,
                'sid': message.sid,
                'modo': 'producao'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar SMS: {e}")
            return {
                'success': False,
                'error': str(e),
                'modo': 'erro'
            }
    
    def enviar_email(self, email, codigo, nome_usuario="Usuário"):
        """Envia Email com código de confirmação."""
        try:
            if self.modo_teste:
                # Modo teste - simular envio
                logger.info(f"🧪 [TESTE] Email enviado para {email}: Código {codigo}")
                return {
                    'success': True,
                    'message': f'Email de teste enviado para {email}',
                    'codigo': codigo,
                    'modo': 'teste'
                }
            
            # Modo produção - SendGrid
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Confirmação de Cadastro - Loterias Inteligentes</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .codigo {{ background: #667eea; color: white; font-size: 32px; font-weight: bold; text-align: center; padding: 20px; margin: 20px 0; border-radius: 10px; letter-spacing: 5px; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎯 Loterias Inteligentes</h1>
                        <p>Confirmação de Cadastro</p>
                    </div>
                    <div class="content">
                        <h2>Olá {nome_usuario}!</h2>
                        <p>Obrigado por se cadastrar em nossa plataforma. Para ativar sua conta, use o código de confirmação abaixo:</p>
                        
                        <div class="codigo">{codigo}</div>
                        
                        <p><strong>Este código expira em 10 minutos.</strong></p>
                        <p>Se você não solicitou este cadastro, ignore este email.</p>
                        
                        <div class="footer">
                            <p>© 2024 Loterias Inteligentes - Todos os direitos reservados</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            message = Mail(
                from_email=SENDGRID_FROM_EMAIL,
                to_emails=email,
                subject='🎯 Confirmação de Cadastro - Loterias Inteligentes',
                html_content=html_content
            )
            
            response = sg.send(message)
            
            logger.info(f"✅ Email enviado via SendGrid: {response.status_code}")
            return {
                'success': True,
                'message': 'Email enviado com sucesso',
                'codigo': codigo,
                'status_code': response.status_code,
                'modo': 'producao'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao enviar Email: {e}")
            return {
                'success': False,
                'error': str(e),
                'modo': 'erro'
            }
    
    def enviar_codigo_confirmacao(self, usuario_id, tipo, destinatario, nome_usuario="Usuário"):
        """Envia código de confirmação por SMS ou Email."""
        try:
            # Gerar código
            from database.db_config import gerar_codigo_confirmacao
            codigo = gerar_codigo_confirmacao(usuario_id, tipo)
            
            if not codigo:
                return {
                    'success': False,
                    'error': 'Erro ao gerar código de confirmação'
                }
            
            # Enviar código
            if tipo == 'sms':
                resultado = self.enviar_sms(destinatario, codigo, nome_usuario)
            elif tipo == 'email':
                resultado = self.enviar_email(destinatario, codigo, nome_usuario)
            else:
                return {
                    'success': False,
                    'error': 'Tipo de envio inválido'
                }
            
            # Log do envio
            self._log_envio(usuario_id, tipo, destinatario, resultado)
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro no envio de código: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _log_envio(self, usuario_id, tipo, destinatario, resultado):
        """Registra log do envio no banco."""
        try:
            from database.db_config import get_db_connection
            
            conn = get_db_connection()
            if not conn: return
            
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO logs_envio (usuario_id, tipo, destinatario, status, resposta, data_envio)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                usuario_id,
                tipo,
                destinatario,
                'sucesso' if resultado.get('success') else 'erro',
                json.dumps(resultado),
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"❌ Erro ao registrar log: {e}")

# Instância global do serviço
envio_service = EnvioService()

if __name__ == '__main__':
    # Teste do serviço
    print("🧪 TESTANDO SERVIÇO DE ENVIO")
    print("=" * 40)
    
    # Teste SMS
    print("\n📱 Testando SMS...")
    resultado_sms = envio_service.enviar_sms("21981651234", "123456", "João Silva")
    print(f"Resultado SMS: {resultado_sms}")
    
    # Teste Email
    print("\n📧 Testando Email...")
    resultado_email = envio_service.enviar_email("dacosta_ef@hotmail.com", "123456", "João Silva")
    print(f"Resultado Email: {resultado_email}")

