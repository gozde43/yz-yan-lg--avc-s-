from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sympy as sp
import os

app = FastAPI()

class MathInput(BaseModel):
    denklem: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    # index.html dosyasını okuyup tarayıcıya arayüz olarak gönderiyoruz
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>index.html dosyası bulunamadı! Lütfen GitHub'a yüklediğinizden emin olun.</h1>"

@app.post("/dogrula")
def denklem_dogrula(veri: MathInput):
    try:
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