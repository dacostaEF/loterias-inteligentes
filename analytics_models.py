# analytics_models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON as SQLITE_JSON
try:
    from sqlalchemy.dialects.postgresql import JSONB
    JSONType = JSONB
except Exception:
    JSONType = SQLITE_JSON  # cai no JSON do SQLite

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = "li_events"
    id          = db.Column(db.Integer, primary_key=True)
    ts          = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    event       = db.Column(db.String(32), index=True)   # 'pageview','click','hb'
    label       = db.Column(db.String(128), index=True)  # <-- NOVO (nome do clique)
    path        = db.Column(db.String(255), index=True)
    referrer    = db.Column(db.String(255))
    utm_source  = db.Column(db.String(80))
    utm_medium  = db.Column(db.String(80))
    utm_campaign= db.Column(db.String(80))
    session_id  = db.Column(db.String(64), index=True)
    visitor_id  = db.Column(db.String(64), index=True)
    duration_ms = db.Column(db.Integer)
    ua          = db.Column(db.String(200))
    country     = db.Column(db.String(2))
    device      = db.Column(db.String(32))
    props       = db.Column(JSONType)                    # <-- OPCIONAL: extras em JSON (SQLite/Postgres)
