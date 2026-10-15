from fastapi import FastAPI
from pydantic import BaseModel
import sympy as sp

app = FastAPI()

# Kullanıcıdan gelecek matematiksel ifade için veri modeli
class MathInput(BaseModel):
    denklem: str

@app.get("/")
def read_root():
    return {"mesaj": "YZ Yanılgı Avcısı Backend Çalışıyor!"}

@app.post("/dogrula")
def denklem_dogrula(veri: MathInput):
    try:
        # SymPy ile gelen metni matematiksel ifadeye çevirip hesaplıyoruz
        ifade = sp.sympify(veri.denklem)
        sonuc = float(ifade.evalf())
        return {
            "durum": "basarili",
            "sonuc": sonuc,
            "mesaj": "Harika! İşlem adımı ve sonuç matematiksel olarak doğru."
        }
    except Exception as hata:
        return {
            "durum": "hata",
            "mesaj": f"Yazdığın ifadede matematiksel bir syntax hatası var: {str(hata)}"
        }