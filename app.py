from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sympy import sympify

app = FastAPI()

# Statik dosyalar veya ana sayfa yapısı varsayımıyla...


class DogrulamaIstegi(BaseModel):
  user_input: str
  expected_value: (
      float  # Veya beklenen değerin türü (örneğin öğrencinin bulması gereken doğru sonuç)
  )


@app.post("/dogrula")
def dogrula(veri: DogrulamaIstegi):
  try:
    girdi = veri.user_input.strip()

    # Kullanıcı `=` kullandıysa (Örn: 7450 - 6192 = 1258)
    if "=" in girdi:
      parcalar = girdi.split("=")
      if len(parcalar) == 2:
        from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def ana_sayfa():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Hata Avcısı</title></head>
    <body>
        <h1>Hata Avcısı Eğitim Aracı Çalışıyor!</h1>
    </body>
    </html>
    """sol_taraf = sympify(parcalar[0].strip())
        sag_taraf = sympify(parcalar[1].strip())
        # Hem sol tarafın kendi içinde tutarlı olup olmadığını
        # hem de genel sonucun doğru olup olmadığını kontrol edebiliriz:
        islem_sonucu = float(sol_taraf)
        girilen_sonuc = float(sag_taraf)
      else:
        raise ValueError("Geçersiz eşitlik formatı.")
    else:
      # Eşittir yoksa direkt ifadeyi değerlendir
      islem_sonucu = float(sympify(girdi))
      girilen_sonuc = islem_sonucu

    return {
        "success": True,
        "islem_sonucu": islem_sonucu,
        "mesaj": "Tebrikler, ifade doğru!",
    }

  except Exception as e:
    raise HTTPException(
        status_code=400,
        detail=(
            f"Matematiksel ifade okunamadı. İşlem işaretlerini kontrol et! "
            f"(Detay: {str(e)})"
        ),
    )