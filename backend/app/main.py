# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.controllers.brief_controller import router as brief_router

app = FastAPI(
    title="IA Brief Generator",
    description="Générateur de briefs professionnels via DeepSeek",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l’API IA Brief Generator ✨"}

# (optionnel) CORS pour permettre au frontend (React/HTML/JS) d'accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Inclusion du contrôleur des briefs
app.include_router(brief_router)
