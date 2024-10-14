from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse  # Certifique-se de importar HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text  
from .database import SessionLocal, engine, Base
from .routes import router as task_router  # Rota de tarefas
from .routes import router as user_router  # Nova rota para usuários
from .models import User

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurações de CORS
origins = [
    "http://127.0.0.1:5500",  # Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas do arquivo routes.py
app.include_router(task_router)  # Rotas de tarefas
app.include_router(user_router, prefix="/users")  # Rotas de usuários com prefixo "/users"

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        # Especifique a codificação ao abrir o arquivo
        with open("src/static/index.html", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return HTMLResponse(content=f"Erro ao carregar o arquivo: {str(e)}", status_code=500)

# Função de dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  
        print("Conexão com o PostgreSQL estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown_event():  
    print("Conexão com o banco de dados encerrada.")
