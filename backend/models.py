from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String) 
    
    # User ile Profile arasında ilişki kuruyoruz (One-to-One)
    profile = relationship("UserProfile", back_populates="owner", uselist=False)

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) 
    
    # Demografik Veriler
    age = Column(Integer)
    location = Column(String)
    
    # Anket Cevapları 
    hobbies = Column(String)          
    favorite_genres = Column(String)  
    
    # NLP Modelinin Besleneceği Veri
    mood_description = Column(String) 
    
    # NLP Tarafından Üretilen Vektör
    # SQLite'da "Liste" tipi olmadığı için vektörü JSON string olarak saklayacağız.
    # Örn: "[0.123, -0.45, 0.88 ...]"
    mood_vector = Column(String) 
    owner = relationship("User", back_populates="profile")

    # --- GÜNCELLENEN QUESTION SINIFI ---
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)       # Soru metni
    question_order = Column(Integer)
    
    # YENİ EKLENENLER:
    type = Column(String)       # "text", "select", "multi-select"
    options = Column(String)    # Seçenekler JSON String olarak: '["Koşu", "Uyku"]'