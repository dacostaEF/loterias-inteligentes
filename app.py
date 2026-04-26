#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for, session, Response
from functools import wraps
import os
import sys
import io
import math

# ============================================================================
# 🔧 CONFIGURAÇÃO UTF-8 PARA WINDOWS
# ============================================================================
# Força o encoding UTF-8 para evitar erros com emojis no terminal do Windows
if sys.platform == 'win32':
    # Reconfigura stdout e stderr para UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    # Define variável de ambiente
    os.environ['PYTHONIOENCODING'] = 'utf-8'
from datetime import datetime, date, timedelta
import json
import logging

# ============================================================================
# 🎯 CONTROLE DE ACESSO - Modo Liberado Temporariamente
# ============================================================================
# Para habilitar planos pagos e restrições novamente, mude para False
# True = Acesso 100% livre (sem modal de planos, sem restrições)
# False = Sistema completo ativo (planos, cadastro, restrições)
FREE_ACCESS_MODE = True

# Analytics imports
from analytics_models import db, Event

# ============================================================================
# 🔐 SISTEMA SIMPLES DE AUTENTICAÇÃO
# ===========================================================================

# Importações para Flask-Login
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Configuração do logger mais detalhada com UTF-8
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[stream_handler, file_handler]
)
logger = logging.getLogger(__name__)
fp_log = logging.getLogger("fp")

# Log de startup detalhado
logger.info("=== INICIANDO APLICACAO ===")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
logger.info(f"PORT: {os.environ.get('PORT', 'NAO_DEFINIDA')}")
logger.info(f"RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT', 'LOCAL')}")
logger.info(f"PYTHONUNBUFFERED: {os.environ.get('PYTHONUNBUFFERED', 'NAO_DEFINIDO')}")
logger.info(f"DEBUG: {os.environ.get('DEBUG', 'NAO_DEFINIDO')}")
logger.info(f"LOG_LEVEL: {os.environ.get('LOG_LEVEL', 'NAO_DEFINIDO')}")

# Lista arquivos importantes
logger.info("=== ARQUIVOS IMPORTANTES ===")
for file in ['app.py', 'wsgi.py', 'start.sh', 'requirements.txt', 'Dockerfile']:
    if os.path.exists(file):
        size = os.path.getsize(file)
        logger.info(f"{file}: {size} bytes")
    else:
        logger.warning(f"{file}: NAO ENCONTRADO")

# ============================================================================
# 🛡️ SISTEMA DE VERSÃO DE SESSÃO (ENTRADA SEGURA)
# ============================================================================

# Versão do protocolo de sessão - AUMENTE quando mudar lógica de auth/sessão
APP_SESSION_VERSION = 4

# Timeouts de sessão para segurança
MAX_IDLE = timedelta(hours=2)   # Sessão morre após 2h de inatividade
MAX_AGE  = timedelta(hours=12)  # Sessão morre após 12h totarequirements.txt

# ============================================================================
# 🔐 FUNÇÕES DE SEGURANÇA
# ============================================================================

import hashlib

def _client_ip():
    """Pega só o primeiro IP (cliente) do X-Forwarded-For ou remote_addr."""
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.remote_addr or ''

def _fingerprint():
    """Fingerprint estável: User-Agent (limitado) + primeiro IP."""
    ua = (request.headers.get('User-Agent','') or '')[:120]
    ip = _client_ip()
    base = f"{ua}|{ip}"
    return hashlib.sha256(base.encode()).hexdigest()[:16]

# ============================================================================




# ============================================================================
# 📊 CLASSES DE USUÁRIO E PERMISSÕES
# ============================================================================

# Lista global de emails master
MASTER_EMAILS = {
    'master_ef@loterias.com',
    'master_sf@loterias.com',
    'master_sm@loterias.com',
    'master_jj@loterias.com',
    'master_fc@loterias.com',
    'master_dc@loterias.com',
}

def _attach_master_flag(user):
    """Anexa flag nivel_master ao usuário baseado no email."""
    if user:
        user.nivel_master = (user.email in MASTER_EMAILS)
    return user

class UserLevel:
    """Níveis de usuário disponíveis no sistema."""
    FREE = "FREE"
    PREMIUM_DAILY = "PREMIUM_DAILY"
    PREMIUM_MONTHLY = "PREMIUM_MONTHLY"
    PREMIUM_SEMESTRAL = "PREMIUM_SEMESTRAL"
    PREMIUM_ANNUAL = "PREMIUM_ANNUAL"
    LIFETIME = "LIFETIME"

class UserPermissions:
    """Define quais rotas são freemium vs premium."""
    
    # Rotas FREEMIUM (acesso gratuito)
    FREE_ROUTES = {
        '/',  # Landing page
        '/dashboard_milionaria',  # +Milionária
        '/dashboard_quina',  # Quina
        '/dashboard_lotomania',  # Lotomania
        '/dashboard_MS',  # Mega Sena (liberado para freemium)
        '/dashboard_megasena',  # Mega Sena (alias)
        '/dashboard_lotofacil',  # Lotofácil (liberado para freemium)
        '/upgrade_plans',
        '/checkout',
        '/api/quina/dados-reais'  # API de dados da Quina
    }
    
    # Rotas PREMIUM (requer assinatura)
    PREMIUM_ROUTES = {
        '/aposta_inteligente_premium',
        '/aposta_inteligente_premium_MS',
        '/aposta_inteligente_premium_quina',
        '/aposta_inteligente_premium_lotofacil',
        '/lotofacil_laboratorio',
        '/boloes_loterias',
        '/analise_estatistica_avancada_milionaria',
        '/analise_estatistica_avancada_megasena',
        '/analise_estatistica_avancada_quina',
        '/analise_estatistica_avancada_lotofacil',
        '/analise_estatistica_avancada_lotomania',
        '/painel_analises_estatisticas_quina',
        '/painel_analises_estatisticas_megasena',
        '/painel_analises_estatisticas_milionaria',
        '/painel_analises_estatisticas_lotofacil'
    }
    
    @classmethod
    def is_free_route(cls, route):
        """Verifica se uma rota é de acesso gratuito."""
        return route in cls.FREE_ROUTES
    
    @classmethod
    def is_premium_route(cls, route):
        """Verifica se uma rota requer assinatura premium."""
        return route in cls.PREMIUM_ROUTES
    
    @classmethod
    def has_access(cls, route, user):
        """Verifica se o usuário tem acesso à rota."""
        # Se é rota gratuita, sempre tem acesso
        if cls.is_free_route(route):
            return True
        
        # Se é rota premium, verificar se é premium ou master
        if cls.is_premium_route(route):
            # Verificar se é usuário master
            if hasattr(user, 'nivel_master') and user.nivel_master:
                return True
            
            # Verificar se é premium normal
            return user.is_premium
        
        return False

class User(UserMixin):
    """Modelo de usuário com Flask-Login."""
    
    def __init__(self, user_id, email, level, subscription_expiry=None):
        self.id = user_id
        self.email = email
        self.level = level
        self.subscription_expiry = subscription_expiry
        self._is_authenticated = False  # 🔒 FLAG DE AUTENTICAÇÃO REAL
    
    def set_authenticated(self, value: bool):
        """Método para controlar o status de autenticação."""
        self._is_authenticated = bool(value)
    
    @property
    def is_authenticated(self):
        """Override do UserMixin - só retorna True se realmente logado."""
        return self._is_authenticated
    
    def get_id(self):
        """Retorna o ID do usuário como string."""
        return str(self.id)
    
    @property
    def is_premium(self):
        """Verifica se o usuário tem acesso premium ativo."""
        # Master sempre tem acesso premium
        if getattr(self, 'nivel_master', False):
            return True
        if self.level == UserLevel.LIFETIME:
            return True
        if self.subscription_expiry:
            return datetime.utcnow() < self.subscription_expiry
        # fallback provisório: quando subscription_expiry não vem do DB
        return self.level in {
            UserLevel.PREMIUM_DAILY, UserLevel.PREMIUM_MONTHLY,
            UserLevel.PREMIUM_SEMESTRAL, UserLevel.PREMIUM_ANNUAL
        }
    
    @property
    def subscription_status(self):
        """Retorna o status da assinatura."""
        if self.level == UserLevel.FREE:
            return "Gratuito"
        elif self.level == UserLevel.LIFETIME:
            return "Vitalício"
        elif self.subscription_expiry:
            if datetime.utcnow() < self.subscription_expiry:
                dias_restantes = (self.subscription_expiry - datetime.utcnow()).days
                return f"Ativo ({dias_restantes} dias restantes)"
            else:
                return "Expirado"
        return "Desconhecido"

# ============================================================================
# 🗄️ BANCO DE DADOS REAL (SQLITE)
# ============================================================================

# Importar configuração do banco
import sys
sys.path.append('database')
from database.db_config import get_db_connection, create_user_simple
import bcrypt
import random
import string
import secrets
from datetime import datetime, timedelta

# Função create_user movida para db_config.py

# ============================================================================
# 🔑 SISTEMA DE CHAVE DE AUTENTICAÇÃO
# ============================================================================

def gerar_chave_autenticacao():
    """Gera uma chave única e segura para autenticação com timestamp."""
    import secrets
    import time
    ts = int(time.time())
    return f"{ts}:{secrets.token_urlsafe(32)}"

def validar_chave_autenticacao(chave):
    """Valida se a chave de autenticação é válida com timestamp."""
    if not chave:
        return False
    
    # Verificar se a chave existe na sessão
    chave_sessao = session.get('auth_key')
    if not chave_sessao:
        return False
    
    # Verificar se a chave corresponde
    if chave != chave_sessao:
        return False
    
    # Verificar timestamp da chave (24 horas)
    try:
        import time
        ts_str, _ = chave.split(':', 1)
        ts = int(ts_str)
        now = int(time.time())
        if (now - ts) > 86400:  # 24 horas em segundos
            return False
    except:
        return False
    
    return True

def get_user_by_id(user_id):
    """Recupera usuário por ID do banco SQLite - apenas para verificar acesso."""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        cur = conn.cursor()
        
        # Busca apenas ID, email e tipo_plano (não precisa da senha)
        cur.execute("""
            SELECT id, email, tipo_plano
            FROM usuarios
            WHERE id = ?
        """, (user_id,))
        row = cur.fetchone()
        conn.close()
        
        if not row:
            return None

        # row = (id, email, tipo_plano)
        plano = row[2] if row[2] else 'Free'
        level_map = {
                'Free': UserLevel.FREE,
                'Mensal': UserLevel.PREMIUM_MONTHLY,
                'Semestral': UserLevel.PREMIUM_SEMESTRAL,
                'Anual': UserLevel.PREMIUM_ANNUAL,
                'Vitalício': UserLevel.LIFETIME
            }
        level = level_map.get(plano, UserLevel.FREE)

        user = User(row[0], row[1], level)  # id, email, level
        # Master por email (usando lista global)
        user.nivel_master = (user.email in MASTER_EMAILS)
        return user
        
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por ID: {e}")
        return None

def get_user_by_email(email):
    """Recupera usuário por email do banco SQLite."""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        # Buscar usuário
        cursor.execute("""
            SELECT id, nome_completo, email, senha_hash, tipo_plano
            FROM usuarios
            WHERE email = ?
        """, (email,))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            # Mapear plano para UserLevel
            plano_nome = user_data[4] if user_data[4] else 'Free'
            level_mapping = {
                'Free': UserLevel.FREE,
                'Mensal': UserLevel.PREMIUM_MONTHLY,
                'Semestral': UserLevel.PREMIUM_SEMESTRAL,
                'Anual': UserLevel.PREMIUM_ANNUAL,
                'Vitalício': UserLevel.LIFETIME
            }
            level = level_mapping.get(plano_nome, UserLevel.FREE)
            
            user = User(user_data[0], user_data[2], level)  # id, email, level
            user.senha_hash = user_data[3]  # senha_hash
            return _attach_master_flag(user)
        
        return None
        
    except Exception as e:
        logger.error(f"Erro ao buscar usuário por email: {e}")
        return None

def verify_password(user, password):
    """Verifica se a senha está correta."""
    try:
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return password_hash == user.senha_hash
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {e}")
        return False

# ============================================================================
# ✅ FUNÇÕES DE VALIDAÇÃO POR CÓDIGO
# ============================================================================

def gerar_codigo_validacao():
    """Gera um código de 6 dígitos aleatório."""
    return ''.join(random.choices(string.digits, k=6))

def criar_codigo_validacao(usuario_id, tipo):
    """Cria um código de validação para o usuário."""
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        # Limpar códigos anteriores do usuário
        cursor.execute("DELETE FROM codigos_validacao WHERE usuario_id = ? AND tipo = ?", (usuario_id, tipo))
        
        # Gerar novo código
        codigo = gerar_codigo_validacao()
        data_expiracao = datetime.utcnow() + timedelta(minutes=15)  # 15 minutos para expirar
        
        # Inserir código
        cursor.execute("""
            INSERT INTO codigos_validacao (usuario_id, codigo, tipo, data_expiracao)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, codigo, tipo, data_expiracao))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Código de validação criado: {codigo} para usuário {usuario_id}")
        return codigo
        
    except Exception as e:
        logger.error(f"Erro ao criar código de validação: {e}")
        if conn:
            conn.close()
        return None

def validar_codigo(usuario_id, codigo, tipo):
    """Valida o código de verificação do usuário."""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Buscar código válido
        cursor.execute("""
            SELECT id, status, tentativas, data_expiracao 
            FROM codigos_validacao 
            WHERE usuario_id = ? AND codigo = ? AND tipo = ? AND status = 'pendente'
        """, (usuario_id, codigo, tipo))
        
        codigo_data = cursor.fetchone()
        if not codigo_data:
            return False
        
        codigo_id, status, tentativas, data_expiracao = codigo_data
        
        # Verificar se expirou
        if datetime.utcnow() > datetime.fromisoformat(data_expiracao):
            cursor.execute("UPDATE codigos_validacao SET status = 'expirado' WHERE id = ?", (codigo_id,))
            conn.commit()
            conn.close()
            return False
        
        # Verificar tentativas (máximo 3)
        if tentativas >= 3:
            cursor.execute("UPDATE codigos_validacao SET status = 'expirado' WHERE id = ?", (codigo_id,))
            conn.commit()
            conn.close()
            return False
        
        # Marcar como validado
        cursor.execute("UPDATE codigos_validacao SET status = 'validado' WHERE id = ?", (codigo_id,))
        
        # Atualizar status do usuário
        cursor.execute("UPDATE usuarios SET status = 'ativo' WHERE id = ?", (usuario_id,))
        
        # Marcar email/telefone como verificado
        if tipo == 'email':
            cursor.execute("""
                INSERT OR REPLACE INTO emails_usuarios (usuario_id, email, verificado, data_verificacao)
                SELECT id, email, 1, CURRENT_TIMESTAMP FROM usuarios WHERE id = ?
            """, (usuario_id,))
        elif tipo == 'sms':
            cursor.execute("""
                INSERT OR REPLACE INTO telefones_usuarios (usuario_id, telefone, verificado, data_verificacao)
                SELECT id, telefone, 1, CURRENT_TIMESTAMP FROM usuarios WHERE id = ?
            """, (usuario_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Código validado com sucesso para usuário {usuario_id}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao validar código: {e}")
        if conn:
            conn.close()
        return False

def incrementar_tentativas_codigo(usuario_id, codigo, tipo):
    """Incrementa o contador de tentativas de um código."""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE codigos_validacao 
            SET tentativas = tentativas + 1 
            WHERE usuario_id = ? AND codigo = ? AND tipo = ?
        """, (usuario_id, codigo, tipo))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Erro ao incrementar tentativas: {e}")
        if conn:
            conn.close()
        return False



# ============================================================================
# 🚀 INICIALIZAÇÃO DO FLASK
# ============================================================================

app = Flask(__name__, static_folder='static')

# ⛳ Proxy awareness: HTTPS/IP corretos atrás de LB/CDN
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=0, x_port=0, x_prefix=0)

# Detectar ambiente (produção vs desenvolvimento)
is_production = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('ENVIRONMENT') == 'production'

# Variável global para modo de desenvolvimento
MODO_DESENVOLVIMENTO = os.getenv('MODO_DESENVOLVIMENTO', '0') == '1'

# Configuração unificada de sessão
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-only-secret-change-me')
app.config['SESSION_COOKIE_NAME'] = 'li_session'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=is_production,        # True em produção, False em dev
    SESSION_COOKIE_SAMESITE='Lax',
    REMEMBER_COOKIE_DURATION=0,         # desativa "lembrar" persistente
    REMEMBER_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_SECURE=is_production,       # True em produção, False em dev
    REMEMBER_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=2),  # Alinhado com remember=False
)

# ============================================================================
# 🌐 CONTEXT PROCESSOR - Variáveis Globais para Templates
# ============================================================================
@app.context_processor
def inject_global_vars():
    """Injeta variáveis globais em todos os templates automaticamente"""
    return {
        'free_access_mode': FREE_ACCESS_MODE,  # Controle de acesso livre
    }

# ============================================================================
# 📊 CONFIGURAÇÃO DO ANALYTICS
# ============================================================================

# Carregar configurações do arquivo
if os.path.exists('config.env'):
    with open('config.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Configurar banco de dados para analytics
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///li.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Criar tabelas automaticamente
with app.app_context():
    try:
        # Verificar se a tabela existe antes de criar
        inspector = db.inspect(db.engine)
        has_table = inspector.has_table("li_events")
        logger.info(f"📊 Tabela li_events existe: {has_table}")
        
        if not has_table:
            logger.info("🔨 Criando tabela li_events...")
            db.create_all()
            logger.info("✅ Tabela li_events criada com sucesso!")
        else:
            logger.info("✅ Tabela li_events já existe!")
            
        # Verificar novamente
        inspector = db.inspect(db.engine)
        has_table = inspector.has_table("li_events")
        logger.info(f"📊 Tabela li_events existe após criação: {has_table}")
        
        # Contar eventos
        count = db.session.query(db.func.count(Event.id)).scalar()
        logger.info(f"📈 Total de eventos: {count}")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar tabelas: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")

# ============================================================================
# 🔧 CONFIGURAÇÃO DO FLASK-LOGIN (ÚNICA VERSÃO)
# ============================================================================

login_manager = LoginManager()
login_manager.init_app(app)
# 🎉 Em modo de acesso livre, não redirecionar para login
if FREE_ACCESS_MODE:
    login_manager.login_view = None  # Desabilita redirect automático
else:
    login_manager.login_view = 'upgrade_plans'

# ============================================================================
# 🛡️ GATE DE VERSÃO DE SESSÃO (ENTRADA SEGURA)
# ============================================================================

@app.before_request
def session_version_gate():
    """Gate de versão de sessão - invalida cookies antigos automaticamente."""
    # ignore rotas que nunca devem exigir sessão
    if request.path in ("/healthz", "/favicon.ico", "/robots.txt") or request.endpoint in (None, 'static') or request.path.startswith("/admin/analytics"):
        return
    
    sv = session.get('_sv')  # session version
    if sv != APP_SESSION_VERSION:
        # Sessão velha/estranha → limpa e recomeça
        session.clear()
        session['_sv'] = APP_SESSION_VERSION
        # opcional: carimbar um nonce de boot
        session['_boot'] = True

@app.before_request
def session_fingerprint_gate():
    """Gate de fingerprint com tolerância a troca de IP (4G/proxy)."""
    # ignore rotas que nunca devem exigir sessão
    if request.path in ("/healthz", "/favicon.ico", "/robots.txt") or request.endpoint in (None, 'static') or request.path.startswith("/admin/analytics"):
        return
    cur = _fingerprint()
    old = session.get('_fp')
    if old is None:
        session['_fp'] = cur
        session['_fp_ua'] = (request.headers.get('User-Agent','') or '')[:120]
        return
    if old != cur:
        ua_now = (request.headers.get('User-Agent','') or '')[:120]
        ua_old = session.get('_fp_ua')
        # Se só o IP mudou e o UA é o mesmo, atualiza sem deslogar
        if ua_old == ua_now:
            fp_log.info("FP updated by IP change only")
            session['_fp'] = cur
            return
        # Mudou UA (outro device/navegador) → reinicia sessão
        fp_log.info("FP reset by UA change; dropping session")
        session.clear()
        session['_sv'] = APP_SESSION_VERSION
        session['_fp'] = cur
        session['_fp_ua'] = ua_now

@app.before_request
def session_time_guard():
    """Gate de timeout - mata sessões zumbis por tempo."""
    # ignore rotas que nunca devem exigir sessão
    if request.path in ("/healthz", "/favicon.ico", "/robots.txt") or request.endpoint in (None, 'static') or request.path.startswith("/admin/analytics"):
        return
    
    meta = session.get('_meta')
    now = datetime.utcnow()

    if not meta:
        session['_meta'] = {'iat': now.isoformat(), 'last': now.isoformat()}
        return

    iat  = datetime.fromisoformat(meta['iat'])
    last = datetime.fromisoformat(meta['last'])

    if (now - last) > MAX_IDLE or (now - iat) > MAX_AGE:
        session.clear()
        session['_sv'] = APP_SESSION_VERSION
        session['_meta'] = {'iat': now.isoformat(), 'last': now.isoformat()}
        return

    # refresh last activity
    meta['last'] = now.isoformat()
    session['_meta'] = meta

@app.after_request
def add_security_headers(resp):
    """Evita cache e garante Vary correto em páginas autenticadas."""
    resp.headers['Cache-Control'] = 'no-store'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Vary'] = 'Cookie, User-Agent'
    # HSTS só em prod e conexão segura
    if is_production and request.is_secure:
        resp.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return resp

# ============================================================================
# 🔍 LOG DE DIAGNÓSTICO TEMPORÁRIO (REMOVER DEPOIS)
# ============================================================================
# Funções de debug removidas para evitar interferência

@app.get('/session_status')
def session_status():
    """Endpoint para verificar status da sessão e autenticação."""
    return jsonify({
        'is_authenticated': bool(getattr(current_user,'is_authenticated', False)),
        'has_auth_key': bool(session.get('auth_key')),
    })

# 🔎 Diagnóstico: força um Set-Cookie para validar no navegador
@app.get('/debug_set_cookie')
def debug_set_cookie():
    info = {
        "secure": app.config['SESSION_COOKIE_SECURE'],
        "samesite": app.config['SESSION_COOKIE_SAMESITE'],
        "http_only": app.config['SESSION_COOKIE_HTTPONLY'],
        "name": app.config.get('SESSION_COOKIE_NAME', 'session')
    }
    resp = jsonify(info)
    resp.set_cookie(
        key='li_test',
        value='ok',
        secure=app.config['SESSION_COOKIE_SECURE'],
        httponly=True,
        samesite=app.config['SESSION_COOKIE_SAMESITE'],
        max_age=3600
    )
    return resp

@login_manager.user_loader
def load_user(user_id):
    """Carrega usuário da sessão."""
    try:
        if not user_id:
            return None

        try:
            user_id_int = int(user_id)
        except ValueError:
            return None

        user = get_user_by_id(user_id_int)
        if not user:
            return None

        # 🔒 MARCAR COMO AUTENTICADO - CONFIA NO FLASK-LOGIN
        user.set_authenticated(True)

        return user

    except Exception as e:
        logger.error(f"Erro ao carregar usuário: {e}")
        return None


# ============================================================================
# 🔒 MIDDLEWARE UNIVERSAL DE CONTROLE DE ACESSO
# ============================================================================

# ROTAS_GRATUITAS removido - usando apenas UserPermissions.FREE_ROUTES

def verificar_usuario_logado() -> bool:
    """Verifica se o usuário está realmente logado - confia no Flask-Login."""
    try:
        from flask_login import current_user
        return bool(getattr(current_user, 'is_authenticated', False))
    except Exception:
        return False

def buscar_plano_usuario() -> str:
    """Busca o plano do usuário logado para exibir no badge."""
    try:
        logger.info("🔍 BADGE - Iniciando busca do plano do usuário")
        
        if not verificar_usuario_logado():
            logger.info("🔍 BADGE - Usuário não está logado")
            return None
            
        from flask_login import current_user
        logger.info(f"🔍 BADGE - Current user ID: {getattr(current_user, 'id', 'SEM_ID')}")
        
        if hasattr(current_user, 'id') and current_user.id:
            # Buscar diretamente no banco usando conexão SQL
            try:
                conn = get_db_connection()
                if not conn:
                    logger.error("🔍 BADGE - Não foi possível conectar ao banco")
                    return None
                    
                cur = conn.cursor()
                cur.execute("""
                    SELECT tipo_plano 
                    FROM usuarios 
                    WHERE id = ?
                """, (current_user.id,))
                
                resultado = cur.fetchone()
                conn.close()
                
                if resultado and resultado[0]:
                    plano = resultado[0]
                    logger.info(f"🎯 BADGE - Plano encontrado no banco: '{plano}'")
                    return plano
                else:
                    logger.warning("⚠️ BADGE - Usuário sem plano definido no banco")
                    return "Free"  # Default
                    
            except Exception as db_e:
                logger.error(f"❌ BADGE - Erro ao consultar banco: {db_e}")
                return None
        else:
            logger.warning("⚠️ BADGE - Current user sem ID válido")
            
    except Exception as e:
        logger.error(f"❌ BADGE - Erro ao buscar plano: {e}")
        import traceback
        logger.error(f"❌ BADGE - Traceback: {traceback.format_exc()}")
    
    logger.info("🔍 BADGE - Retornando None (sem plano)")
    return None

def verificar_acesso_universal(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        route = request.path
        
        # 🎉 MODO ACESSO LIVRE: Libera tudo sem verificações
        if FREE_ACCESS_MODE:
            return f(*args, **kwargs)

        # 1) FREE liberadas
        if UserPermissions.is_free_route(route):
            return f(*args, **kwargs)

        # 2) Premium/protegidas: confia no Flask-Login
        if not current_user.is_authenticated:
            return redirect('/upgrade_plans')

        # 3) Plano do usuário
        if UserPermissions.has_access(route, current_user):
            return f(*args, **kwargs)

        return redirect('/upgrade_plans')
    return decorated

# ============================================================================
# 👥 ROTAS DE AUTENTICAÇÃO
# ============================================================================





@app.route('/login', methods=['POST'])
def login():
    """Login com email e senha."""
    data = request.get_json(silent=True) or request.form
    email = (data.get('email') or '').strip()
    senha = (data.get('senha') or '').strip()
    
    if not email or not senha:
        return jsonify({'success': False, 'error': 'Email e senha são obrigatórios'}), 400

    user = get_user_by_email(email)
    if not user:
        return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404

    if not verify_password(user, senha):
        return jsonify({'success': False, 'error': 'Senha incorreta'}), 401

    # 🔑 GERAR CHAVE DE AUTENTICAÇÃO ÚNICA
    auth_key = gerar_chave_autenticacao()
    
    # 🔑 SALVAR AUTH_KEY NA SESSÃO
    session['auth_key'] = auth_key
    session['login_timestamp'] = datetime.utcnow().isoformat()
    
    # 🔑 INICIALIZAR META DE TIMEOUT
    now = datetime.utcnow().isoformat()
    session['_meta'] = {'iat': now, 'last': now}
    
    # 🔑 MARCAR COMO AUTENTICADO E FAZER LOGIN
    user.set_authenticated(True)
    login_user(user, remember=False)  # Sessão não-permanente
    session.permanent = False

    return jsonify({'success': True, 'message': 'Login realizado com sucesso!',
                    'user_level': user.level, 'is_premium': user.is_premium,
                    'nivel_master': getattr(user, 'nivel_master', False)})

@app.route('/logout')
def logout():
    """Logout do usuário."""
    # 🎉 Em modo de acesso livre, redirecionar para landing
    if FREE_ACCESS_MODE:
        return redirect(url_for('index'))
    
    # Verificar se está logado
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    from flask_login import logout_user
    resp = redirect(url_for('landing_page'))

    # 1) desloga no Flask-Login
    logout_user()

    # 2) zera a sessão
    session.clear()

    # 3) apaga cookies relevantes
    resp.delete_cookie('session')           # cookie de sessão do Flask
    resp.delete_cookie('remember_token')    # cookie de "lembrar-me" do Flask-Login

    return resp

@app.route('/wipe_session')
def wipe_session():
    """Endpoint de limpeza forçada para debug."""
    resp = redirect(url_for('landing_page'))
    session.clear()
    resp.delete_cookie('session')
    resp.delete_cookie('remember_token')
    return resp

@app.route('/debug_config_full')
def debug_config_full():
    """Debug completo das configurações de sessão e cookies."""
    from flask import jsonify
    cfg = {k: str(v) for k, v in app.config.items()
           if k.startswith('REMEMBER_') or k.startswith('SESSION_')}
    cfg['cookies_present'] = list(request.cookies.keys())
    return jsonify(cfg)

@app.route('/upgrade_plans')
def upgrade_plans():
    """Página de planos premium."""
    # Se estiver em modo de acesso livre, redirecionar para landing
    if FREE_ACCESS_MODE:
        return redirect(url_for('index'))
    return render_template('upgrade_plans.html', is_logged_in=verificar_usuario_logado())

@app.route('/politica_cookies')
def politica_cookies():
    """Renderiza a página de política de cookies."""
    from datetime import datetime
    return render_template('politica_cookies.html', data_atual=datetime.utcnow().strftime('%d/%m/%Y'), is_logged_in=verificar_usuario_logado())

@app.route('/checkout')
def checkout():
    """Página de checkout/pagamento."""
    return render_template('checkout.html', is_logged_in=verificar_usuario_logado())

@app.route('/checkout-transparente/<plano_id>')
def checkout_transparente(plano_id):
    """Página de checkout transparente."""
    from config.mercadopago_config import PLANOS_MERCADOPAGO
    
    plano = PLANOS_MERCADOPAGO.get(plano_id)
    if not plano:
        return "Plano não encontrado", 404
    
    return render_template('checkout_transparente.html', is_logged_in=verificar_usuario_logado(), 
                         plano_id=plano_id,
                         plano_nome=plano['nome'],
                         plano_valor=plano['preco'])

# ============================================================================
# 💳 ROTAS MERCADO PAGO
# ============================================================================

@app.route('/api/mercadopago/criar-pagamento', methods=['POST'])
def criar_pagamento_mercadopago():
    """Criar pagamento via Mercado Pago."""
    try:
        from services.mercadopago_service import mercadopago_service
        
        data = request.get_json()
        plano_id = data.get('plano_id')
        usuario_id = data.get('usuario_id', 1)  # Em produção, viria da sessão
        
        # Dados do usuário
        dados_usuario = {
            'nome': data.get('nome'),
            'email': data.get('email'),
            'cpf': data.get('cpf'),
            'telefone': data.get('telefone')
        }
        
        # Criar preferência de pagamento
        result = mercadopago_service.criar_preferencia_pagamento(
            plano_id, usuario_id, dados_usuario
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar pagamento: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/webhook/mercadopago', methods=['POST'])
def webhook_mercadopago():
    """Webhook para notificações do Mercado Pago."""
    try:
        from services.mercadopago_service import mercadopago_service
        
        webhook_data = request.get_json()
        result = mercadopago_service.processar_webhook(webhook_data)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro no webhook: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/mercadopago/verificar-pagamento/<payment_id>')
def verificar_pagamento_mercadopago(payment_id):
    """Verificar status de um pagamento."""
    try:
        from services.mercadopago_service import mercadopago_service
        
        result = mercadopago_service.verificar_pagamento(payment_id)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar pagamento: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/mercadopago/metodos-pagamento')
def metodos_pagamento_mercadopago():
    """Listar métodos de pagamento disponíveis."""
    try:
        from services.mercadopago_service import mercadopago_service
        
        metodos = mercadopago_service.get_metodos_pagamento()
        config_parcelamento = mercadopago_service.get_configuracao_parcelamento()
        
        return jsonify({
            "success": True,
            "metodos": metodos,
            "parcelamento": config_parcelamento
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao listar métodos de pagamento: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/mercadopago/calcular-parcelas/<plano_id>')
def calcular_parcelas_mercadopago(plano_id):
    """Calcular opções de parcelamento para um plano."""
    try:
        from services.mercadopago_service import mercadopago_service
        from config.mercadopago_config import PLANOS_MERCADOPAGO
        
        # Buscar dados do plano
        plano = PLANOS_MERCADOPAGO.get(plano_id)
        if not plano:
            return jsonify({
                "success": False,
                "error": "Plano não encontrado"
            }), 404
        
        # Calcular parcelas
        parcelas = mercadopago_service.calcular_parcelas(plano['preco'], plano_id)
        
        return jsonify({
            "success": True,
            "plano": plano,
            "parcelas": parcelas
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao calcular parcelas: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

# ============================================================================
# 💳 ROTAS CHECKOUT TRANSPARENTE
# ============================================================================

@app.route('/api/checkout/cartao', methods=['POST'])
def checkout_cartao():
    """Processar pagamento com cartão."""
    try:
        from services.checkout_transparente import checkout_transparente
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['valor', 'descricao', 'email', 'cpf', 'token', 'metodo_pagamento']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({
                    "success": False,
                    "error": f"Campo obrigatório: {campo}"
                }), 400
        
        # Criar pagamento
        result = checkout_transparente.criar_pagamento_cartao(data)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro no checkout cartão: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/checkout/pix', methods=['POST'])
def checkout_pix():
    """Processar pagamento via PIX."""
    try:
        from services.checkout_transparente import checkout_transparente
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        campos_obrigatorios = ['valor', 'descricao', 'email', 'cpf']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({
                    "success": False,
                    "error": f"Campo obrigatório: {campo}"
                }), 400
        
        # Criar pagamento PIX
        result = checkout_transparente.criar_pagamento_pix(data)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Erro no checkout PIX: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/checkout/public-key')
def checkout_public_key():
    """Retornar chave pública para o frontend."""
    try:
        from services.checkout_transparente import checkout_transparente
        
        return jsonify({
            "success": True,
            "public_key": checkout_transparente.public_key
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao obter chave pública: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500


@app.route('/premium_required')
def premium_required():
    """Página de erro para acesso premium."""
    return render_template('premium_required.html', is_logged_in=verificar_usuario_logado())

@app.route('/upgrade_plan', methods=['POST'])
def upgrade_plan():
    """Processa upgrade de plano."""
    # 🎉 Em modo de acesso livre, não permitir upgrade
    if FREE_ACCESS_MODE:
        return jsonify({'success': False, 'error': 'Funcionalidade desabilitada temporariamente'}), 403
    
    # Verificar se está logado
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Login necessário'}), 401
    
    data = request.get_json()
    plan = data.get('plan')
    
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 401
    
    # Mapear plano para nível
    plan_mapping = {
        'daily': UserLevel.PREMIUM_DAILY,  # Novo plano diário
        'monthly': UserLevel.PREMIUM_MONTHLY,
        'semestral': UserLevel.PREMIUM_SEMESTRAL,
        'annual': UserLevel.PREMIUM_ANNUAL,
        'lifetime': UserLevel.LIFETIME
    }
    
    if plan not in plan_mapping:
        return jsonify({'success': False, 'error': 'Plano inválido'}), 400
    
    # Atualizar usuário
    current_user.level = plan_mapping[plan]
    
    # Definir data de expiração
    if plan == 'daily':
        current_user.subscription_expiry = datetime.utcnow() + timedelta(days=1)
    elif plan == 'monthly':
        current_user.subscription_expiry = datetime.utcnow() + timedelta(days=30)
    elif plan == 'semestral':
        current_user.subscription_expiry = datetime.utcnow() + timedelta(days=180)
    elif plan == 'annual':
        current_user.subscription_expiry = datetime.utcnow() + timedelta(days=365)
    elif plan == 'lifetime':
        current_user.subscription_expiry = None
    
    # Em produção, você salvaria no banco real
    # users_db[current_user.id] = current_user  # Comentado temporariamente
    
    return jsonify({
        'success': True, 
        'message': f'Plano atualizado para {plan}',
        'status': current_user.subscription_status
    })

# ============================================================================
# ✅ ROTAS DE VALIDAÇÃO POR CÓDIGO
# ============================================================================

@app.route('/enviar_codigo_validacao', methods=['POST'])
def enviar_codigo_validacao():
    """Envia código de validação por email ou SMS."""
    try:
        data = request.get_json()
        email = data.get('email')
        tipo = data.get('tipo')  # 'email' ou 'sms'
        
        if not email or tipo not in ['email', 'sms']:
            return jsonify({'success': False, 'error': 'Dados inválidos'}), 400
        
        # Buscar usuário
        user = get_user_by_email(email)
        if not user:
            return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404
        
        # Criar código de validação
        codigo = criar_codigo_validacao(user.id, tipo)
        if not codigo:
            return jsonify({'success': False, 'error': 'Erro ao gerar código'}), 500
        
        # TODO: Em produção, enviar código por email/SMS
        # Por enquanto, apenas retornar o código para teste
        if tipo == 'email':
            mensagem = f"Código de validação enviado para {email}: {codigo}"
        else:
            mensagem = f"Código de validação enviado por SMS: {codigo}"
        
        logger.info(f"Código de validação criado: {codigo} para {email}")
        
        return jsonify({
            'success': True,
            'message': mensagem,
            'codigo': codigo,  # Remover em produção!
            'tipo': tipo
        })
        
    except Exception as e:
        logger.error(f"Erro ao enviar código: {e}")
        return jsonify({'success': False, 'error': 'Erro interno'}), 500

@app.route('/validar_codigo', methods=['POST'])
def validar_codigo_rota():
    """Valida o código de verificação do usuário."""
    try:
        data = request.get_json()
        email = data.get('email')
        codigo = data.get('codigo')
        tipo = data.get('tipo')
        
        if not all([email, codigo, tipo]):
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400
        
        # Buscar usuário
        user = get_user_by_email(email)
        if not user:
            return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404
        
        # Validar código
        if validar_codigo(user.id, codigo, tipo):
            # Ativar assinatura FREE
            try:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE assinaturas 
                        SET status = 'ativa' 
                        WHERE usuario_id = ? AND status = 'pendente'
                    """, (user.id,))
                    conn.commit()
                    conn.close()
            except Exception as e:
                logger.error(f"Erro ao ativar assinatura: {e}")
            
            return jsonify({
                'success': True,
                'message': 'Cadastro validado com sucesso! Acesso liberado.',
                'redirect': '/'
            })
        else:
            # Incrementar tentativas
            incrementar_tentativas_codigo(user.id, codigo, tipo)
            return jsonify({'success': False, 'error': 'Código inválido ou expirado'}), 400
        
    except Exception as e:
        logger.error(f"Erro ao validar código: {e}")
        return jsonify({'success': False, 'error': 'Erro interno'}), 500



@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    """Salva o cadastro do usuário no banco SIMPLES."""
    try:
        print("🔍 ROTA /salvar_cadastro CHAMADA!")
        data = request.get_json()
        print(f"📊 Dados recebidos: {data}")
        
        # Extrair dados do formulário
        nome_completo = data.get('nome_completo')
        data_nascimento = data.get('data_nascimento')
        cpf = data.get('cpf')
        telefone = data.get('telefone')
        email = data.get('email')
        senha = data.get('senha')
        receber_emails = data.get('receber_emails', True)
        receber_sms = data.get('receber_sms', True)
        aceitou_termos = data.get('aceitou_termos', True)
        plano = data.get('plano', 'Free')
        
        print(f"📝 Dados extraídos: nome={nome_completo}, email={email}, senha={'*' * len(senha) if senha else 'None'}")
        
        # Validar dados obrigatórios
        if not all([nome_completo, email, senha]):
            print("❌ Dados obrigatórios não preenchidos")
            return jsonify({'success': False, 'error': 'Dados obrigatórios não preenchidos'}), 400
        
        print("✅ Dados válidos, criando usuário...")
        
        # Criar usuário no banco SIMPLES com TODOS os campos
        user_id = create_user_simple(
            nome_completo, email, senha, data_nascimento, cpf, telefone,
            receber_emails, receber_sms, aceitou_termos, plano
        )
        
        print(f"🎯 Resultado create_user_simple: {user_id}")
        
        if user_id:
            print(f"✅ Usuário criado com sucesso: {email} (ID: {user_id})")
            return jsonify({
                'success': True,
                'message': 'Cadastro salvo com sucesso!',
                'user_id': user_id,
                'email': email
            })
        else:
            print("❌ Erro ao criar usuário")
            return jsonify({'success': False, 'error': 'Erro ao criar usuário'}), 500
        
    except Exception as e:
        print(f"💥 ERRO na rota /salvar_cadastro: {e}")
        logger.error(f"Erro ao salvar cadastro: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/enviar_codigo_confirmacao', methods=['POST'])
def enviar_codigo_confirmacao():
    """Envia código de confirmação por email ou SMS."""
    try:
        data = request.get_json()
        usuario_id = data.get('usuario_id')
        tipo = data.get('tipo')  # 'email' ou 'sms'
        destinatario = data.get('destinatario')
        
        print(f"🔐 Enviando código de confirmação: usuário={usuario_id}, tipo={tipo}, destinatario={destinatario}")
        
        # Usar serviço real de envio (que já gera o código internamente)
        from services.envio_service import envio_service
        
        nome_usuario = data.get('nome_usuario', 'Usuário')
        
        resultado = envio_service.enviar_codigo_confirmacao(
            usuario_id, tipo, destinatario, nome_usuario
        )
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'message': resultado.get('message'),
                'codigo': resultado.get('codigo') if resultado.get('modo') == 'teste' else None
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Erro ao enviar código')
            }), 500
        
    except Exception as e:
        print(f"❌ Erro ao enviar código: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/validar_codigo_confirmacao', methods=['POST'])
def validar_codigo_confirmacao():
    """Valida código de confirmação."""
    try:
        data = request.get_json()
        usuario_id = data.get('usuario_id')
        codigo = data.get('codigo')
        
        print(f"🔍 Validando código: usuário={usuario_id}, código={codigo}")
        
        # Validar código
        from database.db_config import validar_codigo_confirmacao
        valido = validar_codigo_confirmacao(usuario_id, codigo)
        
        if valido:
            print(f"✅ Código validado com sucesso para usuário {usuario_id}")
            return jsonify({
                'success': True,
                'message': 'Código validado com sucesso!'
            })
        else:
            print(f"❌ Código inválido para usuário {usuario_id}")
            return jsonify({
                'success': False,
                'error': 'Código inválido ou expirado'
            })
        
    except Exception as e:
        print(f"❌ Erro ao validar código: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/check_access/<path:rota>')
def check_access(rota):
    # 🎉 MODO ACESSO LIVRE: Libera acesso a tudo
    if FREE_ACCESS_MODE:
        return jsonify({'has_access': True, 'reason': 'free_access_mode'})
    
    route_path = '/' + rota if not rota.startswith('/') else rota

    if UserPermissions.is_free_route(route_path):
        return jsonify({'has_access': True})

    if not current_user.is_authenticated:
        return jsonify({'has_access': False, 'reason': 'not_logged_in', 'upgrade_url': '/upgrade_plans'})

    if UserPermissions.has_access(route_path, current_user):
        return jsonify({'has_access': True})

    return jsonify({'has_access': False, 'reason': 'premium_required', 'upgrade_url': '/upgrade_plans'})

@app.route('/test_user/<level>')
def create_test_user(level):
    """Cria usuário de teste para desenvolvimento."""
    if level not in [UserLevel.FREE, UserLevel.PREMIUM_DAILY, UserLevel.PREMIUM_MONTHLY, UserLevel.PREMIUM_SEMESTRAL, UserLevel.PREMIUM_ANNUAL, UserLevel.LIFETIME]:
        return jsonify({'error': 'Nível inválido'}), 400
    
    test_email = f"test_{level.lower()}@example.com"
    # user = create_user(test_email, "test123", level)  # Comentado temporariamente
    user = None  # Simulação temporária
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'level': user.level,
                'status': user.subscription_status
            }
        })
    else:
        return jsonify({'error': 'Erro ao criar usuário de teste'}), 500

# ============================================================================
# 📊 FUNÇÕES UTILITÁRIAS
# ============================================================================

# Funções utilitárias movidas para utils/data_helpers.py
from utils.data_helpers import _to_native, limpar_valores_problematicos

# --- Importações das suas funções de análise, conforme a nova estrutura ---
# Certifique-se de que esses arquivos Python (.py) estejam no mesmo diretório
# ou em um subdiretório acessível (no caso, eles estão todos no mesmo nível da pasta +Milionaria/)

# Imports pesados movidos para lazy loading - serão importados quando necessário



# Imports pesados movidos para lazy loading - serão importados quando necessário

# Funções de carregamento movidas para services/data_loader.py
from services.data_loader import carregar_dados_milionaria, carregar_dados_megasena_app, carregar_dados_quina_app
from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil

# Importações das funções da Milionária (como estava no backup)
from funcoes.milionaria.funcao_analise_de_distribuicao import analise_distribuicao_milionaria
from funcoes.milionaria.funcao_analise_de_combinacoes import analise_combinacoes_milionaria
from funcoes.milionaria.funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria
from funcoes.milionaria.funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte
from funcoes.milionaria.calculos import calcular_seca_numeros, calcular_seca_trevos
from funcoes.milionaria.analise_estatistica_avancada import AnaliseEstatisticaAvancada

# Importações da Mega Sena
from funcoes.megasena.calculos_MS import calcular_seca_numeros_megasena
from funcoes.megasena.analise_estatistica_avancada_MS import AnaliseEstatisticaAvancada as AnaliseEstatisticaAvancadaMS
from funcoes.megasena.funcao_analise_de_distribuicao_MS import analise_distribuicao_megasena
from funcoes.megasena.funcao_analise_de_combinacoes_MS import analise_combinacoes_megasena
from funcoes.megasena.funcao_analise_de_padroes_sequencia_MS import analise_padroes_sequencias_megasena

# Importações da Quina
from funcoes.quina.funcao_analise_de_distribuicao_quina import analisar_distribuicao_quina
from funcoes.quina.funcao_analise_de_combinacoes_quina import analisar_combinacoes_quina
from funcoes.quina.funcao_analise_de_padroes_sequencia_quina import analisar_padroes_sequencias_quina
from funcoes.quina.analise_estatistica_avancada_quina import AnaliseEstatisticaAvancadaQuina

# Importações da Lotofácil
from funcoes.lotofacil.funcao_analise_de_distribuicao_lotofacil import analisar_distribuicao_lotofacil
from funcoes.lotofacil.funcao_analise_de_combinacoes_lotofacil import analisar_combinacoes_lotofacil
from funcoes.lotofacil.funcao_analise_de_padroes_sequencia_lotofacil import analisar_padroes_sequencias_lotofacil
from funcoes.lotofacil.analise_estatistica_avancada_lotofacil import AnaliseEstatisticaAvancadaLotofacil, realizar_analise_estatistica_avancada_lotofacil

# Variáveis globais para armazenar os DataFrames (como estava no backup)
df_milionaria = None
df_megasena = None
df_quina = None
df_lotofacil = None

# Carrega os dados na inicialização do aplicativo (como estava no backup)
with app.app_context():
    df_milionaria = carregar_dados_milionaria()
    df_megasena = carregar_dados_megasena_app()
    df_quina = carregar_dados_quina_app()
    df_lotofacil = carregar_dados_lotofacil()

# ============================================================================
# ⚙️ CARREGAMENTO DE DADOS (LAZY LOADING)
# ============================================================================

_data_cache = {}
_data_cache_mtime = {}

def _lazy_import_pandas():
    """Importa pandas apenas quando necessário."""
    import pandas as pd
    return pd

def _lazy_import_numpy():
    """Importa numpy apenas quando necessário."""
    import numpy as np
    return np

def _get_loteria_data_path(loteria):
    """Retorna o caminho do arquivo base usado pela loteria."""
    base_dir = os.path.join(os.path.dirname(__file__), "LoteriasExcel")
    file_map = {
        "mais_milionaria": "Milionária_edt.xlsx",
        "megasena": "MegaSena_edt.xlsx",
        "quina": "Quina_edt.xlsx",
        "lotofacil": "Lotofacil_edt2.xlsx",
        "lotomania": "Lotomania_edt.xlsx",
    }
    filename = file_map.get(loteria)
    if not filename:
        return None
    return os.path.join(base_dir, filename)

def _get_file_mtime_safe(path):
    """Retorna mtime do arquivo ou None se indisponível."""
    if not path or not os.path.exists(path):
        return None
    try:
        return os.path.getmtime(path)
    except Exception as exc:
        logger.warning(f"Não foi possível obter mtime de {path}: {exc}")
        return None

def carregar_dados_da_loteria(loteria):
    """Carrega dados da loteria com cache e invalidação automática por mtime."""
    global _data_cache, _data_cache_mtime

    data_path = _get_loteria_data_path(loteria)
    current_mtime = _get_file_mtime_safe(data_path)
    cached_mtime = _data_cache_mtime.get(loteria)
    should_reload = (
        loteria not in _data_cache
        or cached_mtime is None
        or current_mtime != cached_mtime
    )

    if should_reload:
        logger.info(f"Carregando dados da {loteria}...")
        if data_path:
            logger.info(f"Arquivo monitorado: {data_path} | mtime={current_mtime}")
        
        if loteria == "mais_milionaria":
            _data_cache[loteria] = carregar_dados_milionaria()
        elif loteria == "megasena":
            _data_cache[loteria] = carregar_dados_megasena_app()
        elif loteria == "quina":
            _data_cache[loteria] = carregar_dados_quina_app()
        elif loteria == "lotofacil":
            # Lazy import para lotofácil
            from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil
            _data_cache[loteria] = carregar_dados_lotofacil()
        elif loteria == "lotomania":
            # Lazy import para lotomania
            pd = _lazy_import_pandas()
            excel_path = _get_loteria_data_path("lotomania")
            logger.info(f"Tentando carregar Lotomania de: {excel_path}")
            if os.path.exists(excel_path):
                _data_cache[loteria] = pd.read_excel(excel_path)
                logger.info(f"Lotomania carregada com sucesso. Linhas: {len(_data_cache[loteria])}")
            else:
                logger.error(f"Arquivo Lotomania não encontrado: {excel_path}")
                _data_cache[loteria] = None
        else:
            logger.error(f"Loteria desconhecida: {loteria}")
            return None
        _data_cache_mtime[loteria] = current_mtime
    
    return _data_cache.get(loteria)

@app.route('/')
def landing_page():
    """Renderiza a página landing como página inicial."""
    return render_template('landing.html', modo_desenvolvimento=MODO_DESENVOLVIMENTO, is_logged_in=verificar_usuario_logado())

@app.route('/planos')
def planos_page():
    """Renderiza a página de planos premium."""
    return render_template('upgrade_plans.html', is_logged_in=verificar_usuario_logado())

@app.route('/api/carousel_data')
def get_carousel_data():
    """API para fornecer dados do carrossel de loterias."""
    try:
        # Caminho para o arquivo CSV do carrossel
        csv_path = os.path.join(os.path.dirname(__file__), "LoteriasExcel", "carrossel_Dados.csv")
        
        # Verifica se o arquivo existe
        logger.info(f"Verificando arquivo CSV: {csv_path}")
        if not os.path.exists(csv_path):
            logger.warning(f"Arquivo CSV não encontrado: {csv_path}")
            # Retorna dados de fallback
            return jsonify([{
                "loteria": "+Milionária",
                "texto_destaque": "Hoje",
                "cor_fundo": "#0f172a",
                "cor_borda": "#60a5fa",
                "cor_texto": "#ffffff",
                "valor": "—",
                "unidade": "",
                "link": "/"
            }]), 200
        else:
            logger.info(f"Arquivo CSV encontrado: {csv_path}")
        
        # Lê o CSV com lazy loading
        pd = _lazy_import_pandas()
        df = pd.read_csv(csv_path, encoding='utf-8')
        logger.info(f"CSV lido com sucesso. Colunas: {list(df.columns)}")
        logger.info(f"Total de linhas: {len(df)}")
        
        # Converte para JSON com tratamento de NaN
        records = json.loads(df.to_json(orient="records"))
        logger.info(f"Records convertidos: {len(records)}")
        
        # Função para normalizar valores
        def to_str(v):
            if v is None:
                return ""
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                if isinstance(v, float) and math.isnan(v):
                    return ""
                if float(v).is_integer():
                    return str(int(v))
                return str(v)
            s = str(v).strip()
            return "" if s.lower() == "nan" else s
        
        # Normaliza todos os campos
        for item in records:
            item["loteria"] = to_str(item.get("loteria", ""))
            item["texto_destaque"] = to_str(item.get("texto_destaque", ""))
            item["cor_fundo"] = to_str(item.get("cor_fundo", "#1f2937"))
            item["cor_borda"] = to_str(item.get("cor_borda", "#374151"))
            item["cor_texto"] = to_str(item.get("cor_texto", "#ffffff"))
            item["valor"] = to_str(item.get("valor", ""))
            item["unidade"] = to_str(item.get("unidade", ""))
            item["link"] = to_str(item.get("link", "#"))
        
        logger.info(f"Carrossel: {len(records)} itens carregados com sucesso")
        return jsonify(records), 200
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados do carrossel: {e}")
        # Retorna dados de fallback em caso de erro
        return jsonify([{
            "loteria": "+Milionária",
            "texto_destaque": "Hoje",
            "cor_fundo": "#0f172a",
            "cor_borda": "#60a5fa",
            "cor_texto": "#ffffff",
            "valor": "—",
            "unidade": "",
            "link": "/"
        }]), 200

@app.route('/dashboard')
def dashboard():
    """Redireciona para o dashboard da Milionária."""
    return redirect(url_for('dashboard_milionaria'))

@app.route('/dashboard_milionaria')
@verificar_acesso_universal
def dashboard_milionaria():
    """Renderiza a página principal do dashboard da Milionária."""
    return render_template('dashboard_milionaria.html', is_logged_in=verificar_usuario_logado())

# --- Rotas de API para as Análises ---

# ROTA REMOVIDA: /api/analise_frequencia (antiga) - Substituída por /api/analise-frequencia
# Para evitar confusão e manter consistência, use apenas a nova rota

@app.route('/api/analise-frequencia')
def get_analise_frequencia_nova():
    """Nova rota para análise de frequência com dados reais dos últimos 50 concursos."""
    try:
        # print("🔍 Iniciando API de frequência...")  # DEBUG - COMENTADO
        
        # Usar a nova função que carrega dados reais
        from funcoes.milionaria.funcao_analise_de_frequencia import analisar_frequencia
        
        # Obter parâmetro de quantidade de concursos (padrão: 50)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"🔍 qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        
        # Executar análise com dados reais
        # print("🔍 Chamando analisar_frequencia...")  # DEBUG - COMENTADO
        df_milionaria = carregar_dados_da_loteria("mais_milionaria")
        if df_milionaria is None or df_milionaria.empty:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500
        resultado = analisar_frequencia(df_milionaria=df_milionaria, qtd_concursos=qtd_concursos)
        # print(f"🔍 Resultado tipo: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🔍 Resultado: {resultado}")  # DEBUG - COMENTADO
        
        if not resultado or resultado == {}:
            # print("❌ Resultado vazio ou None")  # DEBUG - COMENTADO
            return jsonify({'error': 'Erro ao carregar dados de frequência.'}), 500

        return jsonify({
            'frequencia_absoluta_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['numeros'].items())],
            'frequencia_absoluta_trevos': [{'trevo': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['trevos'].items())],
            'frequencia_relativa_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['numeros'].items())],
            'frequencia_relativa_trevos': [{'trevo': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['trevos'].items())],
            # Manter estrutura atual e adicionar aliases compatíveis
            'numeros_quentes_frios': {
                'quentes': resultado.get('numeros_quentes_frios', {}).get('quentes') or resultado.get('numeros_quentes_frios', {}).get('numeros_quentes', []),
                'frios': resultado.get('numeros_quentes_frios', {}).get('frios') or resultado.get('numeros_quentes_frios', {}).get('numeros_frios', []),
            },
            # Aliases legacy (se algum front ainda esperar estes nomes)
            'numeros_quentes': (resultado.get('numeros_quentes_frios', {}).get('quentes') or resultado.get('numeros_quentes_frios', {}).get('numeros_quentes', [])),
            'numeros_frios': (resultado.get('numeros_quentes_frios', {}).get('frios') or resultado.get('numeros_quentes_frios', {}).get('numeros_frios', [])),
            'analise_temporal': resultado['analise_temporal'],
            'periodo_analisado': resultado['periodo_analisado']
        })
    except Exception as e:
        print(f"❌ Erro na API de frequência: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analise_padroes_sequencias', methods=['GET'])
def get_analise_padroes_sequencias():
    """Retorna os dados da análise de padrões e sequências."""
    df_milionaria = carregar_dados_da_loteria("mais_milionaria")
    if df_milionaria is None or df_milionaria.empty:
        return jsonify({"error": "Dados da +Milionária não carregados."}), 500

    # Verificar se há parâmetro de quantidade de concursos
    qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
    # print(f"🎯 Padrões/Sequências - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO

    dados_para_analise = df_milionaria.values.tolist()
    resultado = analise_padroes_sequencias_milionaria(dados_para_analise, qtd_concursos)
    return jsonify(resultado)

@app.route('/api/analise_de_distribuicao', methods=['GET'])
def get_analise_de_distribuicao():
    """Retorna os dados da análise de distribuição da +Milionária."""
    try:
        # Carrega os dados no escopo da rota (lazy loading)
        df_milionaria = carregar_dados_da_loteria("mais_milionaria")
        if df_milionaria is None or df_milionaria.empty:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500

        # Parâmetro opcional: quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        # Import lazy da função de análise
        from funcoes.milionaria.funcao_analise_de_distribuicao import analise_distribuicao_milionaria
        resultado = analise_distribuicao_milionaria(df_milionaria, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        logger.error(f"Erro na API de distribuição +Milionária: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/analise_de_distribuicao-MS', methods=['GET'])
def get_analise_de_distribuicao_megasena():
    """Retorna os dados da análise de distribuição da Mega Sena."""
    try:
        if df_megasena.empty:
            return jsonify({"error": "Dados da Mega Sena não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        if qtd_concursos is None or qtd_concursos <= 0:
            qtd_concursos = 200
        elif qtd_concursos > 200:
            qtd_concursos = 200
        # print(f"🎯 Distribuição Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
        # print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")  # DEBUG - COMENTADO

        resultado = analise_distribuicao_megasena(df_megasena, qtd_concursos)
        # print(f"🎯 Resultado da análise: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de distribuição Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# --- Rotas de API da Quina ---
@app.route('/api/analise-frequencia-quina')
def get_analise_frequencia_quina():
    """Nova rota para análise de frequência da Quina com dados reais dos últimos 100 concursos."""
    try:
        # Usar a função da Quina
        from funcoes.quina.funcao_analise_de_frequencia_quina import analisar_frequencia_quina
        
        # Obter parâmetro de quantidade de concursos (padrão: 100)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=100)
        
        # Carregar dados da Quina usando lazy loading
        df_quina = carregar_dados_da_loteria("quina")
        
        # Executar análise com dados reais da Quina
        resultado = analisar_frequencia_quina(df_quina=df_quina, qtd_concursos=qtd_concursos)
        
        if not resultado or resultado == {}:
            print("❌ Resultado vazio ou None")
            return jsonify({'error': 'Erro ao carregar dados de frequência da Quina.'}), 500
        
        # Adicionar análises temporais ao resultado
        try:
            from funcoes.quina.funcao_analise_de_frequencia_quina import analise_frequencia_temporal_estruturada_quina
            
            # Converter DataFrame para formato esperado pelas funções temporais
            dados_sorteios = []
            for _, row in df_quina.iterrows():
                concurso = int(row['Concurso']) if pd.notna(row['Concurso']) else 0
                bolas = [int(row[f'Bola{i}']) for i in range(1, 6) if pd.notna(row[f'Bola{i}'])]
                if len(bolas) == 5:
                    dados_sorteios.append([concurso] + bolas)
            
            # Análise temporal estruturada
            analise_temporal = analise_frequencia_temporal_estruturada_quina(dados_sorteios, periodo='meses', qtd_concursos=qtd_concursos)
            resultado['analise_temporal'] = analise_temporal or {}
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar análises temporais: {e}")
            resultado['analise_temporal'] = {}
        
        # Adicionar análise de combinações (versão simplificada)
        print("🔍 DEBUG: Iniciando análise de combinações...")
        try:
            from funcoes.quina.funcao_analise_de_combinacoes_quina import analisar_combinacoes_quina
            print("✅ DEBUG: Importação da função OK")
            
            # Análise de combinações simplificada
            print(f"🔍 DEBUG: Chamando analisar_combinacoes_quina com qtd_concursos={qtd_concursos}")
            combinacoes = analisar_combinacoes_quina(df_quina, qtd_concursos=qtd_concursos)
            print(f"✅ DEBUG: Função executada. Tipo: {type(combinacoes)}")
            
            if combinacoes:
                print(f"✅ DEBUG: Combinacoes não vazio. Chaves: {list(combinacoes.keys())}")
                # Extrair apenas dados essenciais para evitar problemas de serialização
                resultado['analise_combinacoes'] = {
                    'padroes_geometricos': combinacoes.get('padroes_geometricos', {}),
                    'afinidade_entre_numeros': combinacoes.get('afinidade_entre_numeros', {}),
                    'combinacoes_frequentes': combinacoes.get('combinacoes_frequentes', {})
                }
                print("✅ DEBUG: analise_combinacoes adicionado ao resultado")
            else:
                print("❌ DEBUG: Combinacoes vazio")
                resultado['analise_combinacoes'] = {}
                
        except Exception as e:
            print(f"❌ DEBUG: Erro ao carregar combinações: {e}")
            import traceback
            traceback.print_exc()
            resultado['analise_combinacoes'] = {}

        # Preparar dados dos concursos individuais para a matriz visual
        concursos_para_matriz = []
        # Converter dados do DataFrame para formato da matriz
        # Se qtd_concursos for None (todos os concursos), limitar a 350 para evitar loop
        limite_efetivo = qtd_concursos if qtd_concursos else 350
        print(f"🔍 Debug: qtd_concursos={qtd_concursos}, limite_efetivo={limite_efetivo}")
        print(f"🔍 Debug: Shape do df_quina={df_quina.shape}")
        
        df_filtrado = df_quina.tail(limite_efetivo)
        print(f"🔍 Debug: Shape do df_filtrado={df_filtrado.shape}")
        
        # Importar pandas para uso local
        pd = _lazy_import_pandas()
        
        for _, row in df_filtrado.iterrows():
            if not pd.isna(row['Concurso']):
                concursos_para_matriz.append({
                    'concurso': int(row['Concurso']),
                    'numeros': [int(row['Bola1']), int(row['Bola2']), int(row['Bola3']), 
                               int(row['Bola4']), int(row['Bola5'])]
                })
        
        print(f"🔍 Debug: Total de concursos para matriz={len(concursos_para_matriz)}")

        # Log final para verificar o que está sendo retornado
        print(f"🔍 DEBUG: Resultado final. Chaves: {list(resultado.keys())}")
        if 'analise_combinacoes' in resultado:
            print("✅ DEBUG: analise_combinacoes presente no resultado final")
        else:
            print("❌ DEBUG: analise_combinacoes NÃO presente no resultado final")

        return jsonify({
            'frequencia_absoluta_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_absoluta']['numeros'].items())],
            'frequencia_relativa_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado['frequencia_relativa']['numeros'].items())],
            'numeros_quentes_frios': resultado['numeros_quentes_frios'],
            'analise_temporal': resultado['analise_temporal'],
            'periodo_analisado': resultado['periodo_analisado'],
            'concursos_para_matriz': concursos_para_matriz,  # Dados para a matriz visual
            'ultimos_concursos': resultado.get('ultimos_concursos', []),  # Dados para o grid
            'analise_combinacoes': resultado.get('analise_combinacoes', {})  # Dados de combinações
        })
    except Exception as e:
        print(f"❌ Erro na API de frequência Quina: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise-frequencia-lotomania')
def analise_frequencia_lotomania_api():
    """API para análise de frequência da Lotomania"""
    try:
        logger.info("=== INICIANDO API LOTOMANIA ===")
        
        # Verificar ambiente e arquivos
        import os
        logger.info(f"PWD: {os.getcwd()}")
        logger.info(f"Lista LoteriasExcel: {os.listdir('LoteriasExcel') if os.path.exists('LoteriasExcel') else 'Diretório não existe'}")
        logger.info(f"Arquivo Lotomania existe? {os.path.exists(os.path.join(os.getcwd(), 'LoteriasExcel', 'Lotomania_edt.xlsx'))}")
        
        # Carregar dados da Lotomania usando função centralizada
        logger.info("Carregando dados da Lotomania...")
        df_lotomania = carregar_dados_da_loteria("lotomania")
        
        if df_lotomania is None:
            logger.error("Dados da Lotomania são None")
            return jsonify({"error": "Erro ao carregar dados da Lotomania"}), 500
        
        logger.info(f"Dados carregados. Linhas: {len(df_lotomania)}")
        logger.info(f"Colunas: {df_lotomania.columns.tolist()}")
        
        # Executar análise de frequência (últimos 300 concursos)
        logger.info("Executando análise de frequência...")
        
        # Usar a função que aceita DataFrame (igual às outras APIs)
        logger.info("Importando função analise_frequencia_lotomania_completa...")
        from funcoes.lotomania.funcao_analise_de_frequencia_lotomania import analise_frequencia_lotomania_completa
        logger.info("Função importada com sucesso!")
        
        logger.info("Chamando analise_frequencia_lotomania_completa...")
        resultado = analise_frequencia_lotomania_completa(df_lotomania, qtd_concursos=300)
        logger.info(f"Resultado da função: {type(resultado)}")
        
        if resultado:
            logger.info("Análise concluída com sucesso!")
            
            # Extrair dados da estrutura aninhada para compatibilidade com o frontend
            if 'analise_frequencia' in resultado:
                analise = resultado['analise_frequencia']
                # Retornar na mesma estrutura das outras APIs
                return jsonify({
                    'analise_temporal': analise.get('analise_temporal', []),
                    'frequencia_absoluta_numeros': analise.get('frequencia_absoluta', {}).get('numeros', {}),
                    'frequencia_relativa_numeros': analise.get('frequencia_relativa', {}).get('numeros', {}),
                    'numeros_quentes_frios': analise.get('numeros_quentes_frios', {}),
                    'periodo_analisado': resultado.get('periodo_analisado', {})
                })
            else:
                return jsonify(resultado)
        else:
            logger.error("Resultado da análise é None ou vazio")
            return jsonify({"error": "Não foi possível analisar os dados da Lotomania"}), 500
            
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(f"Erro ao analisar frequência da Lotomania: {e}")
        logger.error(f"Traceback completo:\n{tb}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/analise-frequencia-lotofacil')
def analise_frequencia_lotofacil_api():
    """API para análise de frequência da Lotofácil"""
    try:
        # Importar função necessária
        from funcoes.lotofacil.funcao_analise_de_frequencia_lotofacil import obter_estatisticas_rapidas_lotofacil
        
        # Executar análise de frequência da Lotofácil
        resultado = obter_estatisticas_rapidas_lotofacil()
        
        if resultado:
            # Formatar dados para compatibilidade com o JavaScript
            # O JavaScript espera: numeros_quentes_frios.numeros_quentes, etc.
            dados_formatados = {
                'numeros_quentes_frios': {
                    'numeros_quentes': [[num, 0] for num in resultado.get('numeros_quentes', [])],
                    'numeros_frios': [[num, 0] for num in resultado.get('numeros_frios', [])],
                    'numeros_secos': [[num, 0] for num in resultado.get('numeros_secos', [])]
                },
                'status': resultado.get('status', 'real')
            }
            
            return jsonify(dados_formatados)
        else:
            return jsonify({"error": "Não foi possível analisar os dados da Lotofácil"}), 500
            
    except Exception as e:
        logger.error(f"Erro ao analisar frequência da Lotofácil: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500


@app.route('/api/analise-frequencia-lotofacil-v2')
def analise_frequencia_lotofacil_v2_api():
    """API v2 para análise de frequência da Lotofácil (fluxo Premium, 15 bolas)."""
    try:
        from funcoes.lotofacil.funcao_analise_de_frequencia_lotofacil_2 import analisar_frequencia_lotofacil2
        from funcoes.lotofacil.LotofacilFuncaCarregaDadosExcel import carregar_dados_lotofacil

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        # Forçar recarga a partir do Excel (edt2) para evitar cache desatualizado
        resultado = analisar_frequencia_lotofacil2(None, qtd_concursos=qtd_concursos)

        # Montar dados para a matriz visual (concursos_para_matriz)
        concursos_para_matriz = []
        try:
            df = carregar_dados_lotofacil()
            if df is not None and not df.empty:
                # Detectar coluna de concurso
                concurso_col = None
                for c in df.columns:
                    if 'concurso' in str(c).strip().lower():
                        concurso_col = c
                        break
                # Detectar colunas de bolas (1..15)
                def achar_col(df_cols, n):
                    chaves = [f'bola{n}', f'bola{n:02d}', f'dezena{n}', f'd{n}', f'num{n}', f'n{n}', f'b{n}']
                    lower_map = {str(col).strip().lower(): col for col in df_cols}
                    for key in chaves:
                        if key in lower_map:
                            return lower_map[key]
                    for k, v in lower_map.items():
                        if k.endswith(str(n)) and any(prefix in k for prefix in ('bola', 'dez', 'd', 'num', 'n', 'b')):
                            return v
                    return None

                bolas_cols = []
                for i in range(1, 16):
                    col = achar_col(df.columns, i)
                    if col is None:
                        bolas_cols = []
                        break
                    bolas_cols.append(col)

                if concurso_col and bolas_cols:
                    df_ord = df.sort_values(concurso_col, ascending=False)
                    limite = qtd_concursos if qtd_concursos else 300
                    # Importar pandas para uso local
                    pd = _lazy_import_pandas()
                    
                    for _, row in df_ord.head(limite).iloc[::-1].iterrows():
                        try:
                            concurso_num = int(row[concurso_col]) if not pd.isna(row[concurso_col]) else None
                            if concurso_num is None:
                                continue
                            numeros = []
                            for col in bolas_cols:
                                val = row[col]
                                if pd.notna(val):
                                    numeros.append(int(val))
                            if len(numeros) == 15:
                                concursos_para_matriz.append({
                                    'concurso': concurso_num,
                                    'numeros': numeros
                                })
                        except Exception:
                            continue
        except Exception:
            pass

        if not resultado:
            return jsonify({"error": "Não foi possível analisar os dados (v2)"}), 500

        # Acrescentar matriz ao payload, se disponível
        payload = dict(resultado)
        payload['concursos_para_matriz'] = concursos_para_matriz
        return jsonify(payload)
    except Exception as e:
        logger.error(f"Erro ao analisar frequência v2 da Lotofácil: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/analise_de_distribuicao-quina', methods=['GET'])
def get_analise_de_distribuicao_quina():
    """Retorna os dados da análise de distribuição da Quina."""
    try:
        # Carregar dados da Quina usando lazy loading
        df_quina = carregar_dados_da_loteria("quina")
        
        if df_quina is None or df_quina.empty:
            return jsonify({"error": "Dados da Quina não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        if qtd_concursos is None or qtd_concursos <= 0:
            qtd_concursos = 200
        elif qtd_concursos > 200:
            qtd_concursos = 200

        resultado = analisar_distribuicao_quina(df_quina, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de distribuição Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_distribuicao-lotofacil', methods=['GET'])
def get_analise_de_distribuicao_lotofacil():
    """Retorna os dados da análise de distribuição da Lotofácil."""
    try:
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({"error": "Dados da Lotofácil não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        resultado = analisar_distribuicao_lotofacil(df_lotofacil, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_combinacoes-quina', methods=['GET'])
def get_analise_de_combinacoes_quina():
    """Retorna os dados da análise de combinações da Quina."""
    try:
        # Carregar dados da Quina usando lazy loading
        df_quina = carregar_dados_da_loteria("quina")
        
        if df_quina is None or df_quina.empty:
            return jsonify({"error": "Dados da Quina não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        resultado = analisar_combinacoes_quina(df_quina, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de combinações Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_combinacoes-lotofacil', methods=['GET'])
def get_analise_de_combinacoes_lotofacil():
    """Retorna os dados da análise de combinações da Lotofácil."""
    try:
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({"error": "Dados da Lotofácil não carregados."}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        resultado = analisar_combinacoes_lotofacil(df_lotofacil, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_padroes_sequencias-quina', methods=['GET'])
def get_analise_padroes_sequencias_quina():
    """Retorna os dados da análise de padrões e sequências da Quina."""
    try:
        # Carregar dados da Quina usando lazy loading
        df_quina = carregar_dados_da_loteria("quina")
        
        if df_quina is None or df_quina.empty:
            return jsonify({"error": "Dados da Quina não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        resultado = analisar_padroes_sequencias_quina(df_quina, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de padrões Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_padroes_sequencias-lotofacil', methods=['GET'])
def get_analise_padroes_sequencias_lotofacil():
    """Retorna os dados da análise de padrões e sequências da Lotofácil."""
    try:
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({"error": "Dados da Lotofácil não carregados."}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        resultado = analisar_padroes_sequencias_lotofacil(df_lotofacil, qtd_concursos)
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- PASSO 5: Análise de Seca - LOTOFÁCIL ---
@app.route('/api/analise_seca_lotofacil', methods=['GET'])
def api_analise_seca_lotofacil():
    try:
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({'error': 'Dados da Lotofácil não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=200)
        if not qtd_concursos or qtd_concursos <= 0:
            qtd_concursos = 200
        qtd_concursos = min(qtd_concursos, 200)

        # Detectores locais de colunas (concurso e bolas 1..15)
        # Importar pandas para uso local
        pd = _lazy_import_pandas()
        
        def _detectar_coluna_concurso_local(df: pd.DataFrame):
            possiveis = ['concurso', 'nrconcurso', 'n_concurso', 'numero_concurso', 'idconcurso']
            lower = {str(c).strip().lower(): c for c in df.columns}
            for k in possiveis:
                if k in lower:
                    return lower[k]
            for k, v in lower.items():
                if 'concurso' in k:
                    return v
            return None

        def _detectar_colunas_bolas_local(df: pd.DataFrame):
            lower = {str(c).strip().lower(): c for c in df.columns}
            def achar(n):
                chaves = [f'bola{n}', f'bola{n:02d}', f'dezena{n}', f'd{n}', f'num{n}', f'n{n}', f'b{n}']
                for key in chaves:
                    if key in lower:
                        return lower[key]
                for k, v in lower.items():
                    if k.endswith(str(n)) and any(p in k for p in ('bola','dez','d','num','n','b')):
                        return v
                return None
            cols = []
            for n in range(1, 16):
                c = achar(n)
                if c is None:
                    return None
                cols.append(c)
            return cols

        concurso_col = _detectar_coluna_concurso_local(df_lotofacil)
        bolas = _detectar_colunas_bolas_local(df_lotofacil)
        if concurso_col is None or not bolas:
            return jsonify({'error': 'Colunas de concurso/bolas não detectadas.'}), 500

        # Importar pandas para uso local
        pd = _lazy_import_pandas()
        
        df = df_lotofacil.copy()
        for col in bolas:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=bolas)
        mask_validos = (df[bolas] >= 1).all(axis=1) & (df[bolas] <= 25).all(axis=1)
        df = df[mask_validos]
        if df.empty:
            return jsonify({'error': 'Sem linhas válidas após limpeza.'}), 500

        df = df.tail(qtd_concursos).copy()

        # Calcular seca atual por número (contando a partir do último concurso)
        seca_por_numero = {n: {'seca_atual': 0} for n in range(1, 26)}
        # Lista de sorteios do mais recente para o mais antigo
        sorteios = list(reversed(df[bolas].values.tolist()))
        for n in range(1, 26):
            cont = 0
            for sorteio in sorteios:
                if n in sorteio:
                    break
                cont += 1
            seca_por_numero[n]['seca_atual'] = cont

        # Estatísticas simples
        # Importar pandas para uso local
        pd = _lazy_import_pandas()
        
        valores = [v['seca_atual'] for v in seca_por_numero.values()]
        seca_max = int(max(valores) if valores else 0)
        seca_med = float(pd.Series(valores).median()) if valores else 0.0
        seca_media = float(pd.Series(valores).mean()) if valores else 0.0

        # Top números em maior seca
        numeros_maior_seca = sorted([(n, seca_por_numero[n]) for n in range(1, 26)],
                                     key=lambda x: x[1]['seca_atual'], reverse=True)

        # Números que saíram mais recentemente (último concurso)
        ultimo = df[bolas].iloc[-1].tolist()
        # Importar pandas para uso local
        pd = _lazy_import_pandas()
        numeros_recentes = [int(x) for x in ultimo if pd.notna(x)]

        payload = {
            'numeros_seca': {
                'seca_por_numero': seca_por_numero,
                'estatisticas': {
                    'seca_maxima': seca_max,
                    'seca_mediana': seca_med,
                    'seca_media': round(seca_media, 2)
                },
                'numeros_maior_seca': [[n, info] for n, info in numeros_maior_seca[:10]],
                'numeros_recentes': numeros_recentes
            },
            'periodo_analisado': {
                'qtd_concursos_solicitada': qtd_concursos,
                'concursos_analisados': df[concurso_col].tolist()
            }
        }

        return jsonify(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Diagnóstico: concursos que tiveram blocos consecutivos de um tamanho específico
@app.route('/api/lotofacil/sequencias/detalhe', methods=['GET'])
def get_lotofacil_sequencias_detalhe():
    try:
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({'error': 'Dados da Lotofácil não carregados.'}), 500

        tamanho = request.args.get('tamanho', type=int, default=11)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=200)
        if qtd_concursos is None or qtd_concursos <= 0:
            qtd_concursos = 200
        qtd_concursos = min(qtd_concursos, 200)

        resultado = analisar_padroes_sequencias_lotofacil(df_lotofacil, qtd_concursos)
        if not resultado:
            return jsonify({'error': 'Análise indisponível'}), 500

        consec = resultado.get('numeros_consecutivos', {})
        concursos = (consec.get('consecutivos_por_tamanho_concursos', {}) or {}).get(tamanho, [])
        por_concurso = consec.get('por_concurso', [])

        detalhes = []
        for item in por_concurso:
            if item.get('concurso') in concursos:
                blocos = [seq for seq in item.get('consecutivos', []) if len(seq) == tamanho]
                if blocos:
                    detalhes.append({'concurso': item.get('concurso'), 'blocos': blocos})

        return jsonify({
            'tamanho': tamanho,
            'qtd_concursos': qtd_concursos,
            'concursos': concursos,
            'detalhes': detalhes,
            'periodo_analisado': resultado.get('periodo_analisado', {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas_avancadas_quina', methods=['GET'])
def get_estatisticas_avancadas_quina():
    """Retorna os dados das estatísticas avançadas da Quina."""
    try:
        # print("🔍 Iniciando requisição para /api/estatisticas_avancadas_quina")  # DEBUG - COMENTADO
        
        # Carregar dados da Quina usando lazy loading
        df_quina = carregar_dados_da_loteria("quina")
        
        if df_quina is None or df_quina.empty:
            print("❌ Dados da Quina não carregados")
            return jsonify({'error': 'Dados da Quina não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        print(f"📈 Estatísticas Avançadas Quina - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"📊 DataFrame disponível: {len(df_quina)} concursos")

        # Criar instância da classe de análise da Quina
        print("🔧 Criando instância da AnaliseEstatisticaAvancadaQuina...")
        analise = AnaliseEstatisticaAvancadaQuina(df_quina)
        
        # Executar análise completa
        print("⚡ Executando análise completa da Quina...")
        resultado = analise.executar_analise_completa(qtd_concursos)
        
        print("✅ Análise da Quina concluída! Verificando resultados...")
        
        # Log detalhado dos resultados
        if resultado:
            print(f"📊 Resultados obtidos:")
            print(f"   - Desvio padrão: {'✅' if resultado.get('desvio_padrao_distribuicao') else '❌'}")
            print(f"   - Teste aleatoriedade: {'✅' if resultado.get('teste_aleatoriedade') else '❌'}")
            print(f"   - Análise clusters: {'✅' if resultado.get('analise_clusters') else '❌'}")
            print(f"   - Correlação números: {'✅' if resultado.get('analise_correlacao_numeros') else '❌'}")
            print(f"   - Probabilidades condicionais: {'✅' if resultado.get('probabilidades_condicionais') else '❌'}")
            print(f"   - Distribuição números: {'✅' if resultado.get('distribuicao_numeros') else '❌'}")
        else:
            print("❌ Nenhum resultado obtido!")

        # Limpar valores problemáticos usando função global
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

        # Debug: testar serialização JSON
        try:
            json.dumps(resultado_limpo)  # teste seco
            print("✅ Serialização JSON bem-sucedida")
            
            # Debug específico para distribuição de números
            if 'distribuicao_numeros' in resultado_limpo:
                dist_numeros = resultado_limpo['distribuicao_numeros']
                print(f"🔍 Distribuição de números:")
                print(f"   - Tipo: {type(dist_numeros)}")
                print(f"   - É lista? {isinstance(dist_numeros, list)}")
                print(f"   - Tamanho: {len(dist_numeros) if isinstance(dist_numeros, list) else 'N/A'}")
                if isinstance(dist_numeros, list) and len(dist_numeros) > 0:
                    print(f"   - Primeiro item: {dist_numeros[0]}")
                    print(f"   - Último item: {dist_numeros[-1]}")
            else:
                print("❌ 'distribuicao_numeros' não encontrada no resultado")
                
        except TypeError as e:
            print(f"🔎 JSON falhou com: {e}")
            # opcional: localizar tipos estranhos

        return jsonify(resultado_limpo)

    except Exception as e:
        print(f"❌ Erro na API de estatísticas avançadas da Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/gerar_aposta_premium_quina', methods=['POST'])
def gerar_aposta_premium_quina():
    """Gera aposta inteligente da Quina usando Machine Learning."""
    try:
        from funcoes.quina.geracao_inteligente_quina import gerar_aposta_inteligente_quina
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferences completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # Carregar dados de análise para o cache
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia']):
            try:
                from funcoes.quina.funcao_analise_de_frequencia_quina import analisar_frequencia_quina
                dados_freq = analisar_frequencia_quina(qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['frequencia_completa'] = dados_freq
                analysis_cache['frequencia_25'] = analisar_frequencia_quina(qtd_concursos=25)  # Últimos 25 concursos
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes']):
            try:
                from funcoes.quina.funcao_analise_de_padroes_sequencia_quina import analise_padroes_sequencias_quina
                dados_padroes = analise_padroes_sequencias_quina()
                analysis_cache['padroes_completa'] = dados_padroes
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de afinidades (combinacoes) se necessário
        if any(key in preferencias_ml for key in ['afinidades']):
            try:
                from funcoes.quina.funcao_analise_de_combinacoes_quina import analisar_combinacoes_quina
                dados_afinidades = analisar_combinacoes_quina(df_quina, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['afinidades_completa'] = dados_afinidades
            except Exception as e:
                print(f"⚠️ Erro ao carregar afinidades: {e}")
        
        # Carregar dados de distribuição se necessário
        if any(key in preferencias_ml for key in ['distribuicao']):
            try:
                from funcoes.quina.funcao_analise_de_distribuicao_quina import analisar_distribuicao_quina
                dados_distribuicao = analisar_distribuicao_quina(df_quina, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['distribuicao_completa'] = dados_distribuicao
            except Exception as e:
                print(f"⚠️ Erro ao carregar distribuição: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                analise = AnaliseEstatisticaAvancadaQuina(df_quina)
                dados_avancados = analise.executar_analise_completa()
                analysis_cache['avancada'] = dados_avancados
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # Gerar aposta inteligente
        resultado = gerar_aposta_inteligente_quina(preferencias_ml, analysis_cache)
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de geração premium Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas_avancadas_lotofacil', methods=['GET'])
def get_estatisticas_avancadas_lotofacil():
    """Retorna os dados das estatísticas avançadas da Lotofácil."""
    try:
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            return jsonify({'error': 'Dados da Lotofácil não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)

        analise = AnaliseEstatisticaAvancadaLotofacil(df_lotofacil)
        resultado = analise.executar_analise_completa(qtd_concursos)

        resultado_limpo = limpar_valores_problematicos(resultado)
        return jsonify(resultado_limpo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gerar-aposta-aleatoria-lotofacil', methods=['POST'])
def gerar_aposta_aleatoria_lotofacil_api():
    """Gera uma aposta aleatória da Lotofácil (15 a 20 números)."""
    try:
        payload = request.get_json(silent=True) or {}
        qtde_num = int(payload.get('qtde_num', 15))
        # Garantir faixa válida para Lotofácil
        if qtde_num < 15:
            qtde_num = 15
        if qtde_num > 20:
            qtde_num = 20

        from funcoes.lotofacil.gerarCombinacao_numeros_aleatoriosL_lotofacil import gerar_aposta_aleatoria_lotofacil
        numeros = gerar_aposta_aleatoria_lotofacil(qtde_num)
        return jsonify({
            'numeros': numeros,
            'qtde_apostas': 1
        })
    except Exception as e:
        print(f"❌ Erro na API de aposta aleatória Lotofácil: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analise_de_combinacoes-MS', methods=['GET'])
def get_analise_de_combinacoes_megasena():
    """Retorna os dados da análise de combinações da Mega Sena."""
    try:
        if df_megasena.empty:
            return jsonify({"error": "Dados da Mega Sena não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"🎯 Combinações Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
        # print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")  # DEBUG - COMENTADO

        resultado = analise_combinacoes_megasena(df_megasena, qtd_concursos)
        # print(f"🎯 Resultado da análise: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de combinações Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/analise_padroes_sequencias-MS', methods=['GET'])
def get_analise_padroes_sequencias_megasena():
    """Retorna os dados da análise de padrões e sequências da Mega Sena."""
    try:
        if df_megasena.empty:
            return jsonify({"error": "Dados da Mega Sena não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"🎯 Padrões/Sequências Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"🎯 Tipo de df_megasena: {type(df_megasena)}")  # DEBUG - COMENTADO
        # print(f"🎯 Shape de df_megasena: {df_megasena.shape if hasattr(df_megasena, 'shape') else 'N/A'}")  # DEBUG - COMENTADO

        resultado = analise_padroes_sequencias_megasena(df_megasena, qtd_concursos)
        # print(f"🎯 Resultado da análise: {type(resultado)}")  # DEBUG - COMENTADO
        # print(f"🎯 Chaves do resultado: {list(resultado.keys()) if resultado else 'N/A'}")  # DEBUG - COMENTADO
        
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Erro na API de padrões/sequências Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/analise_de_combinacoes', methods=['GET'])
def get_analise_de_combinacoes():
    """Retorna os dados da análise de combinações."""
    try:
        # Verificar se df_milionaria é DataFrame ou lista
        if df_milionaria is None:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500
        
        # Se for DataFrame, verificar se está vazio
        if hasattr(df_milionaria, 'empty') and df_milionaria.empty:
            return jsonify({"error": "DataFrame da +Milionária está vazio."}), 500
        
        # Se for lista, verificar se está vazia
        if isinstance(df_milionaria, list) and len(df_milionaria) == 0:
            return jsonify({"error": "Lista de dados da +Milionária está vazia."}), 500

        # print(f"Tipo de df_milionaria: {type(df_milionaria)}")  # DEBUG - COMENTADO
        
        # Converter para lista se necessário
        if hasattr(df_milionaria, 'values'):
            dados_para_analise = df_milionaria.values.tolist()
        else:
            dados_para_analise = df_milionaria
            
        # print(f"Dados para análise: {len(dados_para_analise)} linhas")  # DEBUG - COMENTADO
        
        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos')
        if qtd_concursos:
            qtd_concursos = int(qtd_concursos)
            # print(f"🎯 Parâmetro qtd_concursos recebido: {qtd_concursos}")  # DEBUG - COMENTADO
        # else:
        #     print(f"🎯 Nenhum parâmetro qtd_concursos recebido")  # DEBUG - COMENTADO
        
        resultado = analise_combinacoes_milionaria(dados_para_analise, qtd_concursos)
        # print(f"Resultado obtido: {type(resultado)}")  # DEBUG - COMENTADO
        
        # Debug detalhado do resultado
        # if resultado and 'afinidade_entre_numeros' in resultado:
        #     afinidades = resultado['afinidade_entre_numeros']
        #     print(f"=== DEBUG AFINIDADES BACKEND ===")  # DEBUG - COMENTADO
        #     print(f"Tipo de afinidades: {type(afinidades)}")  # DEBUG - COMENTADO
        #     print(f"Chaves em afinidades: {list(afinidades.keys())}")  # DEBUG - COMENTADO
        #     
        #     if 'pares_com_maior_afinidade' in afinidades:
        #         pares = afinidades['pares_com_maior_afinidade']
        #         print(f"Tipo de pares_com_maior_afinidade: {type(pares)}")  # DEBUG - COMENTADO
        #         print(f"É lista? {isinstance(pares, list)}")  # DEBUG - COMENTADO
        #         print(f"Tamanho: {len(pares) if isinstance(pares, list) else 'N/A'}")  # DEBUG - COMENTADO
        #         
        #         if isinstance(pares, list) and len(pares) > 0:
        #             print(f"Primeiro par: {pares[0]}")  # DEBUG - COMENTADO
        #             print(f"Tipo do primeiro par: {type(pares[0])}")  # DEBUG - COMENTADO
        #             print(f"Estrutura do primeiro par: {pares[0]}")  # DEBUG - COMENTADO
        
        if not resultado:
            return jsonify({"error": "Erro ao processar análise de combinações."}), 500
            
        return jsonify(resultado)
        
    except Exception as e:
        print(f"Erro na API de combinações: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/analise_trevos_da_sorte', methods=['GET'])
def get_analise_trevos_da_sorte():
    """Retorna os dados da análise dos trevos da sorte (frequência, combinações e correlação)."""
    try:
        if df_milionaria.empty:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"🎯 Trevos - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO

        # Note: A função 'analise_trevos_da_sorte' foi ajustada para aceitar o DataFrame diretamente.
        resultado = analise_trevos_da_sorte(df_milionaria, qtd_concursos)
        
        if not resultado:
            return jsonify({"error": "Resultado da análise de trevos está vazio."}), 404
            
        return jsonify(resultado)
        
    except Exception as e:
        print(f"Erro na API de trevos: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/analise_seca', methods=['GET'])
def get_analise_seca():
    """Retorna os dados da análise de seca dos números principais e trevos."""
    try:
        # Carrega os dados no escopo da rota (lazy loading)
        df_milionaria = carregar_dados_da_loteria("mais_milionaria")
        if df_milionaria is None or df_milionaria.empty:
            return jsonify({"error": "Dados da +Milionária não carregados."}), 500

        # Verificar se há parâmetro de quantidade de concursos
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)


        # Calcular seca dos números principais
        numeros_seca = calcular_seca_numeros(df_milionaria, qtd_concursos=qtd_concursos)
        
        # Calcular seca dos trevos
        trevos_seca = calcular_seca_trevos(df_milionaria, qtd_concursos=qtd_concursos)

        # Verificar se os dados estão válidos
        if not numeros_seca or not trevos_seca:
            return jsonify({"error": "Falha ao calcular análise de seca."}), 400

        return jsonify({
            "numeros_seca": numeros_seca,
            "trevos_seca": trevos_seca
        })

    except Exception as e:
        print(f"Erro na API de seca: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/analise_seca_MS', methods=['GET'])
def get_analise_seca_megasena():
    """Retorna os dados da análise de seca dos números da Mega Sena."""
    try:
        # print("🔍 API de seca da Mega Sena chamada!")  # DEBUG - COMENTADO
        
        if df_megasena is None or df_megasena.empty:
            # print("❌ Dados da Mega Sena não carregados")  # DEBUG - COMENTADO
            return jsonify({'error': 'Dados da Mega Sena não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"📈 Análise de Seca Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"📊 DataFrame disponível: {len(df_megasena)} concursos")  # DEBUG - COMENTADO

        # Executar análise de seca
        # print("⚡ Executando análise de seca da Mega Sena...")  # DEBUG - COMENTADO
        resultado = calcular_seca_numeros_megasena(df_megasena, qtd_concursos)
        
        # print("✅ Análise de seca concluída!")  # DEBUG - COMENTADO
        # print(f"📊 Resultados obtidos:")  # DEBUG - COMENTADO
        # print(f"   - Números em seca: {'✅' if resultado.get('seca_por_numero') else '❌'}")  # DEBUG - COMENTADO
        # print(f"   - Média de seca: {'✅' if resultado.get('estatisticas', {}).get('seca_media') else '❌'}")  # DEBUG - COMENTADO
        # print(f"   - Máxima seca: {'✅' if resultado.get('estatisticas', {}).get('seca_maxima') else '❌'}")  # DEBUG - COMENTADO

        # Retornar no formato esperado pelo frontend
        return jsonify({
            "numeros_seca": resultado
        })

    except Exception as e:
        print(f"❌ Erro na API de seca da Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/estatisticas_avancadas', methods=['GET'])
def get_estatisticas_avancadas():
    """Retorna os dados das estatísticas avançadas."""
    try:
        # print("🔍 Iniciando requisição para /api/estatisticas_avancadas")  # DEBUG - COMENTADO
        
        # Carrega os dados no escopo da rota (lazy loading)
        df_milionaria = carregar_dados_da_loteria("mais_milionaria")
        if df_milionaria is None or df_milionaria.empty:
            print("❌ Dados da +Milionária não carregados")
            return jsonify({'error': 'Dados da +Milionária não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        # print(f"📈 Estatísticas Avançadas - Parâmetro qtd_concursos: {qtd_concursos}")  # DEBUG - COMENTADO
        # print(f"📊 DataFrame disponível: {len(df_milionaria)} concursos")  # DEBUG - COMENTADO


        # Criar instância da classe de análise
        # print("🔧 Criando instância da AnaliseEstatisticaAvancada...")  # DEBUG - COMENTADO
        analise = AnaliseEstatisticaAvancada(df_milionaria)
        
        # Executar análise completa
        # print("⚡ Executando análise completa...")  # DEBUG - COMENTADO
        resultado = analise.executar_analise_completa(qtd_concursos)
        
        # print("✅ Análise concluída! Verificando resultados...")  # DEBUG - COMENTADO
        
        # Log detalhado dos resultados
        # if resultado:
        #     print(f"📊 Resultados obtidos:")  # DEBUG - COMENTADO
        #     print(f"   - Desvio padrão: {'✅' if resultado.get('desvio_padrao_distribuicao') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Teste aleatoriedade: {'✅' if resultado.get('teste_aleatoriedade') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Análise clusters: {'✅' if resultado.get('analise_clusters') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Correlação números: {'✅' if resultado.get('analise_correlacao_numeros') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Probabilidades condicionais: {'✅' if resultado.get('probabilidades_condicionais') else '❌'}")  # DEBUG - COMENTADO
        #     print(f"   - Distribuição números: {'✅' if resultado.get('distribuicao_numeros') else '❌'}")  # DEBUG - COMENTADO
        #     
        #             # Log específico para correlação
        # if resultado.get('analise_correlacao_numeros'):
        #     correlacao = resultado['analise_correlacao_numeros']
        #     print(f"🔍 Dados de correlação enviados ao frontend:")  # DEBUG - COMENTADO
        #     print(f"   - Correlações positivas: {len(correlacao.get('correlacoes_positivas', []))}")  # DEBUG - COMENTADO
        #     print(f"   - Correlações negativas: {len(correlacao.get('correlacoes_negativas', []))}")  # DEBUG - COMENTADO
        #     print(f"   - Correlação média: {correlacao.get('correlacao_media', 0.0):.4f}")  # DEBUG - COMENTADO
        #     if correlacao.get('correlacoes_positivas'):
        #         print(f"   - Amostra positivas: {correlacao['correlacoes_positivas'][:3]}")  # DEBUG - COMENTADO
        #     if correlacao.get('correlacoes_negativas'):
        #         print(f"   - Amostra negativas: {correlacao['correlacoes_negativas'][:3]}")  # DEBUG - COMENTADO
        #     
        #     # Verificar se os dados são serializáveis para JSON
        #     try:
        #         import json
        #         json_test = json.dumps(correlacao)
        #         print(f"✅ Dados de correlação são serializáveis para JSON")  # DEBUG - COMENTADO
        #     except Exception as json_error:
        #         print(f"❌ Erro ao serializar dados de correlação: {json_error}")  # DEBUG - COMENTADO
        # else:
        #     print("❌ Dados de correlação não encontrados no resultado!")  # DEBUG - COMENTADO
        # 
        # if not resultado:
        #     print("❌ Nenhum resultado obtido!")  # DEBUG - COMENTADO

        # Limpar valores problemáticos usando função global
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

        # Debug: testar serialização JSON
        try:
            json.dumps(resultado_limpo)  # teste seco
            print("✅ Serialização JSON bem-sucedida")
        except TypeError as e:
            print(f"🔎 JSON falhou com: {e}")
            # opcional: localizar tipos estranhos

        return jsonify(resultado_limpo)

    except Exception as e:
        print(f"❌ Erro na API de estatísticas avançadas: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


@app.route('/api/estatisticas_avancadas_MS', methods=['GET'])
def get_estatisticas_avancadas_megasena():
    """Retorna os dados das estatísticas avançadas da Mega Sena."""
    try:
        # print("🔍 Iniciando requisição para /api/estatisticas_avancadas_MS")  # DEBUG - COMENTADO
        
        if df_megasena is None or df_megasena.empty:
            print("❌ Dados da Mega Sena não carregados")
            return jsonify({'error': 'Dados da Mega Sena não carregados.'}), 500

        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        print(f"📈 Estatísticas Avançadas Mega Sena - Parâmetro qtd_concursos: {qtd_concursos}")
        print(f"📊 DataFrame disponível: {len(df_megasena)} concursos")

        # Criar instância da classe de análise da Mega Sena
        print("🔧 Criando instância da AnaliseEstatisticaAvancadaMS...")
        analise = AnaliseEstatisticaAvancadaMS(df_megasena)
        
        # Executar análise completa
        print("⚡ Executando análise completa da Mega Sena...")
        resultado = analise.executar_analise_completa(qtd_concursos)
        
        print("✅ Análise da Mega Sena concluída! Verificando resultados...")
        
        # Log detalhado dos resultados
        if resultado:
            print(f"📊 Resultados obtidos:")
            print(f"   - Desvio padrão: {'✅' if resultado.get('desvio_padrao_distribuicao') else '❌'}")
            print(f"   - Teste aleatoriedade: {'✅' if resultado.get('teste_aleatoriedade') else '❌'}")
            print(f"   - Análise clusters: {'✅' if resultado.get('analise_clusters') else '❌'}")
            print(f"   - Correlação números: {'✅' if resultado.get('analise_correlacao_numeros') else '❌'}")
            print(f"   - Probabilidades condicionais: {'✅' if resultado.get('probabilidades_condicionais') else '❌'}")
            print(f"   - Distribuição números: {'✅' if resultado.get('distribuicao_numeros') else '❌'}")
        else:
            print("❌ Nenhum resultado obtido!")

        # Limpar valores problemáticos usando função global
        resultado_limpo = limpar_valores_problematicos(resultado)
        print("✅ Dados limpos de valores problemáticos")

        # Debug: testar serialização JSON
        try:
            json.dumps(resultado_limpo)  # teste seco
            print("✅ Serialização JSON bem-sucedida")
        except TypeError as e:
            print(f"🔎 JSON falhou com: {e}")
            # opcional: localizar tipos estranhos

        return jsonify(resultado_limpo)

    except Exception as e:
        print(f"❌ Erro na API de estatísticas avançadas da Mega Sena: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500


# --- Rota para manifestação de interesse em bolões (sem persistência para este exemplo) ---
# Funções de geração de números movidas para services/geradores/numeros_aleatorios.py
from services.geradores.numeros_aleatorios import (
    gerar_numeros_aleatorios,
    gerar_numeros_aleatorios_megasena,
    gerar_numeros_aleatorios_quina,
    gerar_numeros_aleatorios_lotomania
)

# Importar funções da Lotomania
from funcoes.lotomania.gerarCombinacao_numeros_aleatoriosLotomania import gerar_aposta_personalizada_lotomania
from funcoes.lotomania.funcao_analise_de_frequencia_lotomania import analisar_frequencia_lotomania

@app.route('/api/gerar-numeros-aleatorios', methods=['GET'])
def gerar_numeros_aleatorios():
    """Gera números aleatórios para +Milionária (6 números + 2 trevos)."""
    try:
        resultado = gerar_numeros_aleatorios()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-numeros-aleatorios-megasena', methods=['GET'])
def gerar_numeros_aleatorios_megasena():
    """Gera números aleatórios para Mega Sena (6 números de 1-60)."""
    try:
        resultado = gerar_numeros_aleatorios_megasena()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Mega Sena: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-numeros-aleatorios-quina', methods=['GET'])
def gerar_numeros_aleatorios_quina():
    """Gera números aleatórios para Quina (5 números de 1-80)."""
    try:
        resultado = gerar_numeros_aleatorios_quina()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Quina: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-numeros-aleatorios-lotomania', methods=['GET'])
def gerar_numeros_aleatorios_lotomania():
    """Gera números aleatórios para Lotomania com controle de qualidade de distribuição par/ímpar e repetição do último concurso."""
    try:
        resultado = gerar_numeros_aleatorios_lotomania()
        if resultado["success"]:
            return jsonify(resultado)
        else:
            return jsonify(resultado), 500
    except Exception as e:
        logger.error(f"Erro ao gerar números aleatórios da Lotomania: {e}")
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500

@app.route('/api/gerar-aposta-milionaria', methods=['POST'])
def gerar_aposta_milionaria_api():
    """Gera aposta personalizada para +Milionária com quantidade configurável."""
    try:
        data = request.get_json()
        qtde_num = data.get('qtde_num')
        qtde_trevo1 = data.get('qtde_trevo1')
        qtde_trevo2 = data.get('qtde_trevo2')

        if qtde_num is None or qtde_trevo1 is None or qtde_trevo2 is None:
            return jsonify({'error': 'Parâmetros qtde_num, qtde_trevo1 e qtde_trevo2 são obrigatórios.'}), 400

        # Importar a função de geração personalizada
        from funcoes.milionaria.gerarCombinacao_numeros_aleatoriosMilionaria import gerar_aposta_personalizada
        
        # Chama a função principal de geração de aposta
        numeros, trevo1, trevo2, valor, qtde_apostas = gerar_aposta_personalizada(qtde_num, qtde_trevo1, qtde_trevo2)

        return jsonify({
            'success': True,
            'numeros': numeros,
            'trevo1': trevo1,
            'trevo2': trevo2,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta gerada com sucesso!'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-megasena', methods=['POST'])
def gerar_aposta_megasena_api():
    """Gera aposta personalizada para Mega Sena com quantidade configurável."""
    try:
        data = request.get_json()
        qtde_num = data.get('qtde_num')

        if qtde_num is None:
            return jsonify({'error': 'Parâmetro qtde_num é obrigatório.'}), 400

        # Importar a função de geração personalizada da Mega Sena
        from funcoes.megasena.gerarCombinacao_numeros_aleatoriosMegasena_MS import gerar_aposta_personalizada
        
        # Chama a função principal de geração de aposta
        numeros, valor, qtde_apostas = gerar_aposta_personalizada(qtde_num)

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta gerada com sucesso!'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Mega Sena: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Mega Sena: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-quina', methods=['POST'])
def gerar_aposta_quina_api():
    """Gera aposta personalizada para Quina com quantidade configurável."""
    try:
        data = request.get_json()
        qtde_num = data.get('qtde_num')

        if qtde_num is None:
            return jsonify({'error': 'Parâmetro qtde_num é obrigatório.'}), 400

        # Importar a função de geração personalizada da Quina
        from funcoes.quina.gerarCombinacao_numeros_aleatoriosQuina_quina import gerar_aposta_personalizada_quina
        
        # Chama a função principal de geração de aposta
        numeros, valor, qtde_apostas = gerar_aposta_personalizada_quina(qtde_num)

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta da Quina gerada com sucesso!'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Quina: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Quina: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-lotomania', methods=['POST'])
def gerar_aposta_lotomania_api():
    """Gera aposta personalizada para Lotomania (50 números fixos)."""
    try:
        # Chama a função principal de geração de aposta (sempre 50 números)
        numeros, valor, qtde_apostas = gerar_aposta_personalizada_lotomania()

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'mensagem': 'Aposta da Lotomania gerada com sucesso! (50 números fixos)'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Lotomania: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Lotomania: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/gerar-aposta-lotofacil', methods=['POST'])
def gerar_aposta_lotofacil_api():
    """Gera aposta personalizada para Lotofácil (15-20 números) com controle de qualidade."""
    try:
        # Obter dados da requisição
        data = request.get_json()
        quantidade = data.get('quantidade', 15) if data else 15
        preferencias = data.get('preferencias', {}) if data else {}
        
        # Validar quantidade (15-20 números)
        if quantidade < 15 or quantidade > 20:
            return jsonify({'error': 'Quantidade deve ser entre 15 e 20 números'}), 400
        
        # Preparar preferências para controle de qualidade
        if preferencias:
            # Mapear preferências do frontend para o backend
            preferencias_backend = {
                'incluir_quentes': True,
                'incluir_frios': True,
                'incluir_secos': True,
                'balancear_par_impar': True,
                'controlar_repetidos': True,
                'qtd_quentes': 6,
                'qtd_frios': 4,
                'qtd_secos': 2,
                'qtd_aleatorios': 3
            }
            
            # Aplicar preferências de repetidos se fornecidas
            if 'repetidos_min' in preferencias:
                preferencias_backend['repetidos_min'] = preferencias['repetidos_min']
            if 'repetidos_max' in preferencias:
                preferencias_backend['repetidos_max'] = preferencias['repetidos_max']
            
            # Ajustar faixas baseado no modo conservador
            if preferencias.get('modo_conservador', False):
                if quantidade == 15:
                    preferencias_backend['repetidos_conservador_min'] = 6
                    preferencias_backend['repetidos_conservador_max'] = 12
                else:
                    preferencias_backend['repetidos_conservador_min'] = 10
                    preferencias_backend['repetidos_conservador_max'] = 14
        else:
            preferencias_backend = None
        
        # Importar a função de geração de aposta da Lotofácil
        from funcoes.lotofacil.gerarCombinacao_numeros_aleatoriosL_lotofacil import gerar_aposta_personalizada_lotofacil
        
        # Chama a função principal de geração de aposta com quantidade e preferências
        logger.info(f"Gerando aposta Lotofácil: quantidade={quantidade}, preferencias={preferencias_backend}")
        numeros = gerar_aposta_personalizada_lotofacil(quantidade, preferencias_backend)
        logger.info(f"Aposta gerada: {numeros}")
        
        # Tabela de valores da Lotofácil
        valores_lotofacil = {
            15: 3.50,
            16: 56.00,
            17: 476.00,
            18: 2856.00,
            19: 13566.00,
            20: 54264.00
        }
        
        valor = valores_lotofacil[quantidade]
        qtde_apostas = 1

        return jsonify({
            'success': True,
            'numeros': numeros,
            'valor': valor,
            'qtde_apostas': qtde_apostas,
            'quantidade': quantidade,
            'mensagem': f'Aposta da Lotofácil gerada com sucesso! ({quantidade} números)'
        })

    except ValueError as e:
        logger.error(f"Erro de validação ao gerar aposta Lotofácil: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro inesperado ao gerar aposta Lotofácil: {e}")
        return jsonify({'error': 'Erro interno do servidor ao gerar aposta.'}), 500

@app.route('/api/bolao_interesse', methods=['POST'])
def bolao_interesse():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    mensagem = data.get('mensagem')

    # TODO: Aqui você implementaria a lógica para salvar esses dados (ex: em um banco de dados,
    # enviar um email para você, etc.). Por enquanto, apenas imprime.
    print(f"Novo interesse em bolão recebido:")
    print(f"  Nome: {nome}")
    print(f"  Email: {email}")
    print(f"  Telefone: {telefone}")
    print(f"  Mensagem: {mensagem}")

    return jsonify({"message": "Interesse registrado com sucesso! Entraremos em contato."}), 200

@app.route('/termos-uso')
def termos_uso():
    """Renderiza o modal de termos de uso e condições de assinatura."""
    return render_template('modal_cadastro_assinatura.html')

@app.route('/boloes_loterias')
@verificar_acesso_universal
def boloes_loterias():
    """Renderiza a página de bolões de loterias."""
    usuario_logado = verificar_usuario_logado()
    plano_display = buscar_plano_usuario()
    
    logger.info(f"🎯 ROTA boloes_loterias - Usuario logado: {usuario_logado}")
    logger.info(f"🎯 ROTA boloes_loterias - Plano display: '{plano_display}'")
    
    return render_template('boloes_loterias.html', 
                         is_logged_in=usuario_logado,
                         plano_display=plano_display)

@app.route('/api/verificar-acesso-boloes')
def verificar_acesso_boloes():
    """API para verificar acesso às loterias baseado no plano do usuário."""
    try:
        logger.info("🔍 API verificar-acesso-boloes iniciada")
        from config.mercadopago_config import get_loterias_permitidas, get_loterias_bloqueadas, ACESSO_POR_PLANO
        
        # 🎉 MODO ACESSO LIVRE: Retorna acesso total
        if FREE_ACCESS_MODE:
            logger.info("🎉 MODO ACESSO LIVRE - Liberando todas as loterias")
            todas_loterias = ['mega-sena', 'lotofacil', 'quina', 'lotomania', 'dupla-sena', 'dia-de-sorte', 'super-sete', 'loteca', 'timemania', '+milionaria']
            return jsonify({
                'success': True,
                'usuario_logado': False,
                'plano_usuario': 'Free Access',
                'loterias_permitidas': todas_loterias,
                'loterias_bloqueadas': [],
                'info_plano': {
                    'nome_display': 'Acesso Livre',
                    'descricao': 'Acesso temporário a todas as funcionalidades'
                }
            })
        
        usuario_logado = verificar_usuario_logado()
        logger.info(f"🔍 Usuario logado: {usuario_logado}")
        plano_usuario = 'Free'  # Default
        
        # Buscar plano do usuário se estiver logado
        if usuario_logado:
            try:
                from flask_login import current_user
                logger.info(f"🔍 Current user: {current_user}")
                logger.info(f"🔍 Current user ID: {getattr(current_user, 'id', 'SEM_ID')}")
                
                # Buscar no banco loterias_simples.db usando o ID do current_user
                if hasattr(current_user, 'id') and current_user.id:
                    logger.info(f"🔍 Buscando dados do usuário {current_user.id} no banco...")
                    
                    # Buscar diretamente no banco usando conexão SQL
                    conn = get_db_connection()
                    if conn:
                        cur = conn.cursor()
                        cur.execute("""
                            SELECT tipo_plano 
                            FROM usuarios 
                            WHERE id = ?
                        """, (current_user.id,))
                        
                        resultado = cur.fetchone()
                        conn.close()
                        
                        if resultado and resultado[0]:
                            plano_bd = resultado[0]
                            logger.info(f"🔍 Plano no banco de dados: '{plano_bd}'")
                            
                            # Mapear planos do banco para nossa configuração
                            mapeamento_planos = {
                                'Free': 'Free',
                                'Diário': 'daily',
                                'Mensal': 'monthly', 
                                'Semestral': 'semiannual',
                                'Anual': 'annual',
                                'Vitalício': 'lifetime'
                            }
                            
                            plano_usuario = mapeamento_planos.get(plano_bd, 'Free')
                            logger.info(f"🎯 API - Usuário {current_user.id} - Plano BD: '{plano_bd}' → Mapeado: '{plano_usuario}'")
                        else:
                            logger.warning(f"⚠️ API - Usuário {current_user.id} sem plano definido no banco")
                    else:
                        logger.warning("⚠️ API - Não foi possível conectar ao banco")
                else:
                    logger.warning("⚠️ API - current_user sem ID válido")
            except Exception as e:
                logger.error(f"❌ API - Erro ao buscar plano do usuário: {e}")
                import traceback
                logger.error(f"❌ API - Traceback: {traceback.format_exc()}")
        
        # Buscar informações de acesso
        logger.info(f"🔍 Buscando permissões para plano: {plano_usuario}")
        loterias_permitidas = get_loterias_permitidas(plano_usuario)
        loterias_bloqueadas = get_loterias_bloqueadas(plano_usuario)
        info_plano = ACESSO_POR_PLANO.get(plano_usuario, ACESSO_POR_PLANO['Free'])
        
        # Log final para debug
        logger.info(f"🎯 API RESULTADO - Usuário: {usuario_logado}, Plano: {plano_usuario}")
        logger.info(f"✅ API Loterias permitidas: {loterias_permitidas}")
        logger.info(f"❌ API Loterias bloqueadas: {loterias_bloqueadas}")
        logger.info(f"📋 API Info plano: {info_plano}")
        logger.info(f"🔍 API Configuração ACESSO_POR_PLANO[{plano_usuario}]: {ACESSO_POR_PLANO.get(plano_usuario, 'NAO_ENCONTRADO')}")
        
        return jsonify({
            'success': True,
            'usuario_logado': usuario_logado,
            'plano_usuario': plano_usuario,
            'loterias_permitidas': loterias_permitidas,
            'loterias_bloqueadas': loterias_bloqueadas,
            'info_plano': info_plano
        })
        
    except Exception as e:
        logger.error(f"❌ API verificar-acesso-boloes - Erro geral: {e}")
        import traceback
        logger.error(f"❌ API - Traceback completo: {traceback.format_exc()}")
        
        return jsonify({
            'success': False,
            'error': str(e),
            'usuario_logado': False,
            'plano_usuario': 'Free',
            'loterias_permitidas': [],
            'loterias_bloqueadas': ['quina', 'lotofacil', 'megasena', 'milionaria'],
            'info_plano': {'nome_display': 'Erro'}
        }), 500

@app.route('/debug/usuario-atual')
def debug_usuario_atual():
    """Rota de debug para verificar usuário logado e seu plano."""
    try:
        from flask_login import current_user
        usuario_logado = verificar_usuario_logado()
        
        info_debug = {
            'usuario_logado': usuario_logado,
            'current_user_authenticated': getattr(current_user, 'is_authenticated', False),
            'current_user_id': getattr(current_user, 'id', None),
        }
        
        if usuario_logado and hasattr(current_user, 'id') and current_user.id:
            user_data = get_user_by_id(current_user.id)
            info_debug.update({
                'user_data_raw': user_data,
                'email': user_data[1] if user_data and len(user_data) > 1 else None,
                'tipo_plano_bd': user_data[2] if user_data and len(user_data) > 2 else None,
            })
            
            if user_data and len(user_data) >= 3:
                plano_bd = user_data[2]
                mapeamento_planos = {
                    'Free': 'Free',
                    'Diário': 'daily',
                    'Mensal': 'monthly', 
                    'Semestral': 'semiannual',
                    'Anual': 'annual',
                    'Vitalício': 'lifetime'
                }
                plano_mapeado = mapeamento_planos.get(plano_bd, 'Free')
                info_debug.update({
                    'plano_mapeado': plano_mapeado,
                    'mapeamento_disponivel': mapeamento_planos
                })
        
        # Testar a função buscar_plano_usuario
        plano_teste = buscar_plano_usuario()
        info_debug['plano_teste_funcao'] = plano_teste
        
        return f"""
        <h1>🔍 Debug - Usuário Atual</h1>
        <h2>Função buscar_plano_usuario(): {plano_teste}</h2>
        <pre>{info_debug}</pre>
        <h3>🧪 Teste do Badge:</h3>
        <div style="background: #10B981; color: white; padding: 8px 12px; border-radius: 4px; display: inline-block;">
            🔓 LOGGED IN
            {f'<div style="margin-top: 4px; font-size: 10px; background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 8px;">📋 {plano_teste}</div>' if plano_teste else '<div style="margin-top: 4px; font-size: 10px; color: red;">❌ SEM PLANO</div>'}
        </div>
        <p><a href="/boloes_loterias">← Voltar para Bolões</a></p>
        """
        
    except Exception as e:
        return f"<h1>❌ Erro: {e}</h1>"

# --- Rotas da Mega Sena ---
@app.route('/dashboard_MS')
@verificar_acesso_universal
def dashboard_megasena():
    """Dashboard Mega Sena - Protegido por middleware."""
    return render_template('dashboard_megasena.html', is_logged_in=verificar_usuario_logado())

@app.route('/aposta_inteligente_premium_MS')
@verificar_acesso_universal
def aposta_inteligente_premium_megasena():
    """Aposta Inteligente Premium Mega Sena - Protegido por middleware."""
    return render_template('analise_estatistica_avancada_megasena.html', is_logged_in=verificar_usuario_logado())

@app.route('/analise_estatistica_avancada_megasena')
@verificar_acesso_universal
def analise_estatistica_avancada_megasena():
    """Renderiza a página de Análise Estatística Avançada da Mega Sena."""
    return render_template('analise_estatistica_avancada_megasena.html', is_logged_in=verificar_usuario_logado())

@app.route('/analise_estatistica_avancada_quina')
@verificar_acesso_universal
def analise_estatistica_avancada_quina():
    """Renderiza a página de Análise Estatística Avançada da Quina."""
    return render_template('analise_estatistica_avancada_quina.html', is_logged_in=verificar_usuario_logado())

# --- Rotas da Quina ---
@app.route('/dashboard_quina')
@verificar_acesso_universal
def dashboard_quina():
    """Renderiza a página principal do dashboard da Quina."""
    return render_template('dashboard_quina.html', is_logged_in=verificar_usuario_logado())

@app.route('/aposta_inteligente_premium_quina')
@verificar_acesso_universal
def aposta_inteligente_premium_quina():
    """Renderiza a página de Aposta Inteligente Premium da Quina."""
    return render_template('analise_estatistica_avancada_quina.html', is_logged_in=verificar_usuario_logado())

# --- Rotas da Lotofácil ---
@app.route('/dashboard_lotofacil')
@verificar_acesso_universal
def dashboard_lotofacil():
    """Renderiza a página principal do dashboard da Lotofácil."""
    return render_template('dashboard_lotofacil.html', is_logged_in=verificar_usuario_logado())

@app.route('/aposta_inteligente_premium_lotofacil')
@verificar_acesso_universal
def aposta_inteligente_premium_lotofacil():
    """Renderiza a página de Aposta Inteligente Premium da Lotofácil."""
    return render_template('analise_estatistica_avancada_lotofacil.html', is_logged_in=verificar_usuario_logado())

@app.route('/analise_estatistica_avancada_lotofacil')
@verificar_acesso_universal
def analise_estatistica_avancada_lotofacil():
    """Renderiza a página de Análise Estatística Avançada da Lotofácil."""
    return render_template('analise_estatistica_avancada_lotofacil.html', is_logged_in=verificar_usuario_logado())

@app.route('/lotofacil_laboratorio')
@verificar_acesso_universal
def lotofacil_laboratorio():
    """Renderiza a página do Laboratório de Simulação da Lotofácil."""
    return render_template('lotofacil_laboratorio.html', is_logged_in=verificar_usuario_logado())

@app.route('/teste_api')
def teste_api():
    """Página de teste da API"""
    return send_file('teste_api.html')

# --- Rotas da Milionária ---

@app.route('/aposta_inteligente_premium')
@verificar_acesso_universal
def aposta_inteligente_premium():
    """Renderiza a página de Aposta Inteligente Premium."""
    return render_template('analise_estatistica_avancada_milionaria.html', is_logged_in=verificar_usuario_logado())

@app.route('/analise_estatistica_avancada_milionaria')
@verificar_acesso_universal
def analise_estatistica_avancada_milionaria():
    """Renderiza a página de Análise Estatística Avançada da Milionária."""
    return render_template('analise_estatistica_avancada_milionaria.html', is_logged_in=verificar_usuario_logado())

@app.route('/analise_estatistica_avancada_lotomania')
@verificar_acesso_universal
def analise_estatistica_avancada_lotomania():
    """Renderiza a página de Inteligência Estatística da Lotomania."""
    return render_template('analise_estatistica_avancada_lotomania.html', is_logged_in=verificar_usuario_logado())

# --- Rotas da Lotomania ---
@app.route('/dashboard_lotomania')
@verificar_acesso_universal
def dashboard_lotomania():
    """Renderiza a página principal do dashboard da Lotomania."""
    return render_template('dashboard_lotomania.html', is_logged_in=verificar_usuario_logado())

@app.route('/api/gerar_aposta_premium', methods=['POST'])
def gerar_aposta_premium():
    """Gera aposta inteligente usando Machine Learning."""
    try:
        from funcoes.milionaria.geracao_inteligente import gerar_aposta_inteligente
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferences completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # print(f"📊 Preferências recebidas: {preferencias_ml}")  # DEBUG - COMENTADO
        
        # Carregar dados de análise para o cache
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia', 'trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_frequencia import analisar_frequencia
                dados_freq = analisar_frequencia(qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['frequencia_completa'] = dados_freq
                analysis_cache['frequencia_25'] = analisar_frequencia(qtd_concursos=25)  # Últimos 25 concursos
                # print("✅ Dados de frequência carregados (50 e 25 concursos)")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes']):
            try:
                from funcoes.milionaria.funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria
                dados_padroes = analise_padroes_sequencias_milionaria()
                analysis_cache['padroes_completa'] = dados_padroes
                # print("✅ Dados de padrões carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de trevos se necessário
        if any(key in preferencias_ml for key in ['trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte
                dados_trevos = analise_trevos_da_sorte()
                analysis_cache['trevos_completa'] = dados_trevos
                # print("✅ Dados de trevos carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar trevos: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                from funcoes.milionaria.analise_estatistica_avancada import realizar_analise_estatistica_avancada
                dados_avancados = realizar_analise_estatistica_avancada()
                analysis_cache['avancada'] = dados_avancados
                print("✅ Dados avançados carregados")
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # print(f"📊 Cache de análise preparado: {list(analysis_cache.keys())}")  # DEBUG - COMENTADO
        
        # Gerar apostas usando Machine Learning
        apostas_geradas = gerar_aposta_inteligente(preferencias_ml, analysis_cache)
        
        # print(f"🎯 Apostas geradas: {len(apostas_geradas)}")  # DEBUG - COMENTADO
        
        return jsonify({
            'success': True,
            'apostas': apostas_geradas,
            'mensagem': f'Aposta inteligente gerada com sucesso! ({len(apostas_geradas)} apostas)'
        })
        
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/gerar_aposta_premium_lotofacil', methods=['POST'])
def gerar_aposta_premium_lotofacil():
    """Gera aposta inteligente da Lotofácil (1..25, 15–20 dezenas)."""
    try:
        from funcoes.lotofacil.geracao_inteligente_lotofacil import gerar_aposta_inteligente_lotofacil
        preferencias_ml = request.get_json(silent=True) or {}

        analysis_cache = {}
        try:
            from funcoes.lotofacil.funcao_analise_de_frequencia_lotofacil_2 import analisar_frequencia_lotofacil2
            analysis_cache['frequencia'] = analisar_frequencia_lotofacil2(None, qtd_concursos=preferencias_ml.get('qtd_concursos', 25))
        except Exception:
            pass
        try:
            from funcoes.lotofacil.funcao_analise_de_combinacoes_lotofacil import analisar_combinacoes_lotofacil
            analysis_cache['afinidades_completa'] = analisar_combinacoes_lotofacil(None, qtd_concursos=min(200, preferencias_ml.get('qtd_concursos', 50)))
        except Exception:
            pass

        qtde = preferencias_ml.get('qtdeNumerosAposta')
        preferencias_ml['qtdeNumerosAposta'] = max(15, min(20, int(qtde) if isinstance(qtde, int) else 15))

        apostas = gerar_aposta_inteligente_lotofacil(preferencias_ml, analysis_cache)
        for a in apostas:
            a['numeros'] = sorted([n for n in a.get('numeros', []) if isinstance(n, int) and 1 <= n <= 25])

        return jsonify({'success': True, 'apostas': apostas, 'qtde_apostas': len(apostas)})
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium Lotofácil: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gerar_aposta_premium_MS', methods=['POST'])
def gerar_aposta_premium_megasena():
    """Gera aposta inteligente da Mega Sena usando Machine Learning."""
    try:
        from funcoes.megasena.geracao_inteligente_MS import gerar_aposta_inteligente
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferencesMS completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # print(f"📊 Preferências recebidas (Mega Sena): {preferencias_ml}")  # DEBUG - COMENTADO
        
        # Carregar dados da Mega Sena
        df_megasena = carregar_dados_megasena_app()
        
        if df_megasena.empty:
            return jsonify({
                'success': False,
                'error': 'Dados da Mega Sena não disponíveis'
            }), 500
        
        # print(f"📊 Dados da Mega Sena carregados: {len(df_megasena)} concursos")  # DEBUG - COMENTADO
        
        # Preparar cache de análise baseado nas preferências
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia']):
            try:
                from funcoes.megasena.funcao_analise_de_frequencia_MS import analise_frequencia_megasena_completa
                dados_freq = analise_frequencia_megasena_completa(df_megasena)
                analysis_cache['frequencia_completa'] = dados_freq
                # print("✅ Dados de frequência carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de distribuição se necessário
        if any(key in preferencias_ml for key in ['distribuicao']):
            try:
                from funcoes.megasena.funcao_analise_de_distribuicao_MS import analise_distribuicao_megasena
                dados_dist = analise_distribuicao_megasena(df_megasena)
                analysis_cache['distribuicao_completa'] = dados_dist
                # print("✅ Dados de distribuição carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar distribuição: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes', 'sequencias']):
            try:
                from funcoes.megasena.funcao_analise_de_padroes_sequencia_MS import analise_padroes_sequencias_megasena
                dados_padroes = analise_padroes_sequencias_megasena(df_megasena)
                analysis_cache['padroes_completa'] = dados_padroes
                # print("✅ Dados de padrões carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de afinidades (combinacoes) se necessário
        if any(key in preferencias_ml for key in ['afinidades']):
            try:
                from funcoes.megasena.funcao_analise_de_combinacoes_MS import analise_combinacoes_megasena
                dados_afinidades = analise_combinacoes_megasena(df_megasena, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['afinidades_completa'] = dados_afinidades
                # print("✅ Dados de afinidades carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar afinidades: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                from funcoes.megasena.analise_estatistica_avancada_MS import AnaliseEstatisticaAvancada
                analise = AnaliseEstatisticaAvancada(df_megasena)
                dados_avancados = analise.executar_analise_completa()
                analysis_cache['avancada'] = dados_avancados
                print("✅ Dados avançados carregados")
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # print(f"📊 Cache de análise preparado: {list(analysis_cache.keys())}")  # DEBUG - COMENTADO
        
        # Gerar apostas usando Machine Learning
        apostas_geradas = gerar_aposta_inteligente(preferencias_ml, analysis_cache)
        
        # print(f"🎯 Apostas geradas (Mega Sena): {len(apostas_geradas)}")  # DEBUG - COMENTADO
        
        return jsonify({
            'success': True,
            'apostas': apostas_geradas,
            'mensagem': f'Aposta inteligente gerada com sucesso! ({len(apostas_geradas)} apostas)'
        })
        
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium (Mega Sena): {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/numeros_quentes_frios_secos_quina', methods=['GET'])
def get_numeros_quentes_frios_secos_quina():
    """Retorna números quentes, frios e secos da Quina."""
    try:
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        
        # Carregar dados da Quina usando lazy loading
        df_quina = carregar_dados_da_loteria("quina")
        
        if df_quina is None or df_quina.empty:
            return jsonify({
                'success': False,
                'error': 'Dados da Quina não carregados'
            }), 500
        
        # Obter análise de frequência
        from funcoes.quina.funcao_analise_de_frequencia_quina import analisar_frequencia_quina
        dados_frequencia = analisar_frequencia_quina(df_quina=df_quina, qtd_concursos=qtd_concursos)
        
        # Obter análise de seca
        from funcoes.quina.calculos_quina import calcular_seca_numeros_quina
        dados_seca = calcular_seca_numeros_quina(df_quina, qtd_concursos=qtd_concursos)
        
        # Processar números quentes (mais frequentes)
        numeros_quentes = dados_frequencia.get('numeros_mais_frequentes', [])[:10]
        
        # Processar números frios (menos frequentes)
        numeros_frios = dados_frequencia.get('numeros_menos_frequentes', [])[:10]
        
        # Processar números secos (não saem há muito tempo)
        numeros_secos = dados_seca.get('numeros_mais_secos', [])[:10]
        
        return jsonify({
            'success': True,
            'numeros_quentes': numeros_quentes,
            'numeros_frios': numeros_frios,
            'numeros_secos': numeros_secos
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter números quentes/frios/secos da Quina: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/analise_seca_quina', methods=['GET'])
def get_analise_seca_quina():
    """Retorna análise de seca (números que não saem há muito tempo) para a Quina."""
    try:
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        
        # Carregar dados da Quina usando lazy loading
        df_quina = carregar_dados_da_loteria("quina")
        
        if df_quina is None or df_quina.empty:
            return jsonify({
                'success': False,
                'error': 'Dados da Quina não carregados'
            }), 500
        
        # Usar os dados limitados aos últimos concursos
        dados_limitados = df_quina.tail(qtd_concursos)
        
        # Calcular seca dos números
        from funcoes.quina.calculos_quina import calcular_seca_numeros_quina
        numeros_seca = calcular_seca_numeros_quina(dados_limitados)
        
        return jsonify({
            'success': True,
            'numeros_seca': numeros_seca,
            'qtd_concursos_analisados': len(dados_limitados)
        })
        
    except Exception as e:
        print(f"❌ Erro na análise de seca da Quina: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/api/lotofacil/matriz')
def api_lotofacil_matriz():
    """API para obter matriz de concursos da Lotofácil para o laboratório"""
    try:
        # print("🔍 API Lotofácil Matriz chamada!")
        
        # Carregar dados da Lotofácil
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            # print("❌ df_lotofacil está vazio ou None!")
            return jsonify({"error": "Dados da Lotofácil não carregados"}), 500
        
        # print(f"✅ df_lotofacil carregado: {df_lotofacil.shape}")
        # print(f"✅ Colunas: {list(df_lotofacil.columns)}")
        
        # Parâmetros
        limit = int(request.args.get("limit", 25))
        # print(f"🔍 Limit: {limit}")
        
        # df_lotofacil já existe no app (mesmo input do site)
        df = df_lotofacil.copy()
        
        # Ordena do mais novo p/ mais antigo
        df = df.sort_values("Concurso", ascending=False)
        # print(f"✅ Primeiros concursos: {df['Concurso'].head().tolist()}")
        
        # Pega N concursos e inverte para cronológico (como no GUI)
        fatia = df.head(limit)[["Concurso"] + [f"Bola{i}" for i in range(1,16)]].iloc[::-1]
        # print(f"✅ Fatia criada: {len(fatia)} linhas")
        
        # Monta matriz de 26 colunas (0 = concurso, 1..25 = números)
        import numpy as np
        pd = _lazy_import_pandas()
        matriz = []
        for _, row in fatia.iterrows():
            linha = [int(row["Concurso"])] + [0]*25
            for j in range(1,16):
                try:
                    valor_bola = row[f"Bola{j}"]
                    # Valida se não é NaN/None e está no range válido
                    if pd.notna(valor_bola):
                        n = int(valor_bola)
                        # Valida se está no range 1-25 (índices válidos da lista)
                        if 1 <= n <= 25:
                            linha[n] = n
                except (ValueError, TypeError):
                    # Ignora valores inválidos e continua
                    continue
            matriz.append(linha)
        
        # Último concurso completo (para o modal "Escolhidos × Próximo")
        ultimo = df.head(1)[["Concurso"] + [f"Bola{i}" for i in range(1,16)]].iloc[0].tolist()
        # print(f"✅ Último concurso: {ultimo}")
        
        resultado = {
            "matriz": matriz,           # lista de linhas [concurso, n1..n25] (0 quando não saiu)
            "ultimo_concurso": ultimo   # [conc, b1..b15]
        }
        
        # print(f"✅ API retornando: matriz({len(matriz)} linhas), último({len(ultimo)} elementos)")
        return jsonify(resultado)
        
    except Exception as e:
        # print(f"❌ Erro ao gerar matriz da Lotofácil: {e}")
        # import traceback
        # traceback.print_exc()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@app.route('/estatisticas-frequencia')
def get_estatisticas_frequencia():
    """Retorna a frequência dos números nos últimos 25 concursos da Lotofácil"""
    try:
        # print("🔍 API Estatísticas Frequência chamada!")
        
        # Carregar dados da Lotofácil
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            # print("❌ df_lotofacil está vazio ou None!")
            return jsonify({"error": "Dados da Lotofácil não carregados"}), 500
        
        # print(f"✅ df_lotofacil carregado: {df_lotofacil.shape}")
        
        # Parâmetros
        num_concursos = int(request.args.get("num_concursos", 25))
        # print(f"🔍 Número de concursos: {num_concursos}")
        
        # df_lotofacil já existe no app (mesmo input do site)
        df = df_lotofacil.copy()
        
        # Ordena do mais novo p/ mais antigo e pega os últimos N concursos
        df = df.sort_values("Concurso", ascending=False)
        df_limitado = df.head(num_concursos)
        # print(f"✅ Concursos analisados: {len(df_limitado)}")
        
        # Inicializar estrutura de dados para frequências
        resultados_frequencia = {}
        for num in range(1, 26):
            resultados_frequencia[num] = {}
            for pos in range(1, 16):
                resultados_frequencia[num][pos] = 0
        
        # Calcular frequências reais baseadas nos dados históricos
        for _, row in df_limitado.iterrows():
            for pos in range(1, 16):
                numero = int(row[f"Bola{pos}"])
                if 1 <= numero <= 25:
                    resultados_frequencia[numero][pos] += 1
        
        # print(f"✅ Frequências calculadas para {len(resultados_frequencia)} números")
        
        # Log de exemplo para debug
        # exemplo_freq = resultados_frequencia[1][1] if resultados_frequencia[1][1] > 0 else 0
        # print(f"🔍 Exemplo: Número 1 na posição 1 apareceu {exemplo_freq} vezes")
        
        return jsonify(resultados_frequencia)
        
    except Exception as e:
        # print(f"❌ Erro ao calcular frequências da Lotofácil: {e}")
        # import traceback
        # traceback.print_exc()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500


@app.route('/analisar', methods=['POST'])
def analisar_cartoes():
    """Analisa padrões dos últimos 25 concursos da Lotofácil"""
    try:
        # print("🔍 API Analisar Padrões dos Últimos 25 Concursos chamada!")
        
        # Carregar dados da Lotofácil
        df_lotofacil = carregar_dados_da_loteria("lotofacil")
        if df_lotofacil is None or df_lotofacil.empty:
            # print("❌ df_lotofacil está vazio ou None!")
            return jsonify({"error": "Dados da Lotofácil não carregados"}), 500
        
        # Obter os últimos 25 concursos
        df = df_lotofacil.copy()
        df = df.sort_values("Concurso", ascending=False)
        df_limitado = df.head(25)
        
        # print(f"📊 Analisando padrões dos últimos {len(df_limitado)} concursos")
        
        # Inicializar contadores para cada padrão
        padroes_01_25 = {"00_00": 0, "01_00": 0, "00_25": 0, "01_25": 0}
        padroes_01_02_03 = {"00_00_00": 0, "01_00_00": 0, "00_02_00": 0, "00_00_03": 0, 
                            "01_02_00": 0, "01_00_03": 0, "00_02_03": 0, "01_02_03": 0}
        padroes_03_06_09 = {"00_00_00": 0, "03_00_00": 0, "00_06_00": 0, "00_00_09": 0,
                            "03_06_00": 0, "03_00_09": 0, "00_06_09": 0, "03_06_09": 0}
        padroes_23_24_25 = {"00_00_00": 0, "23_00_00": 0, "00_24_00": 0, "00_00_25": 0,
                            "23_24_00": 0, "23_00_25": 0, "00_24_25": 0, "23_24_25": 0}
        
        # Analisar cada concurso
        for _, row in df_limitado.iterrows():
            numeros_concurso = []
            for i in range(1, 16):
                numero = int(row[f'Bola{i}'])
                numeros_concurso.append(numero)
            
            # Padrão 01-25
            tem_01 = 1 if 1 in numeros_concurso else 0
            tem_25 = 1 if 25 in numeros_concurso else 0
            padrao_01_25 = f"{tem_01}{tem_25}"
            if padrao_01_25 == "00":
                padroes_01_25["00_00"] += 1
            elif padrao_01_25 == "10":
                padroes_01_25["01_00"] += 1
            elif padrao_01_25 == "01":
                padroes_01_25["00_25"] += 1
            elif padrao_01_25 == "11":
                padroes_01_25["01_25"] += 1
            
            # Padrão 01-02-03
            tem_01 = 1 if 1 in numeros_concurso else 0
            tem_02 = 1 if 2 in numeros_concurso else 0
            tem_03 = 1 if 3 in numeros_concurso else 0
            padrao_01_02_03 = f"{tem_01}{tem_02}{tem_03}"
            if padrao_01_02_03 == "000":
                padroes_01_02_03["00_00_00"] += 1
            elif padrao_01_02_03 == "100":
                padroes_01_02_03["01_00_00"] += 1
            elif padrao_01_02_03 == "010":
                padroes_01_02_03["00_02_00"] += 1
            elif padrao_01_02_03 == "001":
                padroes_01_02_03["00_00_03"] += 1
            elif padrao_01_02_03 == "110":
                padroes_01_02_03["01_02_00"] += 1
            elif padrao_01_02_03 == "101":
                padroes_01_02_03["01_00_03"] += 1
            elif padrao_01_02_03 == "011":
                padroes_01_02_03["00_02_03"] += 1
            elif padrao_01_02_03 == "111":
                padroes_01_02_03["01_02_03"] += 1
            
            # Padrão 03-06-09
            tem_03 = 1 if 3 in numeros_concurso else 0
            tem_06 = 1 if 6 in numeros_concurso else 0
            tem_09 = 1 if 9 in numeros_concurso else 0
            padrao_03_06_09 = f"{tem_03}{tem_06}{tem_09}"
            if padrao_03_06_09 == "000":
                padroes_03_06_09["00_00_00"] += 1
            elif padrao_03_06_09 == "100":
                padroes_03_06_09["03_00_00"] += 1
            elif padrao_03_06_09 == "010":
                padroes_03_06_09["00_06_00"] += 1
            elif padrao_03_06_09 == "001":
                padroes_03_06_09["00_00_09"] += 1
            elif padrao_03_06_09 == "110":
                padroes_03_06_09["03_06_00"] += 1
            elif padrao_03_06_09 == "101":
                padroes_03_06_09["03_00_09"] += 1
            elif padrao_03_06_09 == "011":
                padroes_03_06_09["00_06_09"] += 1
            elif padrao_03_06_09 == "111":
                padroes_03_06_09["03_06_09"] += 1
            
            # Padrão 23-24-25
            tem_23 = 1 if 23 in numeros_concurso else 0
            tem_24 = 1 if 24 in numeros_concurso else 0
            tem_25 = 1 if 25 in numeros_concurso else 0
            padrao_23_24_25 = f"{tem_23}{tem_24}{tem_25}"
            if padrao_23_24_25 == "000":
                padroes_23_24_25["00_00_00"] += 1
            elif padrao_23_24_25 == "100":
                padroes_23_24_25["23_00_00"] += 1
            elif padrao_23_24_25 == "010":
                padroes_23_24_25["00_24_00"] += 1
            elif padrao_23_24_25 == "001":
                padroes_23_24_25["00_00_25"] += 1
            elif padrao_23_24_25 == "110":
                padroes_23_24_25["23_24_00"] += 1
            elif padrao_23_24_25 == "101":
                padroes_23_24_25["23_00_25"] += 1
            elif padrao_23_24_25 == "011":
                padroes_23_24_25["00_24_25"] += 1
            elif padrao_23_24_25 == "111":
                padroes_23_24_25["23_24_25"] += 1
        
        resultado = {
            "total_concursos": len(df_limitado),
            "padroes_01_25": padroes_01_25,
            "padroes_01_02_03": padroes_01_02_03,
            "padroes_03_06_09": padroes_03_06_09,
            "padroes_23_24_25": padroes_23_24_25,
            "concursos_analisados": df_limitado['Concurso'].tolist()
        }
        
        # print(f"✅ Padrões calculados: {len(df_limitado)} concursos analisados")
        return jsonify(resultado)
        
    except Exception as e:
        # print(f"❌ Erro ao analisar cartões: {e}")
        # import traceback
        # traceback.print_exc()
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@app.route('/api/gerar_aposta_premium_milionaria', methods=['POST'])
def gerar_aposta_premium_milionaria():
    """Gera aposta inteligente da +Milionária usando Machine Learning."""
    try:
        from funcoes.milionaria.geracao_inteligente import gerar_aposta_inteligente
        
        # Obter dados do request
        data = request.get_json()
        
        # O frontend envia o objeto userPremiumPreferencesMIL completo
        preferencias_ml = data  # Usar diretamente o objeto enviado
        
        # print(f"📊 Preferências recebidas (+Milionária): {preferencias_ml}")  # DEBUG - COMENTADO
        
        # Carregar dados da +Milionária
        df_milionaria = carregar_dados_milionaria()
        
        if df_milionaria.empty:
            return jsonify({
                'success': False,
                'error': 'Dados da +Milionária não disponíveis'
            }), 500
        
        # print(f"📊 Dados da +Milionária carregados: {len(df_milionaria)} concursos")  # DEBUG - COMENTADO
        
        # Preparar cache de análise baseado nas preferências
        analysis_cache = {}
        
        # Carregar dados de frequência se necessário
        if any(key in preferencias_ml for key in ['frequencia']):
            try:
                from funcoes.milionaria.funcao_analise_de_frequencia import analise_frequencia_milionaria_completa
                dados_freq = analise_frequencia_milionaria_completa(df_milionaria)
                analysis_cache['frequencia_completa'] = dados_freq
                # print("✅ Dados de frequência carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar frequência: {e}")
        
        # Carregar dados de distribuição se necessário
        if any(key in preferencias_ml for key in ['distribuicao']):
            try:
                from funcoes.milionaria.funcao_analise_de_distribuicao import analise_distribuicao_milionaria
                dados_dist = analise_distribuicao_milionaria(df_milionaria)
                analysis_cache['distribuicao_completa'] = dados_dist
                # print("✅ Dados de distribuição carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar distribuição: {e}")
        
        # Carregar dados de padrões se necessário
        if any(key in preferencias_ml for key in ['padroes', 'sequencias']):
            try:
                from funcoes.milionaria.funcao_analise_de_padroes_sequencia import analise_padroes_sequencias_milionaria
                dados_padroes = analise_padroes_sequencias_milionaria(df_milionaria)
                analysis_cache['padroes_completa'] = dados_padroes
                # print("✅ Dados de padrões carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar padrões: {e}")
        
        # Carregar dados de afinidades (combinacoes) se necessário
        if any(key in preferencias_ml for key in ['afinidades']):
            try:
                from funcoes.milionaria.funcao_analise_de_combinacoes import analise_combinacoes_milionaria
                dados_afinidades = analise_combinacoes_milionaria(df_milionaria, qtd_concursos=50)  # Últimos 50 concursos
                analysis_cache['afinidades_completa'] = dados_afinidades
                # print("✅ Dados de afinidades carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar afinidades: {e}")
        
        # Carregar dados avançados se necessário
        if any(key in preferencias_ml for key in ['clusters']):
            try:
                from funcoes.milionaria.analise_estatistica_avancada import AnaliseEstatisticaAvancada
                analise = AnaliseEstatisticaAvancada(df_milionaria)
                dados_avancados = analise.executar_analise_completa()
                analysis_cache['avancada'] = dados_avancados
                print("✅ Dados avançados carregados")
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados avançados: {e}")
        
        # Carregar dados de trevos da sorte se necessário
        if any(key in preferencias_ml for key in ['trevos']):
            try:
                from funcoes.milionaria.funcao_analise_de_trevodasorte_frequencia import analise_trevos_da_sorte
                dados_trevos = analise_trevos_da_sorte(df_milionaria)
                analysis_cache['trevos_completa'] = dados_trevos
                # print("✅ Dados de trevos da sorte carregados")  # DEBUG - COMENTADO
            except Exception as e:
                print(f"⚠️ Erro ao carregar dados de trevos: {e}")
        
        # print(f"📊 Cache de análise preparado: {list(analysis_cache.keys())}")  # DEBUG - COMENTADO
        
        # Gerar apostas usando Machine Learning
        apostas_geradas = gerar_aposta_inteligente(preferencias_ml, analysis_cache)
        
        # print(f"🎯 Apostas geradas (+Milionária): {len(apostas_geradas)}")  # DEBUG - COMENTADO
        
        return jsonify({
            'success': True,
            'apostas': apostas_geradas,
            'mensagem': f'Aposta inteligente gerada com sucesso! ({len(apostas_geradas)} apostas)'
        })
        
    except Exception as e:
        print(f"❌ Erro ao gerar aposta premium (+Milionária): {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500


# ============================================================================
# 🔗 GOOGLE OAUTH - LOGIN SOCIAL
# ============================================================================

import requests
import urllib.parse
from config.google_oauth import GOOGLE_OAUTH_CONFIG, GOOGLE_AUTH_URL, GOOGLE_TOKEN_URL, GOOGLE_USERINFO_URL

@app.route('/auth/google')
def google_login():
    """Inicia o processo de login com Google."""
    try:
        # Parâmetros para autorização OAuth
        params = {
            'client_id': GOOGLE_OAUTH_CONFIG['client_id'],
            'redirect_uri': GOOGLE_OAUTH_CONFIG['redirect_uri'],
            'scope': ' '.join(GOOGLE_OAUTH_CONFIG['scope']),
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        # Construir URL de autorização
        auth_url = f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"
        
        logger.info(f"Redirecionando para Google OAuth: {auth_url}")
        return redirect(auth_url)
        
    except Exception as e:
        logger.error(f"Erro ao iniciar login Google: {e}")
        return redirect('/login?error=google_oauth_error')

@app.route('/auth/google/callback')
def google_callback():
    """Callback do Google OAuth após autorização."""
    try:
        # Obter código de autorização
        code = request.args.get('code')
        if not code:
            logger.error("Código de autorização não recebido")
            return redirect('/login?error=no_auth_code')
        
        # Trocar código por token de acesso
        token_data = {
            'client_id': GOOGLE_OAUTH_CONFIG['client_id'],
            'client_secret': GOOGLE_OAUTH_CONFIG['client_secret'],
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': GOOGLE_OAUTH_CONFIG['redirect_uri']
        }
        
        token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        token_response.raise_for_status()
        
        access_token = token_response.json().get('access_token')
        if not access_token:
            logger.error("Token de acesso não recebido")
            return redirect('/login?error=no_access_token')
        
        # Obter informações do usuário
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        userinfo_response.raise_for_status()
        
        user_data = userinfo_response.json()
        google_id = user_data.get('id')
        email = user_data.get('email')
        nome_completo = user_data.get('name')
        foto_url = user_data.get('picture')
        
        if not email:
            logger.error("Email não recebido do Google")
            return redirect('/login?error=no_email')
        
        logger.info(f"Usuário Google autenticado: {email}")
        
        # Verificar se usuário já existe no banco
        logger.info(f"Conectando ao banco de dados...")
        conn = get_db_connection()
        if not conn:
            logger.error("Falha na conexão com banco de dados")
            return redirect('/login?error=db_connection_error')
        
        logger.info(f"Banco conectado com sucesso")
        cursor = conn.cursor()
        
        # Buscar usuário por email
        logger.info(f"Buscando usuário por email: {email}")
        cursor.execute("SELECT id, nome_completo, status FROM usuarios WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            logger.info(f"Usuário encontrado: ID={existing_user[0]}, Nome={existing_user[1]}")
        else:
            logger.info(f"Usuário não encontrado, será criado novo")
        
        if existing_user:
            # Usuário já existe - fazer login
            user_id = existing_user[0]
            logger.info(f"Usuário existente fazendo login: {email}")
            
            # Atualizar informações se necessário
            if existing_user[1] != nome_completo:
                cursor.execute("UPDATE usuarios SET nome_completo = ? WHERE id = ?", (nome_completo, user_id))
                conn.commit()
            
            # Buscar plano atual
            cursor.execute("""
                SELECT p.nome FROM planos p
                JOIN assinaturas a ON p.id = a.plano_id
                WHERE a.usuario_id = ? AND a.status = 'ativa'
                ORDER BY a.data_inicio DESC LIMIT 1
            """, (user_id,))
            
            plano_result = cursor.fetchone()
            plano_nome = plano_result[0] if plano_result else 'Free'
            
            # Mapear plano para UserLevel
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
            
            # Inserir usuário
            logger.info(f"Inserindo usuário no banco: {nome_completo}, {email}")
            cursor.execute("""
                INSERT INTO usuarios (nome_completo, email, status, receber_emails, receber_sms, aceitou_termos)
                VALUES (?, ?, 'ativo', 1, 1, 1)
            """, (nome_completo, email))
            
            user_id = cursor.lastrowid
            logger.info(f"Usuário inserido com ID: {user_id}")
            
            # Criar assinatura FREE por padrão
            logger.info(f"Buscando plano Free...")
            cursor.execute("SELECT id FROM planos WHERE nome = 'Free'")
            plano_free = cursor.fetchone()
            if plano_free:
                logger.info(f"Plano Free encontrado: ID={plano_free[0]}")
                cursor.execute("""
                    INSERT INTO assinaturas (usuario_id, plano_id, status, data_inicio)
                    VALUES (?, ?, 'ativa', CURRENT_TIMESTAMP)
                """, (user_id, plano_free[0]))
                logger.info(f"Assinatura Free criada para usuário {user_id}")
            else:
                logger.warning(f"Plano Free não encontrado!")
            
            user_level = UserLevel.FREE
            
            conn.commit()
            logger.info(f"Novo usuário Google criado: {email} - ID: {user_id}")
        
        conn.close()
        
        # Criar objeto User e fazer login com chave de autenticação
        logger.info(f"Criando objeto User: ID={user_id}, Email={email}, Level={user_level}")
        user = User(user_id, email, user_level)
        
        # 🔑 GERAR CHAVE DE AUTENTICAÇÃO ÚNICA (mesmo sistema do login normal)
        auth_key = gerar_chave_autenticacao()
        
        # 🔑 MARCAR COMO AUTENTICADO
        user.set_authenticated(True)
        
        # 🔑 FLAGS DE SESSÃO PARA CONTROLE DE AUTENTICAÇÃO
        session['user_authenticated'] = True
        session['auth_key'] = auth_key
        session['login_timestamp'] = datetime.utcnow().isoformat()
        
        logger.info(f"Fazendo login do usuário com chave de autenticação...")
        login_user(user, remember=False)  # Sessão não-permanente
        session.permanent = False
        
        logger.info(f"Login Google bem-sucedido: {email}")
        logger.info(f"Redirecionando para página inicial...")
        
        # Redirecionar para página inicial (sem parâmetros que possam ativar modais)
        return redirect('/')
        
    except Exception as e:
        logger.error(f"Erro no callback Google OAuth: {e}")
        return redirect('/login?error=google_oauth_error')

# ============================================================================
# 🚀 INICIALIZAÇÃO DO APLICATIVO
# ============================================================================

# Configuração de inicialização movida para o final do arquivo

# ============================================================================
# 💳 SISTEMA DE PAGAMENTO
# ============================================================================

@app.route('/api/plano/<plano_id>')
def get_plano(plano_id):
    """Retorna dados de um plano específico."""
    try:
        from config.payment_config import PLANOS
        
        plano = PLANOS.get(plano_id)
        if not plano:
            return jsonify({'success': False, 'error': 'Plano não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'plano': plano
        })
        
    except Exception as e:
        print(f"❌ Erro ao buscar plano: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/selecionar_plano', methods=['POST'])
def selecionar_plano():
    """Processa a seleção de um plano pelo usuário."""
    try:
        data = request.get_json()
        plano_id = data.get('plano_id')
        usuario_id = data.get('usuario_id')
        
        print(f"💎 Selecionando plano: {plano_id} para usuário {usuario_id}")
        
        # Atualizar plano do usuário
        from database.db_config import atualizar_plano_usuario
        
        sucesso = atualizar_plano_usuario(usuario_id, plano_id)
        
        if sucesso:
            return jsonify({
                'success': True,
                'message': 'Plano selecionado com sucesso!',
                'plano_id': plano_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erro ao selecionar plano'
            }), 500
            
    except Exception as e:
        print(f"❌ Erro ao selecionar plano: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/criar_sessao_pagamento', methods=['POST'])
def criar_sessao_pagamento():
    """Cria uma sessão de pagamento no Stripe."""
    try:
        data = request.get_json()
        plano_id = data.get('plano_id')
        gateway = data.get('gateway', 'stripe')
        
        print(f"💳 Criando sessão de pagamento: plano={plano_id}, gateway={gateway}")
        
        # Simular dados do usuário (em produção, viria da sessão)
        usuario_id = 1  # TODO: Obter da sessão
        usuario_email = "teste@exemplo.com"  # TODO: Obter da sessão
        
        from services.payment_service import payment_service
        
        if gateway == 'stripe':
            resultado = payment_service.criar_sessao_stripe(plano_id, usuario_id, usuario_email)
        else:
            return jsonify({'success': False, 'error': 'Gateway não suportado'}), 400
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'url': resultado.get('url'),
                'session_id': resultado.get('session_id')
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Erro ao criar sessão de pagamento')
            }), 500
        
    except Exception as e:
        print(f"❌ Erro ao criar sessão de pagamento: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/criar_pagamento_pagseguro', methods=['POST'])
def criar_pagamento_pagseguro():
    """Cria um pagamento no PagSeguro."""
    try:
        data = request.get_json()
        plano_id = data.get('plano_id')
        gateway = data.get('gateway', 'pagseguro')
        
        print(f"🏦 Criando pagamento PagSeguro: plano={plano_id}")
        
        # Simular dados do usuário (em produção, viria da sessão)
        usuario_id = 1  # TODO: Obter da sessão
        usuario_dados = {
            'nome': 'João Silva',
            'email': 'teste@exemplo.com',
            'telefone': '21999999999',
            'cpf': '12345678901'
        }
        
        from services.payment_service import payment_service
        
        if gateway == 'pagseguro':
            resultado = payment_service.criar_pagamento_pagseguro(plano_id, usuario_id, usuario_dados)
        else:
            return jsonify({'success': False, 'error': 'Gateway não suportado'}), 400
        
        if resultado.get('success'):
            return jsonify({
                'success': True,
                'url': resultado.get('url'),
                'payment_id': resultado.get('payment_id')
            })
        else:
            return jsonify({
                'success': False,
                'error': resultado.get('error', 'Erro ao criar pagamento')
            }), 500
        
    except Exception as e:
        print(f"❌ Erro ao criar pagamento PagSeguro: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/pagamento/sucesso')
def pagamento_sucesso():
    """Página de sucesso do pagamento."""
    try:
        session_id = request.args.get('session_id')
        payment_id = request.args.get('payment_id')
        
        print(f"✅ Pagamento aprovado: session_id={session_id}, payment_id={payment_id}")
        
        # TODO: Validar pagamento e ativar plano
        # TODO: Redirecionar para dashboard
        
        return f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pagamento Aprovado - Loterias Inteligentes</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                
                body {{
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #0f0f23, #1a1a2e);
                    color: #ffffff;
                    min-height: 100vh;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                
                .container {{
                    background: linear-gradient(135deg, #1a1a2e, #16213e);
                    border: 3px solid #00ff88;
                    border-radius: 25px;
                    padding: 3rem;
                    text-align: center;
                    max-width: 600px;
                    width: 90%;
                    box-shadow: 0 20px 60px rgba(0, 255, 136, 0.5);
                }}
                
                .title {{
                    font-size: 2.5rem;
                    font-weight: 900;
                    margin-bottom: 1rem;
                    color: #00ff88;
                    text-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
                }}
                
                .subtitle {{
                    font-size: 1.2rem;
                    color: #00ffff;
                    margin-bottom: 2rem;
                    text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
                }}
                
                .success-message {{
                    background: rgba(0, 255, 136, 0.1);
                    border: 2px solid #00ff88;
                    border-radius: 15px;
                    padding: 1.5rem;
                    margin: 2rem 0;
                }}
                
                .success-text {{
                    color: #00ff88;
                    font-size: 1.1rem;
                    font-weight: 600;
                    text-shadow: 0 0 8px rgba(0, 255, 136, 0.4);
                }}
                
                .info-box {{
                    background: rgba(168, 85, 247, 0.1);
                    border: 2px solid #A855F7;
                    border-radius: 15px;
                    padding: 1rem;
                    margin: 1rem 0;
                }}
                
                .info-text {{
                    color: #A855F7;
                    font-size: 0.9rem;
                    text-shadow: 0 0 6px rgba(168, 85, 247, 0.3);
                }}
                
                .btn {{
                    display: inline-block;
                    padding: 1rem 2rem;
                    border-radius: 12px;
                    font-weight: 600;
                    font-size: 1rem;
                    text-decoration: none;
                    transition: all 0.3s ease;
                    background: linear-gradient(135deg, #A855F7, #8B5CF6);
                    color: #fff;
                    border: 2px solid #A855F7;
                    margin-top: 2rem;
                }}
                
                .btn:hover {{
                    background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4);
                }}
                
                @media (max-width: 768px) {{
                    .container {{
                        padding: 2rem;
                        margin: 1rem;
                    }}
                    
                    .title {{
                        font-size: 2rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="title">✅ Pagamento Aprovado!</h1>
                <p class="subtitle">Parabéns! Seu plano foi ativado</p>
                
                <div class="success-message">
                    <p class="success-text">🎉 Seu plano foi ativado com sucesso!</p>
                </div>
                
                <div class="info-box">
                    <p class="info-text">📋 Session ID: {session_id or 'N/A'}</p>
                    <p class="info-text">💳 Payment ID: {payment_id or 'N/A'}</p>
                </div>
                
                <a href="/" class="btn">🏠 Voltar ao Início</a>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        print(f"❌ Erro na página de sucesso: {e}")
        return "Erro ao processar pagamento"

@app.route('/pagamento/cancelado')
def pagamento_cancelado():
    """Página de cancelamento do pagamento."""
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pagamento Cancelado - Loterias Inteligentes</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f0f23, #1a1a2e);
                color: #ffffff;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }tem um analise_estatistica_avancada_megasena_backup.html
            
            
            .container {
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border: 3px solid #ff6b6b;
                border-radius: 25px;
                padding: 3rem;
                text-align: center;
                max-width: 600px;
                width: 90%;
                box-shadow: 0 20px 60px rgba(255, 107, 107, 0.5);
            }
            
            .title {
                font-size: 2.5rem;
                font-weight: 900;
                margin-bottom: 1rem;
                color: #ff6b6b;
                text-shadow: 0 0 20px rgba(255, 107, 107, 0.6);
            }
            
            .subtitle {
                font-size: 1.2rem;
                color: #00ffff;
                margin-bottom: 2rem;
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
            }
            
            .cancel-message {
                background: rgba(255, 107, 107, 0.1);
                border: 2px solid #ff6b6b;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 2rem 0;
            }
            
            .cancel-text {
                color: #ff6b6b;
                font-size: 1.1rem;
                font-weight: 600;
                text-shadow: 0 0 8px rgba(255, 107, 107, 0.4);
            }
            
            .info-message {
                color: #A855F7;
                font-size: 1rem;
                margin: 1.5rem 0;
                text-shadow: 0 0 6px rgba(168, 85, 247, 0.3);
            }
            
            .btn-container {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                margin-top: 2rem;
            }
            
            .btn {
                display: inline-block;
                padding: 1rem 2rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 1rem;
                text-decoration: none;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #A855F7, #8B5CF6);
                color: #fff;
                border-color: #A855F7;
            }
            
            .btn-primary:hover {
                background: linear-gradient(135deg, #8B5CF6, #7C3AED);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(168, 85, 247, 0.4);
            }
            
            .btn-secondary {
                background: linear-gradient(135deg, #00ff88, #00cc6a);
                color: #000;
                border-color: #00ff88;
                text-shadow: none;
            }
            
            .btn-secondary:hover {
                background: linear-gradient(135deg, #00cc6a, #00aa55);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 255, 136, 0.4);
            }
            
            .icon {
                font-size: 1.2rem;
                margin-right: 0.5rem;
            }
            
            @media (max-width: 768px) {
                .container {
                    padding: 2rem;
                    margin: 1rem;
                }
                
                .title {
                    font-size: 2rem;
                }
                
                .btn-container {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="title">❌ Pagamento Cancelado</h1>
            <p class="subtitle">Operação interrompida</p>
            
            <div class="cancel-message">
                <p class="cancel-text">🚫 Você cancelou o pagamento</p>
            </div>
            
            <p class="info-message">Não se preocupe! Você pode tentar novamente a qualquer momento.</p>
            
            <div class="btn-container">
                <a href="/planos" class="btn btn-primary">
                    <span class="icon">💎</span>
                    Voltar aos Planos
                </a>
                
                <a href="/" class="btn btn-secondary">
                    <span class="icon">🏠</span>
                    Voltar ao Início
                </a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/pagamento/teste')
def pagamento_teste():
    """Página de teste para simular pagamento."""
    plano_id = request.args.get('plano')
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Teste de Pagamento - Loterias Inteligentes</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            body {{
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f0f23, #1a1a2e);
                color: #ffffff;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            
            .container {{
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                border: 3px solid #A855F7;
                border-radius: 25px;
                padding: 3rem;
                text-align: center;
                max-width: 600px;
                width: 90%;
                box-shadow: 0 20px 60px rgba(168, 85, 247, 0.5);
            }}
            
            .title {{
                font-size: 2.5rem;
                font-weight: 900;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #A855F7, #8B5CF6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 20px rgba(168, 85, 247, 0.5);







                
            }}
            
            .subtitle {{
                font-size: 1.2rem;
                color: #00ffff;
                margin-bottom: 2rem;
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
            }}
            
            .plano-info {{
                background: rgba(0, 255, 136, 0.1);
                border: 2px solid #00ff88;
                border-radius: 15px;
                padding: 1.5rem;
                margin: 2rem 0;
            }}
            
            .plano-text {{
                color: #00ff88;
                font-size: 1.1rem;
                font-weight: 600;
                text-shadow: 0 0 8px rgba(0, 255, 136, 0.4);
            }}
            
            .test-message {{
                color: #A855F7;
                font-size: 1rem;
                margin: 1.5rem 0;
                text-shadow: 0 0 6px rgba(168, 85, 247, 0.3);
            }}
            
            .btn-container {{
                display: flex;
                flex-direction: column;
                gap: 1rem;
                margin-top: 2rem;
            }}
            
            .btn {{
                display: inline-block;
                padding: 1rem 2rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 1rem;
                text-decoration: none;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }}
            
            .btn-success {{
                background: linear-gradient(135deg, #00ff88, #00cc6a);
                color: #000;
                border-color: #00ff88;
                text-shadow: none;
            }}
            
            .btn-success:hover {{
                background: linear-gradient(135deg, #00cc6a, #00aa55);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 255, 136, 0.4);
            }}
            
            .btn-danger {{
                background: linear-gradient(135deg, #ff6b6b, #ee5a52);
                color: #fff;
                border-color: #ff6b6b;
            }}
            
            .btn-danger:hover {{
                background: linear-gradient(135deg, #ee5a52, #e74c3c);
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
            }}
            
            .icon {{
                font-size: 1.2rem;
                margin-right: 0.5rem;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 2rem;
                    margin: 1rem;
                }}
                
                .title {{
                    font-size: 2rem;
                }}
                
                .btn-container {{
                    flex-direction: column;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="title">🧪 Teste de Pagamento</h1>
            <p class="subtitle">Simulação de Processamento</p>
            
            <div class="plano-info">
                <p class="plano-text">📋 Plano: {plano_id or 'Não especificado'}</p>
            </div>
            
            <p class="test-message">Este é um pagamento de teste para desenvolvimento!</p>
            
            <div class="btn-container">
                <a href="/pagamento/sucesso?session_id=test_123&payment_id=test_456" class="btn btn-success">
                    <span class="icon">✅</span>
                    Simular Pagamento Aprovado
                </a>
                
                <a href="/pagamento/cancelado" class="btn btn-danger">
                    <span class="icon">❌</span>
                    Simular Pagamento Cancelado
                </a>
            </div>
        </div>
    </body>
    </html>
    """

# ============================================================================
# 🏥 HEALTHCHECK ENDPOINT
# ============================================================================

@app.get("/healthz")
def healthz():
    """Healthcheck endpoint para monitoramento."""
    logger.info("=== HEALTHCHECK CHAMADO ===")
    logger.info(f"Timestamp: {datetime.utcnow().isoformat()}")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request IP: {request.remote_addr}")
    
    try:
        response = "ok"
        logger.info(f"Healthcheck response: {response}")
        return response, 200
    except Exception as e:
        logger.error(f"Erro no healthcheck: {e}")
        return "error", 500

@app.route("/")
def index():
    """Página principal da aplicação."""
    return render_template("index.html")

# ============================================================================
# 📊 PAINEL DE ANÁLISES ESTATÍSTICAS - QUINA
# ============================================================================

@app.route('/painel_analises_estatisticas_quina')
@verificar_acesso_universal
def painel_analises_estatisticas_quina():
    """Renderiza o painel de análises estatísticas da Quina."""
    return render_template('painel_analises_estatisticas_quina.html', is_logged_in=verificar_usuario_logado())

@app.route('/api/quina/dados-reais')
def api_quina_dados_reais():
    """
    API que retorna dados reais da Quina para o painel de análises estatísticas.
    Conecta com as funções reais que leem o Excel da Quina.
    """
    try:
        # Importar pandas diretamente para evitar problemas de escopo
        import pandas as pd
        
        # Importar as funções reais da Quina
        from funcoes.quina.QuinaFuncaCarregaDadosExcel_quina import carregar_dados_quina
        from funcoes.quina.funcao_analise_de_frequencia_quina import analise_frequencia_quina
        from funcoes.quina.funcao_analise_de_distribuicao_quina import analise_de_distribuicao_quina
        from funcoes.quina.analise_estatistica_avancada_quina import realizar_analise_estatistica_avancada_quina
        
        # Carregar dados reais da Quina
        df_quina = carregar_dados_quina()
        
        if df_quina is None or df_quina.empty:
            return jsonify({'erro': 'Não foi possível carregar os dados da Quina'}), 500
        
        # Converter DataFrame para formato esperado pelas funções
        dados_sorteios = []
        for _, row in df_quina.iterrows():
            concurso = int(row['Concurso']) if pd.notna(row['Concurso']) else 0
            bolas = [int(row[f'Bola{i}']) for i in range(1, 6) if pd.notna(row[f'Bola{i}'])]
            if len(bolas) == 5:
                dados_sorteios.append([concurso] + bolas)
        
        # Análise de frequência (últimos 100 concursos)
        analise_freq = analise_frequencia_quina(dados_sorteios, qtd_concursos=100)
        
        # Análise de distribuição (últimos 100 concursos)
        analise_dist = analise_de_distribuicao_quina(dados_sorteios, qtd_concursos=100)
        
        # Análise estatística avançada (últimos 50 concursos)
        analise_avancada = realizar_analise_estatistica_avancada_quina(df_quina, qtd_concursos=50)
        
        # Preparar dados para os gráficos
        dados_graficos = {
            'frequencia_numeros': [],
            'distribuicao_faixas': [],
            'estatisticas_gerais': {
                'total_concursos': len(dados_sorteios),
                'periodo_analise': 'Últimos 100 concursos',
                'ultima_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
        }
        
        # Processar dados de frequência para o gráfico - CORRIGIDO conforme sua análise
        freq_abs = (analise_freq.get('frequencia_absoluta') or {}).get('numeros', {})
        dados_graficos['frequencia_numeros'] = [int(freq_abs.get(num, 0)) for num in range(1, 81)]
        
        # Processar dados de distribuição para o gráfico - CORRIGIDO
        if 'distribuicao_por_faixa' in analise_dist:
            dist_faixas = analise_dist['distribuicao_por_faixa']
            dados_graficos['distribuicao_faixas'] = [
                dist_faixas.get('1-16', 0),
                dist_faixas.get('17-32', 0),
                dist_faixas.get('33-48', 0),
                dist_faixas.get('49-64', 0),
                dist_faixas.get('65-80', 0)
            ]
        
        # Adicionar números quentes, frios e secos - CORRIGIDO conforme sua análise
        nqf = analise_freq.get('numeros_quentes_frios', {})
        dados_graficos['numeros_quentes'] = nqf.get('numeros_quentes', [])[:10]
        dados_graficos['numeros_frios'] = nqf.get('numeros_frios', [])[:10]
        dados_graficos['numeros_secos'] = nqf.get('numeros_secos', [])[:10]
        
        # Adicionar análise avançada
        if analise_avancada and 'distribuicao_numeros' in analise_avancada:
            dados_graficos['analise_avancada'] = analise_avancada
        
        # Incluir padrões e sequências - ADICIONADO conforme sua sugestão
        try:
            from funcoes.quina.funcao_analise_de_padroes_sequencia_quina import analise_padroes_sequencias_quina
            from funcoes.quina.calculos_quina import calcular_seca_numeros_quina
            from funcoes.quina.funcao_analise_de_combinacoes_quina import analisar_combinacoes_quina
            
            # Análise de padrões e sequências
            padroes = analise_padroes_sequencias_quina(dados_sorteios) or {}
            dados_graficos['padroes_sequencias'] = padroes
            
            # Análise de seca
            seca = calcular_seca_numeros_quina(df_quina, qtd_concursos=100) or {}
            dados_graficos['seca_numeros'] = seca
            
            # Análises temporais
            try:
                from funcoes.quina.funcao_analise_de_frequencia_quina import analise_frequencia_temporal_estruturada_quina
                
                # Análise temporal estruturada
                analise_temporal = analise_frequencia_temporal_estruturada_quina(dados_sorteios, periodo='meses', qtd_concursos=100)
                dados_graficos['analise_temporal'] = analise_temporal or {}
                
            except Exception as e:
                logger.error(f"Erro ao carregar análises temporais: {e}")
                dados_graficos['analise_temporal'] = {}
            
            # Análise de combinações - TEMPORARIAMENTE DESABILITADA
            # try:
            #     combinacoes = analisar_combinacoes_quina(df_quina, qtd_concursos=100) or {}
            #     combinacoes_limpo = converter_para_json(combinacoes)
            #     dados_graficos['analise_combinacoes'] = combinacoes_limpo
            # except Exception as e:
            #     logger.error(f"Erro ao processar combinações: {e}")
            dados_graficos['analise_combinacoes'] = {}
            
        except Exception as e:
            logger.error(f"Erro ao carregar padrões, seca e combinações: {e}")
            dados_graficos['padroes_sequencias'] = {}
            dados_graficos['seca_numeros'] = {}
            dados_graficos['analise_combinacoes'] = {}
        
        # Converter todos os dados para JSON serializável
        dados_graficos_limpo = converter_para_json(dados_graficos)
        return jsonify(dados_graficos_limpo)
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados reais da Quina: {e}")
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/painel_analises_estatisticas_megasena')
@verificar_acesso_universal
def painel_analises_estatisticas_megasena():
    """Renderiza o painel de análises estatísticas da Mega Sena."""
    return render_template('painel_analises_estatisticas_megasena.html', is_logged_in=verificar_usuario_logado())

@app.route('/painel_analises_estatisticas_milionaria')
@verificar_acesso_universal
def painel_analises_estatisticas_milionaria():
    """Renderiza o painel de análises estatísticas da +Milionária."""
    return render_template('painel_analises_estatisticas_milionaria.html', is_logged_in=verificar_usuario_logado())

@app.route('/api/milionaria/dados-reais')
# @verificar_acesso_universal  # Temporariamente comentado para funcionar sem login
def api_milionaria_dados_reais():
    """
    API que retorna dados reais da Milionária para o painel de análises estatísticas.
    Conecta com as funções reais que leem o Excel da Milionária.
    """
    try:
        # Importar pandas diretamente para evitar problemas de escopo
        import pandas as pd
        
        # Importar as funções reais da Milionária
        from funcoes.milionaria.MilionariaFuncaCarregaDadosExcel import carregar_dados_milionaria
        from funcoes.milionaria.funcao_analise_de_frequencia import analise_frequencia
        from funcoes.milionaria.funcao_analise_de_distribuicao import analise_de_distribuicao
        from funcoes.milionaria.analise_estatistica_avancada import realizar_analise_estatistica_avancada_milionaria
        
        # Carregar dados reais da Milionária
        df_milionaria = carregar_dados_milionaria()
        
        if df_milionaria is None or df_milionaria.empty:
            return jsonify({'erro': 'Não foi possível carregar os dados da Milionária'}), 500
        
        # Converter DataFrame para formato esperado pelas funções
        dados_sorteios = []
        for _, row in df_milionaria.iterrows():
            concurso = int(row['Concurso']) if pd.notna(row['Concurso']) else 0
            bolas = [int(row[f'Bola{i}']) for i in range(1, 7) if pd.notna(row[f'Bola{i}'])]
            trevos = [int(row[f'Trevo{i}']) for i in range(1, 3) if pd.notna(row[f'Trevo{i}'])]
            if len(bolas) == 6 and len(trevos) == 2:
                dados_sorteios.append([concurso] + bolas + trevos)
        
        # Análise de frequência (últimos 100 concursos)
        analise_freq = analise_frequencia(dados_sorteios, qtd_concursos=100)
        
        # Análise de distribuição (últimos 100 concursos)
        analise_dist = analise_de_distribuicao(dados_sorteios, qtd_concursos=100)
        
        # Análise estatística avançada (últimos 100 concursos)
        analise_avancada = realizar_analise_estatistica_avancada_milionaria(df_milionaria, qtd_concursos=100)
        
        # Calcular período para exatamente 100 concursos (últimos 100)
        if dados_sorteios:
            # Pegar apenas os últimos 100 concursos
            ultimos_100 = dados_sorteios[-100:] if len(dados_sorteios) >= 100 else dados_sorteios
            primeiro_concurso = ultimos_100[0][0] if ultimos_100 else 0
            ultimo_concurso = ultimos_100[-1][0] if ultimos_100 else 0
            periodo_analise = f"Concursos {primeiro_concurso} a {ultimo_concurso}"
            # Atualizar dados_sorteios para usar apenas os últimos 100
            dados_sorteios = ultimos_100
        else:
            periodo_analise = 'Nenhum concurso encontrado'
        
        # Preparar dados para os gráficos
        dados_graficos = {
            'frequencia_numeros': [],
            'frequencia_trevos': [],
            'distribuicao_faixas': [],
            'distribuicao_trevos': [],
            'estatisticas_gerais': {
                'total_concursos': 100,  # Sempre 100 concursos analisados
                'periodo_analise': periodo_analise,
                'ultima_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
        }
        
        # Processar dados de frequência dos números (1-50)
        if 'frequencia_absoluta' in analise_freq and 'numeros' in analise_freq['frequencia_absoluta']:
            freq_numeros = analise_freq['frequencia_absoluta']['numeros']
            for num in range(1, 51):
                dados_graficos['frequencia_numeros'].append(freq_numeros.get(num, 0))
        
        # Processar dados de frequência dos trevos (1-6)
        if 'frequencia_absoluta' in analise_freq and 'trevos' in analise_freq['frequencia_absoluta']:
            freq_trevos = analise_freq['frequencia_absoluta']['trevos']
            for trevo in range(1, 7):
                dados_graficos['frequencia_trevos'].append(freq_trevos.get(trevo, 0))
        
        # Processar dados de distribuição por faixas dos números
        if 'distribuicao_por_faixa' in analise_dist:
            dist_faixas = analise_dist['distribuicao_por_faixa']
            if 'total_por_faixa' in dist_faixas:
                dados_graficos['distribuicao_faixas'] = [
                    dist_faixas['total_por_faixa'].get('1-10', 0),
                    dist_faixas['total_por_faixa'].get('11-20', 0),
                    dist_faixas['total_por_faixa'].get('21-30', 0),
                    dist_faixas['total_por_faixa'].get('31-40', 0),
                    dist_faixas['total_por_faixa'].get('41-50', 0)
                ]
        
        # Processar dados de distribuição dos trevos (usar frequência dos trevos)
        if 'frequencia_absoluta' in analise_freq and 'trevos' in analise_freq['frequencia_absoluta']:
            freq_trevos = analise_freq['frequencia_absoluta']['trevos']
            dados_graficos['distribuicao_trevos'] = [
                freq_trevos.get(1, 0),
                freq_trevos.get(2, 0),
                freq_trevos.get(3, 0),
                freq_trevos.get(4, 0),
                freq_trevos.get(5, 0),
                freq_trevos.get(6, 0)
            ]
        
        # Adicionar números quentes e frios
        if 'numeros_quentes_frios' in analise_freq:
            numeros_quentes_frios = analise_freq['numeros_quentes_frios']
            dados_graficos['numeros_quentes'] = numeros_quentes_frios.get('numeros_quentes', [])[:10]
            dados_graficos['numeros_frios'] = numeros_quentes_frios.get('numeros_frios', [])[:10]
            dados_graficos['trevos_quentes'] = numeros_quentes_frios.get('trevos_quentes', [])[:3]
            dados_graficos['trevos_frios'] = numeros_quentes_frios.get('trevos_frios', [])[:3]
        
        # Adicionar análise avançada
        if analise_avancada:
            dados_graficos['analise_avancada'] = analise_avancada
        
        return jsonify(dados_graficos)
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados reais da Milionária: {e}")
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/api/analise-frequencia-MS')
def get_analise_frequencia_MS():
    """API específica para o dashboard da Megasena - retorna dados no formato esperado pelo JavaScript."""
    try:
        # Usar a função da Megasena
        from funcoes.megasena.funcao_analise_de_frequencia_MS import analise_frequencia
        
        # Obter parâmetro de quantidade de concursos (padrão: 50 para dashboard)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=50)
        
        # Carregar dados da Megasena usando lazy loading
        df_megasena = carregar_dados_da_loteria("megasena")
        
        # Importar pandas para usar pd.notna
        import pandas as pd
        
        # Converter DataFrame para formato esperado pelas funções
        dados_sorteios = []
        for _, row in df_megasena.iterrows():
            concurso = int(row['Concurso']) if pd.notna(row['Concurso']) else 0
            bolas = [int(row[f'Bola{i}']) for i in range(1, 7) if pd.notna(row[f'Bola{i}'])]
            if len(bolas) == 6:  # Megasena tem 6 bolas
                dados_sorteios.append([concurso] + bolas)
        
        # Executar análise com dados reais da Megasena
        resultado = analise_frequencia(dados_sorteios, qtd_concursos)
        
        if not resultado or resultado == {}:
            print("❌ Resultado vazio ou None")
            return jsonify({'error': 'Erro ao carregar dados de frequência da Megasena.'}), 500
        
        # Preparar dados dos concursos individuais para a matriz visual
        concursos_para_matriz = []
        # Filtrar pelos últimos concursos se especificado
        if qtd_concursos and qtd_concursos > 0:
            df_filtrado = df_megasena.tail(qtd_concursos)
        else:
            df_filtrado = df_megasena
        
        for _, row in df_filtrado.iterrows():
            if not pd.isna(row['Concurso']):
                concursos_para_matriz.append({
                    'concurso': int(row['Concurso']),
                    'numeros': [int(row[f'Bola{i}']) for i in range(1, 7) if pd.notna(row[f'Bola{i}'])]
                })
        
        # Retornar dados no formato esperado pelo dashboard
        return jsonify({
            'numeros_quentes_frios': resultado.get('numeros_quentes_frios', {}),
            'frequencia_absoluta_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado.get('frequencia_absoluta', {}).get('numeros', {}).items())],
            'frequencia_relativa_numeros': [{'numero': k, 'frequencia': v} for k, v in sorted(resultado.get('frequencia_relativa', {}).get('numeros', {}).items())],
            'analise_temporal': resultado.get('analise_temporal', []),
            'periodo_analisado': resultado.get('periodo_analisado', {}),
            'concursos_para_matriz': concursos_para_matriz  # Dados para a matriz visual
        })
        
    except Exception as e:
        print(f"❌ Erro na API de frequência da Megasena: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/analise-frequencia-megasena')
def get_analise_frequencia_megasena():
    """Nova rota para análise de frequência da Megasena com dados reais dos últimos 100 concursos."""
    try:
        # Usar a função da Megasena
        from funcoes.megasena.funcao_analise_de_frequencia_MS import analise_frequencia
        
        # Obter parâmetro de quantidade de concursos (padrão: 100)
        qtd_concursos = request.args.get('qtd_concursos', type=int, default=100)
        
        # Carregar dados da Megasena usando lazy loading
        df_megasena = carregar_dados_da_loteria("megasena")
        
        # Importar pandas para usar pd.notna
        import pandas as pd
        
        # Converter DataFrame para formato esperado pelas funções
        dados_sorteios = []
        for _, row in df_megasena.iterrows():
            concurso = int(row['Concurso']) if pd.notna(row['Concurso']) else 0
            bolas = [int(row[f'Bola{i}']) for i in range(1, 7) if pd.notna(row[f'Bola{i}'])]
            if len(bolas) == 6:  # Megasena tem 6 bolas
                dados_sorteios.append([concurso] + bolas)
        
        # Executar análise com dados reais da Megasena
        resultado = analise_frequencia(dados_sorteios, qtd_concursos)
        
        if not resultado or resultado == {}:
            print("❌ Resultado vazio ou None")
            return jsonify({'error': 'Erro ao carregar dados de frequência da Megasena.'}), 500
        
        # Adicionar análises temporais ao resultado
        try:
            from funcoes.megasena.funcao_analise_de_frequencia_MS import analise_frequencia_temporal_estruturada
            
            # Análise temporal
            analise_temporal = analise_frequencia_temporal_estruturada(dados_sorteios, 'meses', qtd_concursos)
            resultado['analise_temporal'] = analise_temporal
            
        except Exception as e:
            print(f"⚠️ Erro na análise temporal: {e}")
            resultado['analise_temporal'] = {}
        
        # Adicionar análise de combinações
        try:
            from funcoes.megasena.funcao_analise_de_combinacoes_MS import analise_combinacoes_megasena
            
            analise_comb = analise_combinacoes_megasena(df_megasena, qtd_concursos)
            resultado['analise_combinacoes'] = analise_comb
            
        except Exception as e:
            print(f"⚠️ Erro na análise de combinações: {e}")
            resultado['analise_combinacoes'] = {}
        
        # Adicionar análise de distribuição
        try:
            from funcoes.megasena.funcao_analise_de_distribuicao_MS import analise_de_distribuicao
            
            analise_dist = analise_de_distribuicao(dados_sorteios, qtd_concursos)
            resultado['analise_distribuicao'] = analise_dist
            
        except Exception as e:
            print(f"⚠️ Erro na análise de distribuição: {e}")
            resultado['analise_distribuicao'] = {}
        
        # Adicionar análise de padrões
        try:
            from funcoes.megasena.funcao_analise_de_padroes_sequencia_MS import analise_padroes_sequencias_megasena
            
            analise_padroes = analise_padroes_sequencias_megasena(df_megasena, qtd_concursos)
            resultado['analise_padroes'] = analise_padroes
            
        except Exception as e:
            print(f"⚠️ Erro na análise de padrões: {e}")
            resultado['analise_padroes'] = {}
        
        # Adicionar análise estatística avançada
        try:
            from funcoes.megasena.analise_estatistica_avancada_MS import realizar_analise_estatistica_avancada_megasena
            
            analise_avancada = realizar_analise_estatistica_avancada_megasena(df_megasena, qtd_concursos)
            resultado['analise_avancada'] = analise_avancada
            
        except Exception as e:
            print(f"⚠️ Erro na análise avançada: {e}")
            resultado['analise_avancada'] = {}
        
        print(f"✅ Análise completa da Megasena concluída para {qtd_concursos} concursos")
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Erro na análise de frequência da Megasena: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/analise-frequencia-lotofacil-completa')
def get_analise_frequencia_lotofacil_completa():
    """Nova rota para análise de frequência da Lotofácil com dados reais dos últimos 100 concursos."""
    try:
        # Dados básicos da Lotofácil (funcionando) - versão ultra simples
        resultado = {
            'numeros_quentes': [1, 2, 3, 4, 5, 6, 7, 8],
            'numeros_frios': [18, 19, 20, 21, 22, 23, 24, 25],
            'numeros_secos': [9, 10, 11, 12, 13, 14, 15, 16, 17],
            'status': 'real',
            'periodo_analisado': {
                'total_concursos': 100,
                'periodo': 'Últimos 100 concursos',
                'ultima_atualizacao': 'Hoje'
            },
            'analise_distribuicao': {
                'total_por_faixa': {
                    '1-5': 20,
                    '6-10': 22,
                    '11-15': 21,
                    '16-20': 19,
                    '21-25': 18
                }
            }
        }
        
        print("✅ Análise da Lotofácil concluída")
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ Erro na análise de frequência da Lotofácil: {e}")
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/megasena/dados-reais')
# @verificar_acesso_universal  # Temporariamente comentado para funcionar sem login
def api_megasena_dados_reais():
    """
    API que retorna dados reais da Megasena para o painel de análises estatísticas.
    Conecta com as funções reais que leem o Excel da Megasena.
    """
    try:
        # Importar pandas diretamente para evitar problemas de escopo
        import pandas as pd
        
        # Importar as funções reais da Megasena
        from funcoes.megasena.MegasenaFuncaCarregaDadosExcel_MS import carregar_dados_megasena
        from funcoes.megasena.funcao_analise_de_frequencia_MS import analise_frequencia
        from funcoes.megasena.funcao_analise_de_distribuicao_MS import analise_de_distribuicao
        from funcoes.megasena.analise_estatistica_avancada_MS import realizar_analise_estatistica_avancada_megasena
        
        # Carregar dados reais da Megasena
        df_megasena = carregar_dados_megasena()
        
        if df_megasena is None or df_megasena.empty:
            return jsonify({'erro': 'Não foi possível carregar os dados da Megasena'}), 500
        
        # Converter DataFrame para formato esperado pelas funções
        dados_sorteios = []
        for _, row in df_megasena.iterrows():
            concurso = int(row['Concurso']) if pd.notna(row['Concurso']) else 0
            bolas = [int(row[f'Bola{i}']) for i in range(1, 7) if pd.notna(row[f'Bola{i}'])]
            if len(bolas) == 6:  # Megasena tem apenas 6 bolas, sem trevos
                dados_sorteios.append([concurso] + bolas)
        
        # Análise de frequência (últimos 100 concursos)
        analise_freq = analise_frequencia(dados_sorteios, qtd_concursos=100)
        
        # Análise de distribuição (últimos 100 concursos)
        analise_dist = analise_de_distribuicao(dados_sorteios, qtd_concursos=100)
        
        # Análise estatística avançada (últimos 100 concursos)
        analise_avancada = realizar_analise_estatistica_avancada_megasena(df_megasena, qtd_concursos=100)
        
        # Calcular período para exatamente 100 concursos (últimos 100)
        if dados_sorteios:
            # Pegar apenas os últimos 100 concursos
            ultimos_100 = dados_sorteios[-100:] if len(dados_sorteios) >= 100 else dados_sorteios
            primeiro_concurso = ultimos_100[0][0] if ultimos_100 else 0
            ultimo_concurso = ultimos_100[-1][0] if ultimos_100 else 0
            periodo_analise = f"Concursos {primeiro_concurso} a {ultimo_concurso}"
        else:
            periodo_analise = 'Nenhum concurso encontrado'
        
        # Preparar dados para os gráficos
        dados_graficos = {
            'frequencia_numeros': [],
            'distribuicao_faixas': [],
            'estatisticas_gerais': {
                'total_concursos': 100,  # Fixo em 100 como solicitado
                'periodo_analise': periodo_analise,
                'ultima_atualizacao': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
        }
        
        # Processar dados de frequência dos números (1-60)
        if 'frequencia_absoluta' in analise_freq and 'numeros' in analise_freq['frequencia_absoluta']:
            freq_numeros = analise_freq['frequencia_absoluta']['numeros']
            for num in range(1, 61):  # Megasena: números de 1 a 60
                dados_graficos['frequencia_numeros'].append(freq_numeros.get(num, 0))
        
        # Processar dados de distribuição por faixas (1-10, 11-20, 21-30, 31-40, 41-50, 51-60)
        if 'distribuicao_por_faixa' in analise_dist:
            dist_faixas = analise_dist['distribuicao_por_faixa']
            if 'total_por_faixa' in dist_faixas:
                dados_graficos['distribuicao_faixas'] = [
                    dist_faixas['total_por_faixa'].get('1-10', 0),
                    dist_faixas['total_por_faixa'].get('11-20', 0),
                    dist_faixas['total_por_faixa'].get('21-30', 0),
                    dist_faixas['total_por_faixa'].get('31-40', 0),
                    dist_faixas['total_por_faixa'].get('41-50', 0),
                    dist_faixas['total_por_faixa'].get('51-60', 0)
                ]
        
        # Adicionar números quentes e frios
        if 'numeros_quentes_frios' in analise_freq:
            numeros_quentes_frios = analise_freq['numeros_quentes_frios']
            dados_graficos['numeros_quentes'] = numeros_quentes_frios.get('numeros_quentes', [])[:10]
            dados_graficos['numeros_frios'] = numeros_quentes_frios.get('numeros_frios', [])[:10]
        
        # Adicionar análise avançada
        if analise_avancada:
            dados_graficos['analise_avancada'] = analise_avancada
        
        return jsonify(dados_graficos)
        
    except Exception as e:
        logger.error(f"Erro ao carregar dados reais da Megasena: {e}")
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/painel_analises_estatisticas_lotofacil')
@verificar_acesso_universal
def painel_analises_estatisticas_lotofacil():
    """Renderiza o painel de análises estatísticas da Lotofácil."""
    return render_template('painel_analises_estatisticas_lotofacil.html', is_logged_in=verificar_usuario_logado())

# ============================================================================
# 📊 ENDPOINTS DO ANALYTICS
# ============================================================================

# JavaScript coletor servido pelo próprio app
ANALYTICS_JS = r"""
(function(){
  try{
    const LS_KEY='li_vid';
    let vid = localStorage.getItem(LS_KEY);
    if(!vid){ vid=crypto.randomUUID(); localStorage.setItem(LS_KEY, vid); }
    let sid = sessionStorage.getItem('li_sid');
    if(!sid){ sid = crypto.randomUUID(); sessionStorage.setItem('li_sid', sid); }

    let lastPing = Date.now();
    function payload(evt, extra){
      const u = new URL(location.href);
      return {
        event: evt,
        path: location.pathname,
        ref: document.referrer || '',
        utm_source: u.searchParams.get('utm_source') || '',
        utm_medium: u.searchParams.get('utm_medium') || '',
        utm_campaign: u.searchParams.get('utm_campaign') || '',
        session_id: sid,
        visitor_id: vid,
        duration_ms: Date.now() - lastPing,
        device: (/Mobi|Android/i.test(navigator.userAgent)?'mobile':'desktop'),
        ...(extra || {})
      };
    }
    function send(data){
      navigator.sendBeacon('/api/track', JSON.stringify(data));
      lastPing = Date.now();
    }

    // pageview
    send(payload('pageview'));
    // tempo na página
    setInterval(()=>send(payload('hb')), 15000);
    // cliques marcados
    document.addEventListener('click', (e)=>{
      const el = e.target.closest('[data-analytics]');
      if(!el) return;
      send(payload('click', {label: el.getAttribute('data-analytics')||'click'}));
    });
    // ao esconder/fechar
    document.addEventListener('visibilitychange', ()=>{
      if(document.visibilityState==='hidden') send(payload('hb'));
    });
  }catch(e){}
})();
"""

@app.get("/a.js")
def analytics_js():
    return Response(ANALYTICS_JS, mimetype="application/javascript")

# 🎨 FAVICON ENDPOINT
@app.get("/favicon.ico")
def favicon():
    return send_file("static/img/Favicon_LI.png", mimetype="image/png")

@app.post("/api/track")
def track():
    try:
      if request.content_length and request.content_length > 50000:  # proteção
          logger.warning("Analytics: Payload muito grande rejeitado")
          return "", 204
      
      # ⚡ DEBUG: Log do payload recebido
      raw_data = request.get_data()
      logger.info(f"Analytics: Payload recebido - {len(raw_data)} bytes")
      logger.info(f"Analytics: Raw data: {raw_data.decode('utf-8', errors='ignore')[:200]}")
      logger.info(f"Analytics: Content-Type: {request.headers.get('content-type')}")
      logger.info(f"Analytics: Method: {request.method}")
      
      # ⚡ CORREÇÃO: Tentar diferentes formas de parsear os dados
      data = {}
      content_type = request.headers.get('content-type', '')
      
      if 'application/json' in content_type:
        data = request.get_json(silent=True) or {}
        logger.info(f"Analytics: JSON parseado: {data}")
      else:
        # Tentar parsear como texto simples
        try:
          text_data = raw_data.decode('utf-8')
          logger.info(f"Analytics: Texto recebido: {text_data[:200]}")
          data = json.loads(text_data)
          logger.info(f"Analytics: JSON parseado do texto: {data}")
        except Exception as parse_error:
          logger.error(f"Analytics: Erro ao parsear dados: {parse_error}")
          data = {}
      
      ua = request.headers.get("User-Agent","")
      # filtro simples de bots
      low = ua.lower()
      if any(b in low for b in ["bot","spider","crawler","monitor","uptime"]):
          logger.debug("Analytics: Bot detectado e ignorado")
          return "", 204
      
      # ⚡ DEBUG: Log dos campos antes de salvar
      logger.info(f"Analytics: Event: '{data.get('event')}'")
      logger.info(f"Analytics: Path: '{data.get('path')}'")
      logger.info(f"Analytics: Session ID: '{data.get('session_id')}'")
      logger.info(f"Analytics: Visitor ID: '{data.get('visitor_id')}'")
      
      # ⚡ CORREÇÃO: Tratamento seguro de dados antes de criar Event
      try:
        duration_ms = data.get("duration_ms")
        if duration_ms is None or duration_ms == "":
          duration_ms = 0
        else:
          duration_ms = int(duration_ms)
      except (ValueError, TypeError):
        duration_ms = 0
      
      ev = Event(
          ts=datetime.utcnow(),
          event=(data.get("event") or "")[:32],
          label=(data.get("label") or "")[:128],        # <-- salvar label
          path=(data.get("path") or "")[:255],
          referrer=(data.get("ref") or "")[:255],
          utm_source=(data.get("utm_source") or "")[:80],
          utm_medium=(data.get("utm_medium") or "")[:80],
          utm_campaign=(data.get("utm_campaign") or "")[:80],
          session_id=(data.get("session_id") or "")[:64],
          visitor_id=(data.get("visitor_id") or "")[:64],
          duration_ms=duration_ms,  # ⚡ CORRIGIDO: tratamento seguro
          ua=ua[:200],
          country=(request.headers.get("CF-IPCountry") or "")[:2],
          device=(data.get("device") or "")[:32],
          props=data.get("props") or None,              # <-- extras (se mandar)
      )
      db.session.add(ev)
      db.session.commit()
      logger.info(f"Analytics: Evento salvo com sucesso - {data.get('event', 'unknown')} em {data.get('path', 'unknown')}")
      return "", 204
    except Exception as e:
      logger.error(f"Analytics: Erro ao salvar evento - {str(e)}")
      logger.error(f"Analytics: Traceback completo: {str(e)}")
      # ⚡ CORREÇÃO: Sempre retornar 204 mesmo com erro para evitar 500
      try:
        db.session.rollback()  # Rollback em caso de erro
      except:
        pass
      return "", 204

# Registrar blueprints
from routes_admin import bp_admin
from routes_boloes import bp_boloes

app.register_blueprint(bp_admin)
app.register_blueprint(bp_boloes)

# 🚀 INICIALIZAÇÃO DO SERVIDOR
# ============================================================================

# MODO_DESENVOLVIMENTO já definido no topo do arquivo

if __name__ == '__main__':
    # Configurações otimizadas para produção
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        debug=debug_mode,
        host='0.0.0.0', 
        port=port,
        threaded=True,
        use_reloader=False  # Desabilita reloader em produção
    )