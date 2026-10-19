from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sympy as sp
import os
import re

app = FastAPI()

class MathInput(BaseModel):
    denklem: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>index.html dosyası bulunamadı!</h1>"

@app.post("/dogrula")
def denklem_dogrula(veri: MathInput):
    try:
        # Kullanıcının yazdığı 'x' veya 'X' harflerini otomatik olarak '*' (çarpma) işaretine çevirelim
        islenmis_metin = veri.denklem.replace('x', '*').replace('X', '*')
        
        # SymPy ile matematiksel ifadeye çevirip hesaplıyoruz
        ifade = sp.sympify(islenmis_metin)
        sonuc = float(ifade.evalf())
        return {
            "durum": "basarili",
            "sonuc": sonuc,
            "mesaj": "Harika! İşlem adımı ve sonuç matematiksel olarak doğru."
        }
    except Exception as hata:
        return {
            "durum": "hata",
            "mesaj": f"Yazdığın ifadede matematiksel bir hata var. İşlem işaretlerini kontrol et! (Detay: {str(hata)})"
        }