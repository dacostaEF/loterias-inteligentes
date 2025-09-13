from app import app

@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200
