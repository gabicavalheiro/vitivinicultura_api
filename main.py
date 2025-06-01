from datetime import timedelta
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from scraping import producao, processamento, comercializacao, importacao, exportacao
from auth import (
    Token, User, UserCreate, authenticate_user, create_access_token,
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db,
    get_password_hash
)

load_dotenv()

app = FastAPI(
    title="API Vitivinicultura Embrapa",
    description="""
    API para coleta e análise de dados do setor vitivinícola brasileiro.
    Fonte: Embrapa Uva e Vinho.
    
    Fornece dados estruturados para:
    * Produção de uvas
    * Processamento
    * Comercialização
    * Importação
    * Exportação
    
    Ideal para análises de mercado e projetos de Machine Learning.
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": user.scopes, "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username já existe")
    
    db_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": get_password_hash(user.password),
        "disabled": False,
        "is_active": True,
        "scopes": ["read:data"]
    }
    fake_users_db[user.username] = db_user
    return User(**db_user)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
def root():
    return {
        "mensagem": "API pública de vitivinicultura da Embrapa",
        "documentacao": "/docs",
        "endpoints_disponiveis": [
            "/producao",
            "/processamento",
            "/comercializacao",
            "/importacao",
            "/exportacao"
        ]
    }

@app.get("/producao")
def get_producao(current_user: User = Depends(get_current_active_user)):
    """Retorna dados históricos de produção de uvas."""
    return producao.get_data()

@app.get("/processamento")
def get_processamento(current_user: User = Depends(get_current_active_user)):
    """Retorna dados de processamento de uvas."""
    return processamento.get_data()

@app.get("/comercializacao")
def get_comercializacao(current_user: User = Depends(get_current_active_user)):
    """Retorna dados de comercialização de produtos vitivinícolas."""
    return comercializacao.get_data()

@app.get("/importacao")
def get_importacao(current_user: User = Depends(get_current_active_user)):
    """Retorna dados de importação de produtos vitivinícolas."""
    return importacao.get_data()

@app.get("/exportacao")
def get_exportacao(current_user: User = Depends(get_current_active_user)):
    """Retorna dados de exportação de produtos vitivinícolas."""
    return exportacao.get_data()


