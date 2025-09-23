#!/usr/bin/env python3
# Script para verificar se a tabela de analytics existe

from app import app
from analytics_models import db
from sqlalchemy import text

with app.app_context():
    try:
        # Verificar se a tabela existe
        result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='li_events'"))
        table_exists = result.fetchone() is not None
        print(f"✅ Tabela li_events existe: {table_exists}")
        
        if table_exists:
            # Contar registros
            count_result = db.session.execute(text("SELECT COUNT(*) FROM li_events"))
            count = count_result.fetchone()[0]
            print(f"📊 Total de eventos registrados: {count}")
            
            # Mostrar últimos 5 eventos
            if count > 0:
                recent_result = db.session.execute(text("SELECT event, path, ts FROM li_events ORDER BY ts DESC LIMIT 5"))
                print("\n🔍 Últimos 5 eventos:")
                for row in recent_result:
                    print(f"  - {row[0]} em {row[1]} às {row[2]}")
            else:
                print("⚠️  Nenhum evento registrado ainda")
        else:
            print("❌ Tabela não existe - precisa ser criada")
            
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {e}")
