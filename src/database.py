from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

# Configuração do Redis
REDIS_URL = "redis://localhost:6379/0"
redis_client = redis.Redis.from_url(REDIS_URL)

# Configuração do banco de dados PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:lycas21@localhost/todo_db" 

# Criação do engine
engine = create_engine(DATABASE_URL)

# Testar a conexão com o banco de dados
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Conexão com o PostgreSQL estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")

# Criação da sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()
