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
            "1. Adım: 48 x 36 = 1728 koli toplam kitap",
            "2. Adım: 1728 - 675 = 1053 kitap kaldı",
            "3. Adım: 1053 / 9 = 113 kitap düşer",
        ],
        "hatali_adim_no": 3,
        "ipucu": (
            "3. adımdaki bölme işleminde 1053'ü 9'a bölerken kalanı ve basamak"
            " hesaplamasını tekrar kontrol et."
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
            "3. Adım: 679 / 7 = 93 kg düşer",
        ],
        "hatali_adim_no": 3,
        "ipucu": (
            "679'u 7'ye bölerken bölme işlemini adım adım yeniden yapmalısın."
        ),
        "dogru_ifade": "679 / 7 = 97",
        "beklenen_sonuc": 97,
    },
    3: {
        "baslik": "3. Soru: Afiş Fiyatları Karşılaştırma",
        "metin": """
        Bir okul, şenlik afişlerini bastırmak için üç baskı merkezinden fiyat almıştır:
        <br><br>
        <table style="width:100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 10px; background-color: white;">
            <thead>
                <tr style="background-color: #e8f0fe; color: #1a73e8; border-bottom: 2px solid #aecbfa;">
                    <th style="padding: 8px; border: 1px solid #dadce0; text-align: center;">Baskı Merkezi</th>
                    <th style="padding: 8px; border: 1px solid #dadce0; text-align: center;">Hazırlık Ücreti</th>
                    <th style="padding: 8px; border: 1px solid #dadce0; text-align: center;">Bir Afişin Fiyatı</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center; font-weight: bold;">A</td>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center;">90 TL</td>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center;">6 TL</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center; font-weight: bold;">B</td>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center;">30 TL</td>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center;">7 TL</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center; font-weight: bold;">C</td>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center;">Yok</td>
                    <td style="padding: 8px; border: 1px solid #dadce0; text-align: center;">8 TL</td>
                </tr>
            </tbody>
        </table>
        <b>Soru:</b> 50 afiş için A firmasının ödeyeceği tutarı hesaplayalım.
        """,
        "yapay_zeka_cozumu": [
            "1. Adım: Tutar = Hazırlık Ücreti + Afiş Sayısı x Birim Fiyat",
            "2. Adım: 90 + 50 = 140 buldum",
            "3. Adım: 140 x 6 = 840 TL ödenir",
        ],
        "hatali_adim_no": 3,
        "ipucu": (
            "Matematikte işlem önceliği vardır; toplama ve çarpma bir arada"
            " olduğunda önce hangisi yapılır?"
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
            "2. Adım: 5975 - 175 = 5800 kap",
            "3. Adım: 5800 / 25 = 232 koli",
            "4. Adım: 232 / 16 = 14 seferde taşınır",
        ],
        "hatali_adim_no": 4,
        "ipucu": (
            "232 koliyi 16'lı gruplara böldüğünde arta kalan koliler için bir"
            " sefer daha eklenmeli mi?"
        ),
        "dogru_ifade": "232 / 16 = 15",
        "beklenen_sonuc": 15,
    },
    7: {
        "baslik": "5. Soru: Piknik Sandviç Tepsileri",
        "metin": (
            "Bir okul pikniğine 328 öğrenci ve 19 görevli katılacaktır."
            " Sandviçler en fazla 18'li tepsiler hâlinde taşınmaktadır. Herkese"
            " bir sandviç verileceğine göre en az kaç tepsi hazırlanmalıdır?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 328 + 19 = 347 kişi",
            "2. Adım: 347 / 18 = 19 tepsi yeterlidir",
        ],
        "hatali_adim_no": 2,
        "ipucu": (
            "Bölme işleminde arta kalan kişileri açıkta bırakmamak için ne"
            " yapmalıyız?"
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
            "1. Adım: 385 x 12 = 4620 TL",
            "2. Adım: 4620 + 740 = 5360 TL",
            "3. Adım: 8000 - 5360 = 2640 TL kalan",
            (
                "4. Adım: 2640 / 95 = 27 (kalan 75 TL'yi de eklersek 27 + 75 = 102"
                " kitap)"
            ),
        ],
        "hatali_adim_no": 4,
        "ipucu": (
            "Bölme işleminde kalan 75 TL paradır, kitap adedi değildir! Doğru"
            " kitap sayısını bulmak için 2640'ı 95'e bölüp kalanı atlamalısın."
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
        "yapay_zeka_cozumu": ["1. Adım: 7000 x 17 = 119000 ağaç kurtarılır"],
        "hatali_adim_no": 1,
        "ipucu": (
            "7000 kg içinde 7 tane 1000 kg vardır. Oranı bulduktan sonra 7 kat"
            " sayısı ile 17'yi çarpmalısın! (Örn: 7 * 17 = 119)"
        ),
        "dogru_ifade": "7 * 17 = 119",
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
            "1. Adım: 1411 + 2185 + 1319 + 1277 = 6150 m",
            "2. Adım: 7450 - 6150 = 1300 m",
        ],
        "hatali_adim_no": 1,
        "ipucu": "1. adımda dört dağın boyunu toplarken hata yapılmış. Toplam 6150 değil, 6192 olmalıdır.",
        "dogru_ifade": "1411 + 2185 + 1319 + 1277 = 6192",
        "beklenen_sonuc": 6192,
    },
    11: {
        "baslik": "9. Soru: Ahmet'in Birikimi",
        "metin": (
            "2024 yılının ilk altı ayında 23300 TL, yıl sonunda toplam 38800 TL"
            " biriktiren Ahmet, yıl boyunca her ay en az 2500 TL"
            " biriktirdiğine göre kasım ayında en fazla kaç TL biriktirmiştir?"
        ),
        "yapay_zeka_cozumu": [
            "1. Adım: 38800 - 23300 = 15500 TL",
            "2. Adım: 15500 / 6 = 2583 TL biriktirmiştir",
        ],
        "hatali_adim_no": 2,
        "ipucu": (
            "Diğer ayların en az 2500 TL olma şartını dikkate alarak hesapla."
        ),
        "dogru_ifade": "15500 - (5 * 2500) = 3000",
        "beklenen_sonuc": 3000,
    },
}


class DogrulamaIstegi(BaseModel):
  soru_id: int
  secilen_adim: int  # Öğrencinin seçtiği hatalı adım numarası (0 = Hata Yok)
  user_input: str


@app.get("/sorular")
def sorulari_getir():
  return SORULAR_VERITABANI


@app.post("/dogrula")
def dogrula(veri: DogrulamaIstegi):
  try:
    soru = SORULAR_VERITABANI.get(veri.soru_id)
    if not soru:
      raise HTTPException(status_code=404, detail="Soru bulunamadı.")

    # 1. Kontrol: Hatalı adım seçimi doğru mu?
    dogru_adim = soru.get("hatali_adim_no")
    if veri.secilen_adim != dogru_adim:
      return {
          "success": False,
          "mesaj": (
              "Seçtiğin hatalı adım numarası yanlış. Yapay zekanın nerede hata"
              " yaptığını tekrar incele!"
          ),
          "ipucu": soru["ipucu"],
      }

    girdi = veri.user_input.strip()

    # 2. Kontrol: İşlem eşittir (=) içermeli
    if "=" not in girdi:
      return {
          "success": False,
          "mesaj": (
              "Lütfen düzeltmeyi sadece sonuç olarak değil, eşittir (=)"
              " kullanarak tam bir işlem şeklinde yaz!"
          ),
          "ipucu": soru["ipucu"],
      }

    parcalar = girdi.split("=")
    if len(parcalar) == 2:
      sol_taraf_str = parcalar[0].strip()
      sag_taraf_str = parcalar[1].strip()

      sol_deger = float(sympify(sol_taraf_str))
      sag_deger = float(sympify(sag_taraf_str))

      beklenen = soru["beklenen_sonuc"]

      # Normal eşitlik VEYA kalanlı bölmelerde bölüm kontrolü (Örn: 2640/95 = 27)
      if (
          abs(sol_deger - sag_deger) < 1e-6
          and abs(sag_deger - beklenen) < 1e-6
      ) or (
          abs(sag_deger - beklenen) < 1e-6
          and sol_deger >= sag_deger
          and sol_deger < sag_deger + 1
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
            "mesaj": (
                "Yazdığın işlem doğru sonuca ulaşmıyor veya eşitliğin iki"
                " tarafı uyuşmuyor. Kontrol et!"
            ),
            "ipucu": soru["ipucu"],
        }
    else:
      raise ValueError("Geçersiz eşitlik formatı.")

  except Exception as e:
    raise HTTPException(
        status_code=400,
        detail=(
            "Matematiksel ifade okunamadı. Lütfen `=` işaretini ve işlem"
            " formatını kontrol et!"
        ),
    )