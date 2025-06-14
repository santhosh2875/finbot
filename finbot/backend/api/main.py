# === backend/api/main.py ===
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from backend.api import auth, chatbot
from backend.db import user_db
from backend.core.config import OPENROUTER_API_KEY
from backend.api.models import Token, ChatRequest

user_db.init_db()

dummy_users = [
    ("alice", auth.hash_password("password123"), "Finance"),
    ("bob", auth.hash_password("password123"), "Marketing"),
    ("charlie", auth.hash_password("password123"), "HR"),
    ("dan", auth.hash_password("password123"), "Engineering"),
    ("eve", auth.hash_password("password123"), "C-Level"),
    ("john", auth.hash_password("password123"), "Employee"),
]
for user in dummy_users:
    user_db.add_user(*user)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_db.get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    user_id, username, hashed_password, role = user
    if not auth.verify_password(form_data.password, hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    token = auth.create_access_token({"sub": username, "role": role})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/chat")
def chat(req: ChatRequest):
    payload = auth.decode_access_token(req.token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_role = payload.get("role")
    if not user_role:
        raise HTTPException(status_code=403, detail="Role missing in token")
    result = chatbot.get_answer(req.query, user_role)
    return {
        "role": user_role,
        "query": req.query,
        "answer": result["answer"],
        "sources": result["sources"]
    }

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FinBot RBAC Chatbot",
        version="1.0.0",
        description="Chatbot with RBAC using FastAPI, OpenRouter, and ChromaDB",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
