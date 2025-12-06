from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json # Vektör listesini stringe çevirmek için lazım

# Kendi yazdığımız modülleri içeri alıyoruz
import models, schemas, crud
import ai_service 
from database import SessionLocal, engine

# 1. VERİTABANI OLUŞTURMA (Sihirli Satır)
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# --- DEPENDENCY (Bağımlılık Enjeksiyonu) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- BAŞLANGIÇTA SORULARI EKLEME (SEEDING) ---
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    # Eğer tabloda hiç soru yoksa, varsayılanları ekle
    if db.query(models.Question).count() == 0:
        print("📥 Veritabanı boş, varsayılan sorular ekleniyor...")
        
# 1. Aktivite Sorusu (GÜNCELLENDİ)
        q1 = models.Question(
            question_order=1, 
            text="Genelde ne yaparken müzik dinliyorsun?",  # <--- Burayı değiştirdik
            type="multi-select", 
            options=json.dumps(["Kod Yazarken 💻", "Spor Yaparken 🏃", "Ders Çalışırken 📚", "Uzanırken 😴", "Yolda / Seyahatte 🚌"])
        )
        
        # 2. Müzik Zevki Sorusu
        q2 = models.Question(
            question_order=2,
            text="Hangi türleri seversin?",
            type="multi-select",
            options=json.dumps(["Rock", "Pop", "Rap", "Klasik", "Electronic", "Jazz", "Indie"])
        )

        # 3. Ruh Hali Sorusu
        q3 = models.Question(
            question_order=3,
            text="Peki modun nasıl? Bize biraz hislerinden bahset.",
            type="text", 
            options=None 
        )

        db.add_all([q1, q2, q3])
        db.commit()
        print("✅ Sorular başarıyla eklendi!")
    
    db.close()

# --- YENİ EKLENECEK API: SORULARI GETİR ---
@app.get("/content/questions", response_model=List[schemas.Question])
def get_questions(db: Session = Depends(get_db)):
    """Frontend'in ekrana çizeceği soruları buradan çekiyoruz"""
    return db.query(models.Question).order_by(models.Question.question_order).all()

# --- DEPENDENCY (Bağımlılık Enjeksiyonu) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API ENDPOINTLERİ ---

@app.get("/")
def home():
    return {"message": "Sistem Aktif! /docs adresine giderek test et."}

# 1. KAYIT OL (Register)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Önce email var mı diye kontrol et
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı.")
    
    # Yoksa kaydet
    return crud.create_user(db=db, user=user)

# 2. PROFİL OLUŞTUR / ANKET CEVAPLA (GÜNCELLENEN KISIM)
@app.post("/users/{user_id}/profile/", response_model=schemas.Profile)
def create_profile_for_user(
    user_id: int, 
    profile: schemas.ProfileCreate, 
    db: Session = Depends(get_db)
):
    # A. NLP Analizi Yap: Metni 384 boyutlu vektöre çevir
    # Örnek Çıktı: [0.12, -0.55, 0.98, ...]
    vector_list = ai_service.get_mood_vector(profile.mood_description)
    
    # B. Formatla: Listeyi veritabanında saklanabilir JSON String'e çevir
    # Örnek Çıktı: "[0.12, -0.55, 0.98, ...]" (Tırnak içinde yazı oldu)
    vector_json_str = json.dumps(vector_list)
    
    # C. Konsola Bilgi Ver (İşlem başarılı mı görelim)
    print(f"🤖 NLP Vektörü Oluştu. Boyut: {len(vector_list)}")

    # D. Veritabanına Kaydet (Vektör stringini de gönderiyoruz)
    # NOT: crud.py dosyasındaki fonksiyonun bu parametreyi alacak şekilde güncellenmiş olması lazım!
    return crud.create_user_profile(
        db=db, 
        profile=profile, 
        user_id=user_id,
        mood_vector_json=vector_json_str 
    )

# 3. KULLANICI DETAYINI GETİR
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return db_user