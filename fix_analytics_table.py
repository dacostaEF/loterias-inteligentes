#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para forçar a criação da tabela li_events
"""

import os
import sys
from flask import Flask
from analytics_models import db, Event

# Configurar Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///li.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar banco
db.init_app(app)

print("🔧 FORÇANDO CRIAÇÃO DA TABELA li_events...")

with app.app_context():
    try:
        # Verificar se a tabela existe
        inspector = db.inspect(db.engine)
        has_table = inspector.has_table("li_events")
        print(f"📊 Tabela li_events existe: {has_table}")
        
        if not has_table:
            print("🔨 Criando tabela li_events...")
            db.create_all()
            print("✅ Tabela criada com sucesso!")
        else:
            print("✅ Tabela já existe!")
            
        # Verificar novamente
        inspector = db.inspect(db.engine)
        has_table = inspector.has_table("li_events")
        print(f"📊 Tabela li_events existe após criação: {has_table}")
        
        # Contar eventos
        count = db.session.query(db.func.count(Event.id)).scalar()
        print(f"📈 Total de eventos: {count}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

print("🎯 Script concluído!")
