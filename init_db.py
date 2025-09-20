# init_db.py
from app import app
from analytics_models import db
with app.app_context():
    db.create_all()
print("OK: li_events criada")
