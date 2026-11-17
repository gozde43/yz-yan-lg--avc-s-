import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sympy import sympify

app = FastAPI()

JSON_DOSYASI = "sorular.json"


def soruları_yukle():
  if os.path.exists(JSON_DOSYASI):
    with open(JSON_DOSYASI, "r", encoding="utf-8") as f:
      return json.load(f)
  return {}


@app.get("/", response_class=FileResponse)
def ana_sayfa():
  return "index.html"


@app.get("/sorular")
def sorulari_getir():
  return soruları_yukle()


class DogrulamaIstegi(BaseModel):
  soru_id: int
  secilen_adim: int
  islem_girdisi: str
  sonuc_girdisi: str


@app.post("/dogrula")
def dogrula(veri: DogrulamaIstegi):
  try:
    sorular = soruları_yukle()
    soru = sorular.get(str(veri.soru_id))
    if not soru:
      raise HTTPException(status_code=404, detail="Soru bulunamadı.")

    dogru_adim = soru.get("hatali_adim_no")

    # 1. Adım Kontrolü
    if veri.secilen_adim != dogru_adim:
      return {
          "success": False,
          "hata_turu": "Adim Secim Hatasi",
          "mesaj": (
              "Seçtiğin adım numarası yanlış. Yapay zekanın nerede hata"
              " yaptığını tekrar incele!"
          ),
          "ipucu": soru["ipucu"],
      }

    islem_str = veri.islem_girdisi.strip()
    sonuc_str = veri.sonuc_girdisi.strip()

    if not islem_str or not sonuc_str:
      return {
          "success": False,
          "hata_turu": "Eksik Girdi",
          "mesaj": "Lütfen hem işlem kutusunu hem de sonuç kutusunu doldur!",
          "ipucu": soru["ipucu"],
      }

    sol_deger = float(sympify(islem_str))
    sag_deger = float(sympify(sonuc_str))
    beklenen = soru["beklenen_sonuc"]

    # Matematiksel Doğruluk Kontrolü
    if (
        abs(sol_deger - sag_deger) < 1e-6
        and abs(sag_deger - beklenen) < 1e-6
    ) or (
        abs(sag_deger - beklenen) < 1e-6
        and (
            abs(sol_deger - sag_deger) < 1e-6
            or (sol_deger >= sag_deger and sol_deger < sag_deger + 1)
        )
    ):
      return {
          "success": True,
          "mesaj": (
              "Tebrikler! Hem hatalı adımı doğru seçtin hem de işlemi"
              " mükemmel düzelttin."
          ),
      }
    else:
      return {
          "success": False,
          "hata_turu": "İşlem / Hesaplama Hatasi",
          "mesaj": (
              "Yazdığın işlemin sonucu ile sonuç kutusundaki değer uyuşmuyor"
              " veya doğru sonuca ulaşmıyor. Kontrol et!"
          ),
          "ipucu": soru["ipucu"],
      }

  except Exception as e:
    raise HTTPException(
        status_code=400,
        detail=(
            "Matematiksel ifade okunamadı. Lütfen rakam ve işlem"
            " işaretlerini kontrol et!"
        ),
    )