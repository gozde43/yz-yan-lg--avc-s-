from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from sympy import sympify

app = FastAPI()


# 1. Ana sayfa: Doğrudan index.html dosyasını tarayıcıya yansıtır
@app.get("/", response_class=FileResponse)
def ana_sayfa():
  return "index.html"


class DogrulamaIstegi(BaseModel):
  user_input: str


# 2. Matematiksel doğrulama ve eşitlik kontrolü endpoint'i
@app.post("/dogrula")
def dogrula(veri: DogrulamaIstegi):
  try:
    girdi = veri.user_input.strip()

    # Kullanıcı `=` kullandıysa (Örn: 7450 - 6192 = 1258)
    if "=" in girdi:
      parcalar = girdi.split("=")
      if len(parcalar) == 2:
        sol_taraf = sympify(parcalar[0].strip())
        sag_taraf = sympify(parcalar[1].strip())

        # Sol ve sağ tarafın sayısal değerlerini karşılaştır
        sol_deger = float(sol_taraf)
        sag_deger = float(sag_taraf)

        if abs(sol_deger - sag_deger) < 1e-6:
          return {
              "success": True,
              "islem_sonucu": sol_deger,
              "mesaj": "Tebrikler, eşitlik doğru!",
          }
        else:
          raise ValueError(
              "Eşitliğin her iki tarafı birbirine denk değil (sol taraf:"
              f" {sol_deger}, sağ taraf: {sag_deger})."
          )
      else:
        raise ValueError("Geçersiz eşitlik formatı.")
    else:
      # Eşittir yoksa direkt ifadeyi çöz
      islem_sonucu = float(sympify(girdi))
      return {
          "success": True,
          "islem_sonucu": islem_sonucu,
          "mesaj": "İfade başarıyla doğrulandı!",
      }

  except Exception as e:
    raise HTTPException(
        status_code=400,
        detail=(
            f"Matematiksel ifade okunamadı. İşlem işaretlerini kontrol et! "
            f"(Detay: {str(e)})"
        ),
    )