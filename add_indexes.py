# add_indexes.py - Script para adicionar índices de performance
from app import app
from analytics_models import db
from sqlalchemy import text

def add_performance_indexes():
    with app.app_context():
        try:
            # Índice composto para top_events (label + ts)
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_events_label_ts 
                ON li_events (label, ts) 
                WHERE label IS NOT NULL AND label != ''
            """))
            
            # Índice para funnel queries (event + label + ts)
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_events_event_label_ts 
                ON li_events (event, label, ts)
            """))
            
            # Índice para realtime (session_id + ts)
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_events_session_ts 
                ON li_events (session_id, ts)
            """))
            
            # Índice para device analysis
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_events_device_ts 
                ON li_events (device, ts)
            """))
            
            db.session.commit()
            print("✅ Índices de performance adicionados com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao adicionar índices: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_performance_indexes()
