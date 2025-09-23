#!/usr/bin/env python3
# Script para debugar os dados de analytics

from app import app
from analytics_models import db
from sqlalchemy import text

with app.app_context():
    try:
        # Verificar dados detalhados
        result = db.session.execute(text("SELECT * FROM li_events ORDER BY ts DESC LIMIT 3"))
        print("🔍 Últimos 3 eventos detalhados:")
        print("=" * 80)
        
        for row in result:
            print(f"ID: {row[0]}")
            print(f"Timestamp: {row[1]}")
            print(f"Event: '{row[2]}'")
            print(f"Label: '{row[3]}'")
            print(f"Path: '{row[4]}'")
            print(f"Referrer: '{row[5]}'")
            print(f"Session ID: '{row[8]}'")
            print(f"Visitor ID: '{row[9]}'")
            print(f"Device: '{row[12]}'")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
