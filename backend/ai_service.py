from sentence_transformers import SentenceTransformer

# Model tek bir kez yüklenir (Global Değişken)
# 'all-MiniLM-L6-v2' modeli hem hızlıdır hem de semantic (anlamsal) ilişkileri çok iyi kurar.
print("🧠 NLP Modeli (BERT) yükleniyor... (İlk seferde indirme yapabilir)")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model hazır!")

def get_mood_vector(text: str):
    """
    Gelen metni alır (örn: "Canım sıkkın"),
    BERT modelinden geçirir ve 384 boyutlu bir liste (vektör) döner.
    """
    # encode() normalde numpy array döner, veritabanı/JSON için list'e çeviriyoruz.
    embedding = model.encode(text).tolist()
    return embedding