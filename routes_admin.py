# routes_admin.py
from flask import Blueprint, jsonify, render_template_string, request
from sqlalchemy import func, desc, inspect
from datetime import datetime, timedelta
from analytics_models import db, Event
import os

bp_admin = Blueprint("admin", __name__, url_prefix="/admin/analytics")

# proteção simples por key (?key=...)
@bp_admin.before_request
def guard():
    KEY = os.getenv("ADMIN_KEY")
    if KEY and request.args.get("key") != KEY:
        return "unauthorized", 401

# 🔍 DIAGNÓSTICO INSTANTÂNEO
@bp_admin.get("/_diag")
def diag():
    out = {}
    try:
        insp = inspect(db.engine)
        out["db_url_ok"] = True
        out["has_table_li_events"] = insp.has_table("li_events")
        out["events_count"] = (db.session.query(func.count(Event.id)).scalar()
                               if out["has_table_li_events"] else None)
        return jsonify(out)
    except Exception as e:
        out["db_url_ok"] = False
        out["error"] = str(e)
        return jsonify(out), 500

@bp_admin.get("/kpis")
def kpis():
    try:
        since = datetime.utcnow() - timedelta(days=1)
        pv = db.session.query(func.count(Event.id)).filter(Event.ts>=since, Event.event=='pageview').scalar() or 0
        vis = db.session.query(func.count(func.distinct(Event.visitor_id))).filter(Event.ts>=since).scalar() or 0
        ses = db.session.query(func.count(func.distinct(Event.session_id))).filter(Event.ts>=since).scalar() or 0
        total_ms = db.session.query(func.coalesce(func.sum(Event.duration_ms),0)).filter(Event.ts>=since, Event.event=='hb').scalar() or 0
        avg = round((total_ms/1000)/max(pv,1), 1)
        return jsonify({"pageviews_24h": pv, "visitors_24h": vis, "sessions_24h": ses, "avg_time_per_view_s": avg})
    except Exception as e:
        from flask import current_app
        current_app.logger.exception("KPIS ERROR")
        return jsonify({"error":"kpis_failed","detail":str(e)}), 500

@bp_admin.get("/top-pages")
def top_pages():
    try:
        since = datetime.utcnow() - timedelta(days=7)
        rows = (db.session.query(Event.path, func.count(Event.id).label("pv"))
                .filter(Event.ts>=since, Event.event=='pageview')
                .group_by(Event.path).order_by(desc("pv")).limit(20).all())
        return jsonify([{"path": p, "pageviews": int(pv)} for p, pv in rows])
    except Exception as e:
        from flask import current_app
        current_app.logger.exception("TOP-PAGES ERROR")
        return jsonify([])  # Retorna array vazio para não quebrar o front

@bp_admin.get("/daily")
def daily():
    try:
        days = int(request.args.get('days') or 14)
        since = datetime.utcnow() - timedelta(days=days)
        date_expr = func.date(Event.ts)
        rows = (db.session.query(date_expr.label('d'), func.count(Event.id))
                .filter(Event.ts>=since, Event.event=='pageview')
                .group_by('d').order_by('d').all())
        labels = [str(d) for d,_ in rows]
        pv = [int(c) for _,c in rows]
        return jsonify({"labels": labels, "pageviews": pv})
    except Exception as e:
        from flask import current_app
        current_app.logger.exception("DAILY ERROR")
        return jsonify({"labels": [], "pageviews": []})  # Retorna estrutura consistente

@bp_admin.get("/top-events")
def top_events():
    since = datetime.utcnow() - timedelta(days=7)
    rows = (db.session.query(Event.label, func.count(Event.id).label("c"))
            .filter(Event.ts>=since, Event.event=='click', Event.label.isnot(None), Event.label!='')
            .group_by(Event.label).order_by(desc("c")).limit(30).all())
    return jsonify([{"label": lbl, "count": int(c)} for lbl, c in rows])

@bp_admin.get("/realtime")
def realtime():
    since = datetime.utcnow() - timedelta(seconds=60)
    sessions = (db.session.query(func.count(func.distinct(Event.session_id)))
                .filter(Event.ts>=since).scalar()) or 0
    return jsonify({"online": int(sessions)})

@bp_admin.get("/funnel-premium")
def funnel_premium():
    since = datetime.utcnow() - timedelta(days=7)
    pv = db.session.query(func.count(Event.id)).filter(Event.ts>=since, Event.event=='pageview').scalar() or 0
    modais = db.session.query(func.count(Event.id)).filter(
        Event.ts>=since, Event.event=='click',
        Event.label.like('li:%:painel:abrir_modal_%')
    ).scalar() or 0
    palpites = db.session.query(func.count(Event.id)).filter(
        Event.ts>=since, Event.event=='click',
        Event.label=='li:quina:premium:gerar_palpite'
    ).scalar() or 0
    ctas = db.session.query(func.count(Event.id)).filter(
        Event.ts>=since, Event.event=='click',
        Event.label=='li:home:cta:assinar_premium'
    ).scalar() or 0
    return jsonify({"pageviews": pv, "modais": modais, "palpites": palpites, "cta_premium": ctas})

@bp_admin.get("/")
def dashboard():
    return render_template_string("""
<!doctype html><html lang="pt-br"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Analytics — Loterias Inteligentes</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body{background:#0b1220;color:#e5e7eb}
  main{max-width:1100px;margin:32px auto}
  .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  .card{padding:16px;border-radius:12px;background:#0f172a}
  canvas{max-height:320px}
</style></head><body>
<main>
  <h2>Analytics — Loterias Inteligentes</h2>
  <div class="cards">
    <div class="card"><h5>Pageviews (24h)</h5><p id="pv">…</p></div>
    <div class="card"><h5>Visitantes (24h)</h5><p id="vis">…</p></div>
    <div class="card"><h5>Sessões (24h)</h5><p id="ses">…</p></div>
  </div>
  <article class="card" style="margin-top:16px">
    <h5>Tempo médio por visualização (s) — 24h</h5><p id="avg">…</p>
  </article>
  <article class="card" style="margin-top:16px">
    <h5>Top páginas (7 dias)</h5><canvas id="topPages"></canvas>
  </article>
  <article class="card" style="margin-top:16px">
    <h5>Série diária de pageviews (14 dias)</h5><canvas id="dailyPv"></canvas>
  </article>
  <article class="card" style="margin-top:16px">
    <h5>Top Eventos (7 dias)</h5><canvas id="topEvents"></canvas>
  </article>
  <article class="card" style="margin-top:16px">
    <h5>Funil Premium (7 dias)</h5><canvas id="funnelPremium"></canvas>
  </article>
  <article class="card" style="margin-top:16px">
    <h5>Usuários Online Agora</h5><p id="onlineNow">...</p>
  </article>
</main>
<script>
async function load(){
  const k = await fetch('kpis' + location.search).then(r=>r.json());
  pv.textContent=k.pageviews_24h; vis.textContent=k.visitors_24h; ses.textContent=k.sessions_24h; avg.textContent=k.avg_time_per_view_s;

  const topRes = await fetch('top-pages' + location.search);
  if (!topRes.ok) {
    console.error('HTTP error', topRes.status);
    return;
  }
  let topData;
  try { topData = await topRes.json(); } catch { topData = []; }
  const top = Array.isArray(topData) ? topData : [];
  if (!Array.isArray(top)) {
    console.error('Payload inesperado:', topData);
    return;
  }
  new Chart(document.getElementById('topPages'), {
    type:'bar',
    data:{labels: top.map(t=>t.path), datasets:[{label:'Pageviews', data: top.map(t=>t.pageviews)}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}}}
  });

  const daily = await fetch('daily?days=14' + (location.search?('&'+location.search.slice(1)):'')).then(r=>r.json());
  new Chart(document.getElementById('dailyPv'), {
    type:'line',
    data:{labels: daily.labels, datasets:[{label:'Pageviews', data: daily.pageviews, fill:false, tension:.2}]},
    options:{responsive:true,maintainAspectRatio:false}
  });

  // Top Eventos
  const events = await fetch('top-events' + location.search).then(r=>r.json());
  new Chart(document.getElementById('topEvents'), {
    type:'bar',
    data:{labels: events.map(e=>e.label), datasets:[{label:'Cliques', data: events.map(e=>e.count)}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}}}
  });

  // Funil Premium
  const funnel = await fetch('funnel-premium' + location.search).then(r=>r.json());
  new Chart(document.getElementById('funnelPremium'), {
    type:'bar',
    data:{labels:['Pageviews','Modais','Palpites','CTA Premium'], datasets:[{label:'Conversão', data:[funnel.pageviews,funnel.modais,funnel.palpites,funnel.cta_premium]}]},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}}}
  });

  // Online Agora
  const online = await fetch('realtime' + location.search).then(r=>r.json());
  onlineNow.textContent = online.online + ' usuários online';
}
load();
</script>
</body></html>
    """)
