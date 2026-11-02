from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sympy import sympify

app = FastAPI()


@app.get("/", response_class=FileResponse)
def ana_sayfa():
  return "index.html"


SORULAR_VERITABANI = {
    1: {
        "baslik": "1. Soru: Kütüphane Kitap Dağıtımı",
        "metin": (
            "Bir okul kütüphanesine 48 koli kitap gelmiştir. Her kolide 36 kitap"
            " vardır. Kitapların 675 tanesi yakın çevredeki bir köy okuluna"
            " gönderilmiştir. Kalan kitaplar 9 sınıf kitaplığına eşit sayıda"
            " yerleştirilmiştir. Her sınıf kitaplığına kaç kitap"
            " yerleştirilmiştir?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 48 x 36 = 1728 (Toplam kitap)",
            "2. Adım: 1728 - 675 = 1053 (Kalan kitap)",
            "3. Adım: 1053 / 9 = 117 (Her sınıfa düşen)",
        ],
        "ipucu": (
            "3. adımdaki 1053 / 9 bölme işlemini tekrar kağıt üzerinde"
            " yapmayı dene! 10'un içinde 9 bir kere var, kalan 1..."
        ),
        "dogru_ifade": "1053 / 9 = 117",
        "beklenen_sonuc": 117,
    },
    2: {
        "baslik": "2. Soru: Elma Dağıtımı",
        "metin": (
            "Bir üretici, 36 kasanın her birine 24 kg elma yerleştirmiştir. Günün"
            " ilk bölümünde 185 kg elma satılmıştır. Kalan elmalar 7 markete eşit"
            " miktarda gönderilecektir. Her markete kaç kilogram elma gönderilir?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 36 x 24 = 864 kg elma",
            "2. Adım: 864 - 185 = 679 kg kalan",
            "3. Adım: 679 / 7 = 97 kg market başı",
        ],
        "ipucu": (
            "679'u 7'ye bölerken yüzler ve onlar basamağındaki bölme işlemlerini"
            " kontrol et!"
        ),
        "dogru_ifade": "679 / 7 = 97",
        "beklenen_sonuc": 97,
    },
    3: {
        "baslik": "3. Soru: Afiş Fiyatları Karşılaştırma",
        "metin": (
            "Bir okul, şenlik afişlerini bastırmak için üç baskı merkezinden"
            " fiyat almıştır. (A: 90 TL hazırlık, 6 TL/afiş; B: 30 TL hazırlık,"
            " 7 TL/afiş; C: Hazırlık yok, 8 TL/afiş). 50 afiş için A firmasının"
            " tutarını hesaplayalım."
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: Toplam Fiyat = Hazırlık + Afiş sayısı x Birim Fiyat",
            "2. Adım: A firması için = 90 + 50 x 6",
            "3. Adım: (90 + 50) x 6 = 140 x 6 = 390 TL",
        ],
        "ipucu": (
            "Toplama ve çarpma yan yana olduğunda hangisi önce yapılır? İşlem"
            " önceliğine dikkat et!"
        ),
        "dogru_ifade": "90 + 50 * 6 = 390",
        "beklenen_sonuc": 390,
    },
    6: {
        "baslik": "4. Soru: Yoğurt Kabı Taşıma",
        "metin": (
            "Bir süt işletmesi pazartesi 2850, salı 3125 yoğurt kabı üretmiştir."
            " Kalite kontrolünde 175 kap ayrılmıştır. Kalan kaplar 25'erli"
            " kolilere yerleştirilecektir. Dağıtım aracı her seferinde en fazla"
            " 16 koli taşıyabilmektedir. Bütün kolileri taşımak için en az kaç"
            " sefer gerekir?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 2850 + 3125 = 5975 kap",
            "2. Adım: 5975 - 175 = 5800 kap kalır",
            "3. Adım: 5800 / 25 = 232 koli",
            "4. Adım: 232 / 16 = 14 sefer gerekir.",
        ],
        "ipucu": (
            "232'yi 16'ya böldüğünde bir kalan artıyor mu? Kalan kolileri"
            " taşımak için +1 sefer gerekebilir mi?"
        ),
        "dogru_ifade": "232 / 16 = 15",
        "beklenen_sonuc": 15,
    },
    7: {
        "baslik": "5. Soru: Piknik Sandviç Tepsileri",
        "metin": (
            "Bir okul pikniğine 328 öğrenci ve 19 görevli katılacaktır."
            " Sandviçler 18'li tepsiler hâlinde hazırlanmaktadır. Herkese bir"
            " sandviç verileceğine göre en az kaç tepsi hazırlanmalıdır?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 328 + 19 = 347 toplam kişi",
            "2. Adım: 347 / 18 = 19 tepsi (ve 5 kişi artıyor)",
            "3. Adım: 19 tepsi yeterlidir.",
        ],
        "ipucu": (
            "Arta kalan 5 kişi sandviçsiz mi kalacak? Onlar için ekstra 1 tepsi"
            " daha açmak gerekmez mi?"
        ),
        "dogru_ifade": "19 + 1 = 20",
        "beklenen_sonuc": 20,
    },
    8: {
        "baslik": "6. Soru: Bilim Kulübü Kitap Alımı",
        "metin": (
            "Bir bilim kulübünün 8000 TL bütçesi vardır. Tanesi 385 TL olan 12"
            " deney seti ve 740 TL tutarında malzeme alınmıştır. Kalan para"
            " ile tanesi 95 TL olan kitaplardan en fazla kaç tane alınabilir?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 385 x 12 = 4620 TL (Deney setleri)",
            "2. Adım: 4620 + 740 = 5360 TL toplam harcama",
            "3. Adım: 8000 - 5360 = 2640 TL kalan para",
            "4. Adım: 2640 / 95 = 27 kitap (75 TL artar)",
            "5. Adım: Sonuç olarak 27 kitap alınır.",
        ],
        "ipucu": (
            "Kalan parayı böldüğümüzde artan 75 TL ile 1 kitap daha alınabilir"
            " mi, yoksa yetersiz mi kalır?"
        ),
        "dogru_ifade": "2640 / 95 = 27",
        "beklenen_sonuc": 27,
    },
    9: {
        "baslik": "7. Soru: Atık Kâğıt ve Ağaç Kurtarma",
        "metin": (
            "Topladığı her 1000 kg kâğıtla 17 adet yetişkin ağacı kesilmekten"
            " kurtaran bir ortaokul, 1 yılda 7000 kg atık kâğıt toplarsa kaç adet"
            " yetişkin ağacı kurtarır?"
        ),
        "yapay_zeka_cozumu": ["1. Adım: 7000 x 17 = 119000 adet ağaç kurtarılır."],
        "ipucu": (
            "7000 kg içinde kaç tane '1000 kg' var? Önce kat oranını bulmak"
            " için bölme yapmalısın!"
        ),
        "dogru_ifade": "7000 / 1000 * 17 = 119",
        "beklenen_sonuc": 119,
    },
    10: {
        "baslik": "8. Soru: Dağların Yüksekliği",
        "metin": (
            "Bir bölgedeki beş dağdan dördünün yükseklikleri 1411 m, 2185 m,"
            " 1319 m ve 1277 m'dir. Toplamları 7450 m'yi geçmemektedir. 5. dağın"
            " yüksekliği en fazla kaç metre olabilir?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 1411 + 2185 + 1319 + 1277 = 6192 m",
            "2. Adım: 7450 - 6192 = 1258 m",
        ],
        "ipucu": (
            "1. adımdaki dört dağın yüksekliğini tekrar topla. Eldeleri eklemeyi"
            " unutmş olabilir mi?"
        ),
        "dogru_ifade": "7450 - 6192 = 1258",
        "beklenen_sonuc": 1258,
    },
    11: {
        "baslik": "9. Soru: Ahmet'in Birikimi",
        "metin": (
            "2024 yılının ilk altı ayında 23300 TL, yıl sonunda toplam 38800 TL"
            " biriktiren Ahmet, yıl boyunca her ay en az 2500 TL"
            " biriktirdiğine göre kasım ayında en fazla kaç TL biriktirmiştir?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 38800 - 23300 = 15500 TL (Son 6 ay toplamı)",
            "2. Adım: 15500 / 6 = 2583 TL biriktirmiştir.",
        ],
        "ipucu": (
            "Kasım ayının 'en fazla' olması için diğer 5 ayın 'en az' (yani 2500"
            " TL) olması gerekir!"
        ),
        "dogru_ifade": "15500 - (5 * 2500) = 3000",
        "beklenen_sonuc": 3000,
    },
}


class DogrulamaIstegi(BaseModel):
  soru_id: int
  user_input: str


@app.get("/sorular")
def sorulari_getir():
  return SORULAR_VERITABANI


@app.post("/dogrula")
def dogrula(veri: DogrulamaIstegi):
  try:
    soru = SORULAR_VERITABANI.get(veri.soru_id)
    if not soru:
      raise HTTPException(status_code=444, detail="Soru bulunamadı.")

    girdi = veri.user_input.strip()

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
              "mesaj": (
                  "Tebrikler! Hatanı yakaladın ve doğru eşitliği yazdın."
              ),
          }
        else:
          return {
              "success": False,
              "mesaj": (
                  "Eşitliğin iki tarafı birbiriyle eşleşmiyor. Tekrar dene!"
              ),
              "ipucu": soru["ipucu"],
          }
      else:
        raise ValueError("Geçersiz eşitlik.")
    else:
      islem_sonucu = float(sympify(girdi))
      if abs(islem_sonucu - soru["beklenen_sonuc"]) < 1e-6:
        return {
            "success": True,
            "islem_sonucu": islem_sonucu,
            "mesaj": "Tebrikler! Doğru sonuca ulaştın.",
        }
      else:
        return {
            "success": False,
            "mesaj": "Bulduğun sonuç hatalı. Tekrar dene!",
            "ipucu": soru["ipucu"],
        }

  except Exception as e:
    raise HTTPException(
        status_code=400,
        detail=(
            "Matematiksel ifade okunamadı. Lütfen işlem işaretlerini kontrol"
            " et!"
        ),
    )