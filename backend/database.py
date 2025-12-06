from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite veritabanı dosyası backend klasöründe "muzik_app.db" adıyla oluşacak
SQLALCHEMY_DATABASE_URL = "sqlite:///./muzik_app.db"

# Veritabanı motorunu (engine) oluşturuyoruz
# connect_args={"check_same_thread": False} sadece SQLite için gereklidir
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Veritabanı oturumu (Session) oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modellerimizin (Tabloların) miras alacağı temel sınıf
Base = declarative_base()