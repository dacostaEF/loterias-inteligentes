#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração de debug para Railway
"""

import os
import logging

def setup_debug_logging():
    """Configura logging detalhado para debug."""
    
    # Configuração de logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('debug.log')
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Log de ambiente
    logger.info("=== DEBUG CONFIG ATIVADO ===")
    logger.info(f"Python version: {os.sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Environment variables:")
    
    for key, value in os.environ.items():
        if any(keyword in key.upper() for keyword in ['PORT', 'FLASK', 'PYTHON', 'RAILWAY', 'DEBUG']):
            logger.info(f"  {key}: {value}")
    
    # Testa imports
    logger.info("=== TESTANDO IMPORTS ===")
    try:
        import flask
        logger.info("✅ Flask importado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao importar Flask: {e}")
    
    try:
        import pandas
        logger.info("✅ Pandas importado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao importar Pandas: {e}")
    
    try:
        import numpy
        logger.info("✅ Numpy importado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao importar Numpy: {e}")
    
    return logger

if __name__ == "__main__":
    setup_debug_logging()
