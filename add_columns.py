# add_columns.py - Script para adicionar colunas manualmente
from app import app
from analytics_models import db
from sqlalchemy import text

def add_missing_columns():
    with app.app_context():
        try:
            # Adicionar coluna label
            db.session.execute(text("ALTER TABLE li_events ADD COLUMN label VARCHAR(128)"))
            
            # Adicionar coluna props
            db.session.execute(text("ALTER TABLE li_events ADD COLUMN props TEXT"))
            
            db.session.commit()
            print("✅ Colunas adicionadas com sucesso!")
            
            # Verificar colunas
            result = db.session.execute(text("PRAGMA table_info(li_events)"))
            print("\nColunas da tabela:")
            for row in result:
                print(f"- {row[1]} ({row[2]})")
                
        except Exception as e:
            print(f"❌ Erro ao adicionar colunas: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_missing_columns()
