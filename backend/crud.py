from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models, schemas

# Şifreleme ayarları (Bcrypt kullanıyoruz)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- YARDIMCI FONKSİYONLAR (Hashleme) ---

def get_password_hash(password):
    """Normal şifreyi alır, okunamaz hale (hash) getirir."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Girilen şifre ile veritabanındaki hash aynı mı diye bakar."""
    return pwd_context.verify(plain_password, hashed_password)

# --- VERİTABANI İŞLEMLERİ (CRUD) ---

# 1. Kullanıcı Bul (Email ile)
def get_user_by_email(db: Session, email: str):
    # SQL karşılığı: SELECT * FROM users WHERE email = '...'
    return db.query(models.User).filter(models.User.email == email).first()

# 2. Yeni Kullanıcı Oluştur (Create)
def create_user(db: Session, user: schemas.UserCreate):
    # Şifreyi hashle
    hashed_password = get_password_hash(user.password)
    
    # Model objesini hazırla
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password # Hashlenmiş halini kaydediyoruz!
    )
    
    # Veritabanına ekle
    db.add(db_user)
    db.commit()      # İşlemi onayla (Save)
    db.refresh(db_user) # ID'si oluşmuş halini geri al
    return db_user

# 3. Profil Oluştur (Onboarding Cevapları)
def create_user_profile(db: Session, profile: schemas.ProfileCreate, user_id: int, mood_vector_json: str):
    # Gelen veriyi (ProfileCreate şeması) veritabanı modeline (UserProfile) çevir
    # **profile.dict() -> Python sözlüğünü modele döker (Kısayol)
    db_profile = models.UserProfile(**profile.dict(), user_id=user_id, mood_vector=mood_vector_json)
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# 4. Profil Getir (Eşleştirme/Öneri için lazım olacak)
def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()