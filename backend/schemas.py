from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- QUESTION ŞEMALARI (GÜNCELLENDİ) ---
class QuestionBase(BaseModel):
    text: str
    question_order: int
    type: str                  # Frontend buna bakıp Input mu yoksa Buton mu çizeceğini anlayacak
    options: Optional[str] = None # Seçenek listesi (JSON String olarak gidecek)

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True

# --- PROFIL ŞEMALARI (Onboarding ve NLP Verisi) ---
# Temel profil verileri
class ProfileBase(BaseModel):
    age: int
    location: str
    hobbies: str          # Frontend "Yüzme,Kodlama" gibi string yollayacak
    favorite_genres: str
    mood_description: str # NLP için en önemli veri

# Profil oluştururken ne istiyoruz? (Base ile aynı)
class ProfileCreate(ProfileBase):
    pass

# Veritabanından okurken ne döndüreceğiz?
class Profile(ProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True # ORM nesnelerini (SQLAlchemy) okuyabilmesi için

# --- KULLANICI ŞEMALARI (Auth) ---

# Ortak veriler
class UserBase(BaseModel):
    email: EmailStr # Email formatında olup olmadığını otomatik kontrol eder
    username: str

# Kayıt olurken şifre istenir
class UserCreate(UserBase):
    password: str

# Giriş yaparken sadece email ve şifre yeterli
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Kullanıcı verisini Frontend'e GÖNDERİRKEN (Response) kullanılacak şema
# DİKKAT: Burada 'password' alanı YOK. Şifreyi gizliyoruz.
class User(UserBase):
    id: int
    is_active: bool = True
    profile: Optional[Profile] = None # Eğer profili varsa onu da göster

    class Config:
        from_attributes = True