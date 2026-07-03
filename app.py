from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

API_KEY = "ak_gvb4gtg6k10167a1r4gya9br"
EMAIL = "23f3000908@study.iitm.ac.in"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class RequestBody(BaseModel):
    events: List[Event]

@app.post("/analytics")
def analytics(body: RequestBody, x_api_key: str = Header(None)):
    print("Received API key:", repr(x_api_key))

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


    total_events = len(body.events)

    unique_users = len(set(e.user for e in body.events))

    revenue = 0

    user_totals = {}

    for e in body.events:
        if e.amount > 0:
            revenue += e.amount
            user_totals[e.user] = user_totals.get(e.user, 0) + e.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }

@app.get("/")
def root():
    return {"status":"ok"}