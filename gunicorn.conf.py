# Configuração do Gunicorn para produção
import os

# Configurações básicas
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = int(os.environ.get('WEB_CONCURRENCY', 2))
threads = int(os.environ.get('WEB_THREADS', 4))
timeout = int(os.environ.get('WEB_TIMEOUT', 120))
keepalive = 2

# Configurações de performance
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Configurações de logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Configurações de segurança
forwarded_allow_ips = '*'
secure_scheme_headers = {'X-FORWARDED-PROTO': 'https'}
