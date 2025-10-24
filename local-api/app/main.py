from __future__ import annotations
import os, time
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Header, HTTPException, Request, Response, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(title="Robust Local API", version="1.0.0")

USERS: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "Ada Lovelace", "email": "ada@example.com"},
    2: {"id": 2, "name": "Grace Hopper", "email": "grace@example.com"},
}
NEXT_USER_ID = 3

ORDERS: Dict[int, Dict[str, Any]] = {}
NEXT_ORDER_ID = 1

IDEMPOTENCY_CACHE: Dict[str, Dict[str, Any]] = {}
RATE_LOG: Dict[str, List[float]] = {}

REQUIRE_AUTH = bool(int(os.getenv("REQUIRE_AUTH", "0")))

def ensure_auth(auth_header: Optional[str]):
    if not REQUIRE_AUTH:
        return
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

class UserIn(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr

class User(BaseModel):
    id: int
    name: str
    email: str

class OrderIn(BaseModel):
    sku: str
    qty: int = Field(ge=1)

class Order(BaseModel):
    id: int
    sku: str
    qty: int

def body_fingerprint(data: Dict[str, Any]) -> str:
    try:
        import json
        return json.dumps(data, sort_keys=True, separators=(",", ":"))
    except Exception:
        return str(data)

def client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "local"

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@app.get("/users", response_model=List[User])
def list_users(authorization: Optional[str] = Header(default=None)) -> List[User]:
    ensure_auth(authorization)
    return list(USERS.values())

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, authorization: Optional[str] = Header(default=None)) -> User:
    ensure_auth(authorization)
    u = USERS.get(user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u

@app.post("/users", status_code=201, response_model=User)
def create_user(payload: UserIn, authorization: Optional[str] = Header(default=None)) -> User:
    global NEXT_USER_ID
    ensure_auth(authorization)
    uid = NEXT_USER_ID
    NEXT_USER_ID += 1
    user = {"id": uid, **payload.model_dump()}
    USERS[uid] = user
    return user

@app.post("/orders", status_code=201, response_model=Order)
def create_order(
    payload: OrderIn,
    request: Request,
    response: Response,
    authorization: Optional[str] = Header(default=None),
    idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
    xidempotency_key: Optional[str] = Header(default=None, alias="x-idempotency-key"),
) -> Order:
    global NEXT_ORDER_ID
    ensure_auth(authorization)
    key = idempotency_key or xidempotency_key
    if key:
        fp = body_fingerprint(payload.model_dump())
        cached = IDEMPOTENCY_CACHE.get(key)
        if cached:
            if cached["fingerprint"] == fp:
                return cached["order"]
            raise HTTPException(status_code=409, detail="Idempotency key reuse with different payload")
        oid = NEXT_ORDER_ID
        NEXT_ORDER_ID += 1
        order = {"id": oid, **payload.model_dump()}
        ORDERS[oid] = order
        IDEMPOTENCY_CACHE[key] = {"order": order, "fingerprint": fp}
        return order
    oid = NEXT_ORDER_ID
    NEXT_ORDER_ID += 1
    order = {"id": oid, **payload.model_dump()}
    ORDERS[oid] = order
    return order

@app.get("/ratelimit")
def ratelimited_endpoint(request: Request):
    limit = int(os.getenv("RATE_LIMIT_PER_MIN", "30"))
    window = 60.0
    now = time.time()
    ip = client_ip(request)
    timestamps = RATE_LOG.setdefault(ip, [])
    RATE_LOG[ip] = [t for t in timestamps if now - t < window]
    timestamps = RATE_LOG[ip]
    if len(timestamps) >= limit:
        retry_after = int(window - (now - timestamps[0])) if timestamps else 60
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests"},
            headers={"Retry-After": str(max(retry_after, 1))},
        )
    timestamps.append(now)
    return {"ok": True, "remaining": max(limit - len(timestamps), 0)}

@app.get("/")
def root():
    return {"message": "Robust Local API", "docs": "/docs"}
