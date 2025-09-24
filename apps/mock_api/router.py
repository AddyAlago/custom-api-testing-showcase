from fastapi import APIRouter, HTTPException, status, Header
from typing import Dict, Optional
from .models import User, UserCreate, Order, OrderCreate

router = APIRouter()

USERS: Dict[int, User] = {}
ORDERS: Dict[int, Order] = {}
_user_id = 0
_order_id = 0

REQUIRED_BEARER = "secret-token"

def _auth(auth: Optional[str]):
    if auth is None or not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = auth.split(" ", 1)[1]
    if token != REQUIRED_BEARER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/users", status_code=201, response_model=User)
def create_user(body: UserCreate, authorization: Optional[str] = Header(default=None)):
    nonlocal_vars = router.__dict__.setdefault("_state", {"user_id": 0})
    _auth(authorization)
    nonlocal_vars["user_id"] += 1
    u = User(id=nonlocal_vars["user_id"], **body.model_dump())
    USERS[u.id] = u
    return u

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, authorization: Optional[str] = Header(default=None)):
    _auth(authorization)
    if user_id not in USERS:
        raise HTTPException(status_code=404)
    return USERS[user_id]

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, body: UserCreate, authorization: Optional[str] = Header(default=None)):
    _auth(authorization)
    if user_id not in USERS:
        raise HTTPException(status_code=404)
    u = User(id=user_id, **body.model_dump())
    USERS[user_id] = u
    return u

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, authorization: Optional[str] = Header(default=None)):
    _auth(authorization)
    if user_id not in USERS:
        raise HTTPException(status_code=404)
    USERS.pop(user_id)

@router.post("/orders", status_code=201, response_model=Order)
def create_order(body: OrderCreate, authorization: Optional[str] = Header(default=None)):
    nonlocal_vars = router.__dict__.setdefault("_state", {"order_id": 0, "user_id": 0})
    _auth(authorization)
    if body.user_id not in USERS:
        raise HTTPException(status_code=400, detail="user missing")
    nonlocal_vars["order_id"] += 1
    total = sum(i.qty * 9.99 for i in body.items)
    order = Order(id=nonlocal_vars["order_id"], total=total, **body.model_dump())
    ORDERS[order.id] = order
    return order

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int, authorization: Optional[str] = Header(default=None)):
    _auth(authorization)
    if order_id not in ORDERS:
        raise HTTPException(status_code=404)
    return ORDERS[order_id]

@router.get("/orders")
def list_orders(authorization: Optional[str] = Header(default=None)):
    _auth(authorization)
    return list(ORDERS.values())
