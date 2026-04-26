from fastapi import FastAPI, Request, HTTPException
import os, hmac, hashlib, json

app = FastAPI()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
BACKLOG_SECRET = os.getenv("BACKLOG_SECRET", "changeme")

try:
    import redis.asyncio as redis
    r = redis.from_url(REDIS_URL)
except Exception:
    r = None


def verify_signature(body: bytes, signature: str) -> bool:
    if not signature:
        return False
    mac = hmac.new(BACKLOG_SECRET.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    sig = request.headers.get("X-Backlog-Signature", "")
    if not verify_signature(body, sig):
        raise HTTPException(status_code=401, detail="invalid signature")
    try:
        payload = await request.json()
    except Exception:
        payload = {"raw": body.decode(errors='replace')}

    # enqueue: prefer Redis if available, fallback to local file queue
    if r is not None:
        await r.lpush("backlog:webhooks", json.dumps(payload, ensure_ascii=False))
    else:
        with open("backlog_webhook_queue.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    return {"status": "queued"}
