from fastapi import FastAPI, Body, Header, HTTPException, Response
from pydantic import BaseModel, EmailStr
from typing import Optional, Any, Dict, List
from time import time

app = FastAPI(title="Custom API Testing Showcase")

# -----------------------
# In-memory data stores
# -----------------------
USERS: Dict[int, Dict[str, Any]] = {}
ORDERS: Dict[int, Dict[str, Any]] = {}
NEXT_USER_ID = 1
NEXT_ORDER_ID = 1

# Idempotency store: key -> order_id
IDEMPOTENCY_KEYS: Dict[str, int] = {}

# Rate limiting (very simple, in-memory)
RATE_LIMIT = 10              # showcase default
RATE_WINDOW_SEC = 60
_rate_counts = 0
_rate_window_start = time()

# -----------------------
# Models
# -----------------------
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

# -----------------------
# Health & Root
# -----------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    # Intentionally minimal - some scanners expect 200 here, but we target /docs in CI
    return {"message": "Custom API Testing Showcase"}

# -----------------------
# Users
# -----------------------
@app.post("/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    global NEXT_USER_ID
    # normalize email
    normalized_email = user.email.strip().lower()
    new = {"id": NEXT_USER_ID, "name": user.name, "email": normalized_email}
    USERS[NEXT_USER_ID] = new
    NEXT_USER_ID += 1
    return new

@app.get("/users", response_model=List[User])
def list_users(page: int = 1, size: int = 10):
    # deterministic order by id (ascending) for pagination monotonicity
    records = [USERS[k] for k in sorted(USERS.keys())]
    if page < 1 or size < 1:
        return []
    start = (page - 1) * size
    end = start + size
    return records[start:end]

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return USERS[user_id]

# -----------------------
# Orders with Idempotency
# -----------------------
@app.post("/orders", status_code=201)
def create_order(
    body: Dict[str, Any] = Body(...),
    idemp: Optional[str] = Header(None, convert_underscores=False, alias="Idempotency-Key"),
    xidemp: Optional[str] = Header(None, convert_underscores=False, alias="x-idempotency-key"),
):
    """
    Accept ANY JSON body; implement idempotency via either 'Idempotency-Key' or 'x-idempotency-key'.
    Return same order id for a repeated key.
    """
    global NEXT_ORDER_ID
    key = idemp or xidemp
    if key:
        if key in IDEMPOTENCY_KEYS:
            order_id = IDEMPOTENCY_KEYS[key]
            return {"id": order_id, **body}

    order_id = NEXT_ORDER_ID
    ORDERS[order_id] = {"id": order_id, **body}
    NEXT_ORDER_ID += 1

    if key:
        IDEMPOTENCY_KEYS[key] = order_id

    return ORDERS[order_id]

# -----------------------
# Rate limiting
# -----------------------
@app.get("/ratelimit/info")
def ratelimit_info():
    return {"limit": RATE_LIMIT, "window_seconds": RATE_WINDOW_SEC}

@app.get("/ratelimit")
def ratelimit(resp: Response):
    """
    Very basic global rate limit: allow RATE_LIMIT per RATE_WINDOW_SEC,
    then return 429 with Retry-After until window resets.
    """
    global _rate_counts, _rate_window_start
    now = time()
    if now - _rate_window_start > RATE_WINDOW_SEC:
        _rate_window_start = now
        _rate_counts = 0

    _rate_counts += 1
    if _rate_counts > RATE_LIMIT:
        # IMPORTANT: put the header in the exception, not on resp
        raise HTTPException(
            status_code=429,
            detail="Too Many Requests",
            headers={"Retry-After": "5"}  # value must be a string
        )

    return {"ok": True, "count_in_window": _rate_counts}
