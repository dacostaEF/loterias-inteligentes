#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de PIX Simulado para Demonstração
"""

import qrcode
import base64
import io
import logging
from datetime import datetime, timedelta
import random
import string

logger = logging.getLogger(__name__)

class PIXSimulator:
    """Simulador de PIX para demonstração."""
    
    def __init__(self):
        """Inicializar o simulador."""
        self.pagamentos = {}
    
    def gerar_pix(self, dados_pagamento):
        """
        Gerar PIX simulado com QR Code.
        
        Args:
            dados_pagamento (dict): Dados do pagamento
            
        Returns:
            dict: Resultado do PIX simulado
        """
        try:
            # Gerar ID único do pagamento
            payment_id = self._gerar_id_pagamento()
            
            # Gerar código PIX simulado
            pix_code = self._gerar_codigo_pix(dados_pagamento)
            
            # Gerar QR Code
            qr_code_base64 = self._gerar_qr_code(pix_code)
            
            # Criar dados do pagamento
            pagamento = {
                "id": payment_id,
                "status": "pending",
                "valor": dados_pagamento['valor'],
                "descricao": dados_pagamento['descricao'],
                "pix_code": pix_code,
                "qr_code_base64": qr_code_base64,
                "data_criacao": datetime.now(),
                "data_vencimento": datetime.now() + timedelta(minutes=30),
                "cliente": {
                    "nome": dados_pagamento.get('nome', 'Cliente'),
                    "email": dados_pagamento['email'],
                    "cpf": dados_pagamento['cpf']
                }
            }
            
            # Salvar pagamento
            self.pagamentos[payment_id] = pagamento
            
            logger.info(f"✅ PIX simulado criado - ID: {payment_id}")
            
            return {
                "success": True,
                "payment_id": payment_id,
                "status": "pending",
                "qr_code": pix_code,
                "qr_code_base64": qr_code_base64,
                "comprovante": self._gerar_comprovante_pix(pagamento),
                "pix_data": {
                    "qr_code": pix_code,
                    "qr_code_base64": qr_code_base64,
                    "payment_id": payment_id
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no PIX simulado: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def verificar_pagamento(self, payment_id):
        """
        Verificar status do pagamento.
        
        Args:
            payment_id (str): ID do pagamento
            
        Returns:
            dict: Status do pagamento
        """
        if payment_id not in self.pagamentos:
            return {
                "success": False,
                "error": "Pagamento não encontrado"
            }
        
        pagamento = self.pagamentos[payment_id]
        
        # Simular aprovação aleatória (70% de chance)
        if pagamento["status"] == "pending":
            if random.random() < 0.7:  # 70% de chance de aprovação
                pagamento["status"] = "approved"
                pagamento["data_aprovacao"] = datetime.now()
                logger.info(f"✅ PIX simulado aprovado - ID: {payment_id}")
            else:
                pagamento["status"] = "rejected"
                pagamento["data_rejeicao"] = datetime.now()
                logger.info(f"❌ PIX simulado rejeitado - ID: {payment_id}")
        
        return {
            "success": True,
            "payment_id": payment_id,
            "status": pagamento["status"],
            "comprovante": self._gerar_comprovante_pix(pagamento)
        }
    
    def _gerar_id_pagamento(self):
        """Gerar ID único do pagamento."""
        return f"PIX_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
    
    def _gerar_codigo_pix(self, dados_pagamento):
        """Gerar código PIX simulado."""
        # Código PIX simulado (não é um código real)
        codigo = f"00020126580014br.gov.bcb.pix0136{random.randint(100000000000000000000000000000000000, 999999999999999999999999999999999999)}5204000053039865405{float(dados_pagamento['valor']):.2f}5802BR5913LOTERIAS INTEL6014SAO PAULO62070503***6304"
        
        # Adicionar checksum simulado
        checksum = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        codigo += checksum
        
        return codigo
    
    def _gerar_qr_code(self, pix_code):
        """Gerar QR Code em base64."""
        try:
            # Criar QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(pix_code)
            qr.make(fit=True)
            
            # Criar imagem
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Converter para base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar QR Code: {str(e)}")
            return None
    
    def _gerar_comprovante_pix(self, pagamento):
        """Gerar comprovante de pagamento PIX."""
        try:
            comprovante = {
                "tipo": "PIX",
                "status": pagamento["status"].upper(),
                "payment_id": pagamento["id"],
                "valor": pagamento["valor"],
                "descricao": pagamento["descricao"],
                "cliente": pagamento["cliente"],
                "data_criacao": pagamento["data_criacao"].strftime("%d/%m/%Y %H:%M:%S"),
                "data_vencimento": pagamento["data_vencimento"].strftime("%d/%m/%Y %H:%M:%S"),
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
            
            if pagamento["status"] == "approved":
                comprovante["data_aprovacao"] = pagamento["data_aprovacao"].strftime("%d/%m/%Y %H:%M:%S")
                comprovante["instrucoes"] = [
                    "✅ Pagamento aprovado com sucesso!",
                    "✅ Seu plano foi ativado automaticamente",
                    "✅ Você receberá um email de confirmação",
                    "✅ Aproveite suas funcionalidades premium!"
                ]
            elif pagamento["status"] == "rejected":
                comprovante["instrucoes"] = [
                    "❌ Pagamento rejeitado",
                    "❌ Verifique os dados e tente novamente",
                    "❌ Em caso de dúvidas, entre em contato conosco"
                ]
            
            return comprovante
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar comprovante: {str(e)}")
            return {
                "tipo": "PIX",
                "status": "ERRO",
                "erro": str(e)
            }

# Instância global
pix_simulator = PIXSimulator()














