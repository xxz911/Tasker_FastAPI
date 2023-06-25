from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Путь для БД
DB_URL = 'sqlite:///sqlite.db'

# Создаем объект для подключения к БД
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

# Настраиваем фабрику
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем базовый класс для всех моделей
Base = declarative_base()


# Функция для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создаем БД
Base.metadata.create_all(bind=engine)
