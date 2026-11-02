from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from sympy import sympify

app = FastAPI()


# 1. Ana sayfa: Doğrudan index.html dosyasını tarayıcıya yansıtır
@app.get("/", response_class=FileResponse)
def ana_sayfa():
  return "index.html"


# 2. Soruların listesi ve hatalı çözümleri (Sol taraf için veri kaynağı)
SORULAR_VERITABANI = {
    1: {
        "baslik": "1. Çok Adımlı Problemler (Kütüphane Kitap Dağıtımı)",
        "metin": (
            "Bir okul kütüphanesine 48 koli kitap gelmiştir. Her kolide 36 kitap"
            " vardır. Kitapların 675 tanesi yakın çevredeki bir köy okuluna"
            " gönderilmiştir. Kalan kitaplar 9 sınıf kitaplığına eşit sayıda"
            " yerleştirilmiştir. Her sınıf kitaplığına kaç kitap"
            " yerleştirilmiştir?"
        ),
        "hatali_cozum_adimlari": [
            "48 x 36 = 1728 (Koli x Kitap)",
            "1728 - 675 = 1053 (Kalan kitap)",
            (
                "1053 / 9 = 117 -> **İşlem Hatası Yapıldı!** (Bölme işleminde"
                " dikkat hatası var)"
            ),
        ],
        "dogru_ifade": "1053 / 9 = 117",
        "beklenen_sonuc": 117,
    },
    2: {
        "baslik": "2. Çok Adımlı Problemler (Elma Dağıtımı)",
        "metin": (
            "Bir üretici, 36 kasanın her birine 24 kg elma yerleştirmiştir. Günün"
            " ilk bölümünde 185 kg elma satılmıştır. Kalan elmalar 7 markete eşit"
            " miktarda gönderilecektir. Her markete kaç kilogram elma gönderilir?"
        ),
        "hatali_cozum_adimlari": [
            "36 x 24 = 864 (Toplam elma)",
            "864 - 185 = 679 (Kalan elma)",
            (
                "679 / 7 = 97 -> **İşlem Hatası Yapıldı!** (İşlem adımlarını"
                " kontrol et)"
            ),
        ],
        "dogru_ifade": "679 / 7 = 97",
        "beklenen_sonuc": 97,
    },
    3: {
        "baslik": "3. Karar Verme ve Karşılaştırma (Afiş Fiyatları)",
        "metin": (
            "Bir okul, şenlik afişlerini bastırmak için üç baskı merkezinden"
            " fiyat almıştır. (A: 90 TL hazırlık, 6 TL/afiş; B: 30 TL hazırlık,"
            " 7 TL/afiş; C: Hazırlık yok, 8 TL/afiş)"
        ),
        "hatali_cozum_adimlari": [
            (
                "A için: 90 + 50 * 6 = (90 + 50) * 6 = 390 TL -> **İşlem"
                " Önceliği Hatası!**"
            ),
            "B için: 30 + 50 * 7 = 380 TL",
            "C için: 50 * 8 = 400 TL",
        ],
        "dogru_ifade": "90 + 50 * 6 = 390",
        "beklenen_sonuc": 390,
    },
    6: {
        "baslik": "6. Yoğurt Kabı ve Koli Seferleri",
        "metin": (
            "Bir süt işletmesi pazartesi 2850, salı 3125 yoğurt kabı üretmiştir."
            " Kalite kontrolünde 175 kap ayrılmıştır. Kalan kaplar 25'erli"
            " kolilere yerleştirilecektir. Dağıtım aracı her seferinde en fazla"
            " 16 koli taşıyabilmektedir. Bütün kolileri taşımak için en az kaç"
            " sefer gerekir?"
        ),
        "hatali_cozum_adimlari": [
            "2850 + 3125 = 5975",
            "5975 - 175 = 5800 kap",
            "5800 / 25 = 232 koli",
            (
                "232 / 16 = 14 sefer -> **Kalan +1 Seferi Eklemeyi Unuttu!**"
            ),
        ],
        "dogru_ifade": "232 / 16 = 15",
        "beklenen_sonuc": 15,
    },
    7: {
        "baslik": "7. Bölme Sonucunu Yorumlama (Piknik Sandviç)",
        "metin": (
            "Bir okul pikniğine 328 öğrenci ve 19 görevli katılacaktır."
            " Sandviçler 18'li tepsiler hâlinde hazırlanmaktadır. Herkese bir"
            " sandviç verileceğine göre en az kaç tepsi hazırlanmalıdır?"
        ),
        "hatali_cozum_adimlari": [
            "328 + 19 = 347 kişi",
            "347 / 18 = 19 tepsi (kalan 5 sandviç)",
            "Kalanı ihmal etsin -> **Hatalı Yorumlama (Kalan için 1 tepsi eklenmeli)**",
        ],
        "dogru_ifade": "19 + 1 = 20",
        "beklenen_sonuc": 20,
    },
    8: {
        "baslik": "8. Bilim Kulübü Bütçe ve Alışveriş",
        "metin": (
            "Bir bilim kulübünün 8000 TL bütçesi vardır. Kulüp, tanesi 385 TL"
            " olan 12 deney seti ve ayrıca 740 TL tutarında malzeme satın"
            " almıştır. Kalan para ile tanesi 95 TL olan bilim kitaplarından"
            " alınacaktır. En fazla kaç kitap alınabilir?"
        ),
        "hatali_cozum_adimlari": [
            "385 x 12 = 4620 TL",
            "4620 + 740 = 5360 TL harcama",
            "8000 - 5360 = 2640 TL kalan",
            (
                "2640 / 95 = 27 kitap (kalın para 75 TL) -> Kalan parayı"
                " kitap adedi olarak düşünsün."
            ),
        ],
        "dogru_ifade": "2640 / 95 = 27",
        "beklenen_sonuc": 27,
    },
    9: {
        "baslik": "Ek Soru: Kâğıt Tasarrufu ve Ağaç Kazanımı",
        "metin": (
            "Topladığı her 1000 kg kâğıtla 17 adet yetişkin ağacı kesilmekten"
            " kurtaran bir ortaokul, 1 yılda 7000 kg atık kâğıt toplarsa kaç adet"
            " yetişkin ağacı kurtarır?"
        ),
        "hatali_cozum_adimlari": [
            (
                "7000 x 17 = 119000 -> **Kat Oranını (1000 kg) Atlayıp Doğrudan"
                " Çarptı!**"
            )
        ],
        "dogru_ifade": "7000 / 1000 * 17 = 119",
        "beklenen_sonuc": 119,
    },
    10: {
        "baslik": "Ek Soru: Dağların Yüksekliği",
        "metin": (
            "Bir bölgedeki beş dağdan dördünün yükseklikleri 1411 m, 2185 m,"
            " 1319 m ve 1277 m'dir. Toplamları 7450 m'yi geçmemektedir. 5. dağın"
            " yüksekliği en fazla kaç metre olabilir?"
        ),
        "hatali_cozum_adimlari": [
            "1411 + 2185 + 1319 + 1277 = 6192 (Hatalı Toplama İşlemi yapıldı)",
            "7450 - 6192 = 1258",
        ],
        "dogru_ifade": "7450 - 6192 = 1258",
        "beklenen_sonuc": 1258,
    },
    11: {
        "baslik": "Ek Soru: Ahmet'in Birikimi",
        "metin": (
            "2024 yılının ilk altı ayında 23300 TL, yıl sonunda toplam 38800 TL"
            " biriktiren Ahmet, yıl boyunca her ay en az 2500 TL"
            " biriktirdiğine göre kasım ayında en fazla kaç TL biriktirmiştir?"
        ),
        "hatali_cozum_adimlari": [
            "38800 - 23300 = 15500 TL (Yılın ikinci yarısı)",
            (
                "15500 / 6 = 2583 TL -> **En az 2500 TL kriteri göz ardı"
                " edildi!**"
            ),
        ],
        "dogru_ifade": "15500 - (5 * 2500) = 3000",
        "beklenen_sonuc": 3000,
    },
}


class DogrulamaIstegi(BaseModel):
  soru_id: int
  user_input: str


# 3. Soruları listelemek için API endpoint'i
@app.get("/sorular")
def sorulari_getir():
  return SORULAR_VERITABANI


# 4. Matematiksel doğrulama ve eşitlik kontrolü endpoint'i
@app.post("/dogrula")
def dogrula(veri: DogrulamaIstegi):
  try:
    girdi = veri.user_input.strip()

    # Kullanıcı `=` kullandıysa (Örn: 7450 - 6192 = 1258 veya 1053 / 9 = 117)
    if "=" in girdi:
      parcalar = girdi.split("=")
      if len(parcalar) == 2:
        sol_taraf = sympify(parcalar[0].strip())
        sag_taraf = sympify(parcalar[1].strip())

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
              f"Eşitliğin iki tarafı denk değil (Sol: {sol_deger}, Sağ:"
              f" {sag_deger})."
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