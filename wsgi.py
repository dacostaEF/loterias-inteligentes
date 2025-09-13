from app import app

@app.get("/healthz")
def healthz():
    """Healthcheck super simples para Railway."""
    return "ok", 200
