#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Boleto Simulado para Demonstração
"""

import logging
from datetime import datetime, timedelta
import random
import string

logger = logging.getLogger(__name__)

class BoletoSimulator:
    """Simulador de Boleto para demonstração."""
    
    def __init__(self):
        """Inicializar o simulador."""
        self.boletos = {}
    
    def gerar_boleto(self, dados_pagamento):
        """
        Gerar boleto simulado.
        
        Args:
            dados_pagamento (dict): Dados do pagamento
            
        Returns:
            dict: Resultado do boleto simulado
        """
        try:
            # Gerar ID único do boleto
            boleto_id = self._gerar_id_boleto()
            
            # Gerar código de barras simulado
            codigo_barras = self._gerar_codigo_barras(dados_pagamento)
            
            # Gerar linha digitável
            linha_digitavel = self._gerar_linha_digitavel(codigo_barras)
            
            # Criar dados do boleto
            boleto = {
                "id": boleto_id,
                "status": "pending",
                "valor": dados_pagamento['valor'],
                "descricao": dados_pagamento['descricao'],
                "codigo_barras": codigo_barras,
                "linha_digitavel": linha_digitavel,
                "data_criacao": datetime.now(),
                "data_vencimento": datetime.now() + timedelta(days=3),
                "cliente": {
                    "nome": dados_pagamento.get('nome', 'Cliente'),
                    "email": dados_pagamento['email'],
                    "cpf": dados_pagamento['cpf']
                }
            }
            
            # Salvar boleto
            self.boletos[boleto_id] = boleto
            
            logger.info(f"✅ Boleto simulado criado - ID: {boleto_id}")
            
            return {
                "success": True,
                "boleto_id": boleto_id,
                "status": "pending",
                "codigo_barras": codigo_barras,
                "linha_digitavel": linha_digitavel,
                "comprovante": self._gerar_comprovante_boleto(boleto),
                "boleto_data": {
                    "codigo_barras": codigo_barras,
                    "linha_digitavel": linha_digitavel,
                    "boleto_id": boleto_id
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no boleto simulado: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def verificar_boleto(self, boleto_id):
        """
        Verificar status do boleto.
        
        Args:
            boleto_id (str): ID do boleto
            
        Returns:
            dict: Status do boleto
        """
        if boleto_id not in self.boletos:
            return {
                "success": False,
                "error": "Boleto não encontrado"
            }
        
        boleto = self.boletos[boleto_id]
        
        # Simular pagamento aleatório (30% de chance)
        if boleto["status"] == "pending":
            if random.random() < 0.3:  # 30% de chance de pagamento
                boleto["status"] = "paid"
                boleto["data_pagamento"] = datetime.now()
                logger.info(f"✅ Boleto simulado pago - ID: {boleto_id}")
            else:
                boleto["status"] = "pending"
                logger.info(f"⏳ Boleto simulado ainda pendente - ID: {boleto_id}")
        
        return {
            "success": True,
            "boleto_id": boleto_id,
            "status": boleto["status"],
            "comprovante": self._gerar_comprovante_boleto(boleto)
        }
    
    def _gerar_id_boleto(self):
        """Gerar ID único do boleto."""
        return f"BOL_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
    
    def _gerar_codigo_barras(self, dados_pagamento):
        """Gerar código de barras simulado."""
        # Código de barras simulado (não é um código real)
        codigo = f"23791{random.randint(10000, 99999)}{random.randint(100000000000000000000000000000000000, 999999999999999999999999999999999999)}"
        
        # Adicionar dígito verificador simulado
        dv = random.randint(1, 9)
        codigo += str(dv)
        
        return codigo
    
    def _gerar_linha_digitavel(self, codigo_barras):
        """Gerar linha digitável do boleto."""
        # Linha digitável simulado (não é uma linha real)
        linha = f"23791.{random.randint(10000, 99999)} {random.randint(10000, 99999)}.{random.randint(100000000, 999999999)} {random.randint(10000, 99999)}.{random.randint(100000000, 999999999)} {random.randint(1, 9)} {codigo_barras[-14:]}"
        
        return linha
    
    def _gerar_comprovante_boleto(self, boleto):
        """Gerar comprovante de boleto."""
        try:
            comprovante = {
                "tipo": "BOLETO",
                "status": boleto["status"].upper(),
                "boleto_id": boleto["id"],
                "valor": boleto["valor"],
                "descricao": boleto["descricao"],
                "cliente": boleto["cliente"],
                "data_criacao": boleto["data_criacao"].strftime("%d/%m/%Y %H:%M:%S"),
                "data_vencimento": boleto["data_vencimento"].strftime("%d/%m/%Y"),
                "instrucoes": [
                    "1. Pague o boleto em qualquer banco ou lotérica",
                    "2. Use o código de barras ou linha digitável",
                    "3. Aguarde a confirmação (até 3 dias úteis)",
                    "4. Você receberá um email de confirmação"
                ],
                "observacoes": [
                    "• Boleto válido por 3 dias úteis",
                    "• Após o vencimento, será necessário gerar novo boleto",
                    "• Em caso de dúvidas, entre em contato conosco"
                ]
            }
            
            if boleto["status"] == "paid":
                comprovante["data_pagamento"] = boleto["data_pagamento"].strftime("%d/%m/%Y %H:%M:%S")
                comprovante["instrucoes"] = [
                    "✅ Boleto pago com sucesso!",
                    "✅ Seu plano foi ativado automaticamente",
                    "✅ Você receberá um email de confirmação",
                    "✅ Aproveite suas funcionalidades premium!"
                ]
            elif boleto["status"] == "pending":
                comprovante["instrucoes"] = [
                    "⏳ Boleto aguardando pagamento",
                    "⏳ Pague até a data de vencimento",
                    "⏳ Use o código de barras ou linha digitável",
                    "⏳ Confirmação em até 3 dias úteis"
                ]
            
            return comprovante
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar comprovante: {str(e)}")
            return {
                "tipo": "BOLETO",
                "status": "ERRO",
                "erro": str(e)
            }

# Instância global
boleto_simulator = BoletoSimulator()
















