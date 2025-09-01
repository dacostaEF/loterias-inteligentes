#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotas de autenticação Firebase para Loterias Inteligentes
"""

from flask import Blueprint, request, jsonify
from flask_login import login_user
from database.db_config import (
    get_user_by_google_id, update_user_last_login, create_user as db_create_user
)
from app import User, UserLevel
import logging

logger = logging.getLogger(__name__)

# Criar blueprint para rotas Firebase
firebase_bp = Blueprint('firebase', __name__)

@firebase_bp.route('/auth/google/firebase', methods=['POST'])
def firebase_google_auth():
    """Recebe dados de autenticação do Firebase e cria/autentica usuário."""
    try:
        data = request.get_json()
        google_id = data.get('google_id')
        email = data.get('email')
        nome_completo = data.get('nome_completo')
        foto_url = data.get('foto_url')
        
        if not all([google_id, email, nome_completo]):
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400
        
        logger.info(f"Autenticação Firebase recebida: {email}")
        
        # Verificar se usuário já existe no banco
        existing_user = get_user_by_google_id(google_id)
        
        if existing_user:
            # Usuário existente - fazer login
            user_id = existing_user['id']
            logger.info(f"Usuário existente fazendo login: {email}")
            
            # Atualizar informações se necessário
            if existing_user['nome_completo'] != nome_completo:
                from database.db_config import get_db_connection
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE usuarios SET nome_completo = ? WHERE id = ?", (nome_completo, user_id))
                    conn.commit()
                    conn.close()
            
            # Buscar plano atual
            plano_nome = existing_user['plano_nome'] if existing_user['plano_nome'] else 'Free'
            
            level_mapping = {
                'Free': UserLevel.FREE,
                'Diário': UserLevel.PREMIUM_DAILY,
                'Mensal': UserLevel.PREMIUM_MONTHLY,
                'Semestral': UserLevel.PREMIUM_SEMESTRAL,
                'Anual': UserLevel.PREMIUM_ANNUAL,
                'Vitalício': UserLevel.LIFETIME
            }
            
            user_level = level_mapping.get(plano_nome, UserLevel.FREE)
            
        else:
            # Usuário novo - criar no banco
            logger.info(f"Criando novo usuário Google: {email}")
            
            user_id = db_create_user(
                nome_completo=nome_completo,
                email=email,
                senha_hash=None,
                google_id=google_id,
                foto_url=foto_url
            )
            
            if not user_id:
                logger.error(f"Erro ao criar usuário: {email}")
                return jsonify({'success': False, 'error': 'Erro ao criar usuário'}), 500
            
            user_level = UserLevel.FREE
            logger.info(f"Novo usuário Google criado: {email} - ID: {user_id}")
        
        # Atualizar último login
        update_user_last_login(user_id)
        
        # Criar objeto User e fazer login
        user = User(user_id, email, user_level)
        user.google_id = google_id  # Adicionar Google ID ao objeto
        login_user(user)
        
        logger.info(f"Login Google bem-sucedido: {email}")
        
        return jsonify({'success': True, 'message': 'Usuário autenticado com sucesso'})
        
    except Exception as e:
        logger.error(f"Erro na autenticação Firebase: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500



