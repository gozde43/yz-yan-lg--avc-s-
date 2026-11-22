from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel
from typing import List, Optional
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import json
import os
import csv
import io
import re
import html
from datetime import datetime

app = FastAPI(title="Hata Avcısı - Eleştirel YZ Matematik Platformu")

ALLOWED_STATIC_FILES = {"style.css", "script.js"}
DATA_DIR = "veriler"
os.makedirs(DATA_DIR, exist_ok=True)


def load_sorular() -> dict:
    if not os.path.exists("sorular.json"):
        raise HTTPException(status_code=404, detail="sorular.json dosyası bulunamadı")
    with open("sorular.json", "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_math_expr(expr_str: str) -> str:
    s = expr_str.strip()
    if "=" in s:
        s = s.split("=")[0].strip()
    s = s.replace(",", ".")
    s = s.replace("×", "*").replace("x", "*").replace("X", "*").replace("·", "*")
    s = s.replace("÷", "/").replace(":", "/")
    if not re.match(r"^[0-9+\-*/().\s]+$", s):
        raise ValueError("Geçersiz karakter tespit edildi.")
    return s


def evaluate_math_expr(expr_str: str) -> float:
    cleaned = normalize_math_expr(expr_str)
    transformations = standard_transformations + (implicit_multiplication_application,)
    parsed = parse_expr(cleaned, transformations=transformations)
    return float(parsed.evalf())


class DogrulamaIstegi(BaseModel):
    katilimci_id: str
    soru_id: str
    secilen_adim: int  # 0 = "Hata Yok", 1..N = Adım numarası
    yazilan_islem: str
    yazilan_sonuc: Optional[str] = ""
    gecen_sure: int
    deneme_sayisi: int
    kullanilan_ipucu_seviyesi: int = 0


class IpucuIstegi(BaseModel):
    soru_id: str
    seviye: int = 1


class CevabiGosterIstegi(BaseModel):
    soru_id: str


@app.get("/")
def read_root():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"error": "index.html bulunamadı"}


@app.get("/static/{file_path:path}")
def serve_safe_static(file_path: str):
    filename = os.path.basename(file_path)
    if filename not in ALLOWED_STATIC_FILES:
        raise HTTPException(status_code=403, detail="Bu dosyaya erişim izni yok.")
    if os.path.exists(os.path.join("static", filename)):
        return FileResponse(os.path.join("static", filename))
    if os.path.exists(filename):
        return FileResponse(filename)
    raise HTTPException(status_code=404, detail="Statik dosya bulunamadı.")


@app.get("/api/sorular")
def get_sorular():
    raw_data = load_sorular()
    safe_data = {}
    for q_id, item in raw_data.items():
        safe_data[q_id] = {
            "baslik": item["baslik"],
            "metin": item["metin"],
            "gorsel_tipi": item.get("gorsel_tipi", ""),
            "yapay_zeka_cozumu": item["yapay_zeka_cozumu"],
            "bolme_gorseli": item.get("bolme_gorseli", None),
            "toplam_ipucu": len(item.get("ipuclari", []))
        }
    return JSONResponse(content=safe_data)


@app.post("/api/ipucu")
def get_ipucu(istek: IpucuIstegi):
    sorular = load_sorular()
    if istek.soru_id not in sorular:
        raise HTTPException(status_code=404, detail="Soru bulunamadı")
    soru = sorular[istek.soru_id]
    ipuclari = soru.get("ipuclari", [])
    if not ipuclari:
        return {"seviye": 0, "toplam_seviye": 0, "ipucu_metni": ""}
    idx = max(0, min(istek.seviye - 1, len(ipuclari) - 1))
    return {
        "seviye": idx + 1,
        "toplam_seviye": len(ipuclari),
        "ipucu_metni": ipuclari[idx]
    }


@app.post("/api/cevabi-goster")
def cevabi_goster(istek: CevabiGosterIstegi):
    sorular = load_sorular()
    if istek.soru_id not in sorular:
        raise HTTPException(status_code=404, detail="Soru bulunamadı")
    soru = sorular[istek.soru_id]
    dogru_adim = int(soru["hatali_adim_no"])
    beklenen_islem = soru["beklenen_islem"]
    beklenen_sonuc = soru["beklenen_sonuc"]
    return {
        "hatali_adim_no": dogru_adim,
        "beklenen_islem": beklenen_islem,
        "beklenen_sonuc": beklenen_sonuc,
        "kategori": soru.get("kategori", ""),
        "newman_basamagi": soru.get("newman_basamagi", ""),
        "mesaj": (
            f"📘 Doğru Cevap Gösterildi: Hatalı olan {dogru_adim}. Adım için doğru işlem "
            f"{beklenen_islem} = {beklenen_sonuc} olmalıdır. Şimdi sonraki soruya geçebilirsin."
        )
    }


@app.post("/api/dogrula")
def dogrula_cevap(istek: DogrulamaIstegi):
    sorular = load_sorular()
    if istek.soru_id not in sorular:
        raise HTTPException(status_code=404, detail="Soru bulunamadı")

    soru = sorular[istek.soru_id]
    dogru_adim = int(soru["hatali_adim_no"])

    if istek.secilen_adim == 0:
        return {
            "dogru_mu": False,
            "hata_kodu": "OTOMASYON_YANLILIGI",
            "kategori": soru["kategori"],
            "newman_basamagi": soru.get("newman_basamagi", ""),
            "mesaj": "⚠️ Yapay zekanın çözümünde aslında bir hata var! Çözümü her zaman doğru kabul etmemeli, her adımı tek tek kontrol etmelisin."
        }

    if istek.secilen_adim != dogru_adim:
        if istek.secilen_adim > dogru_adim:
            hata_kodu = "ZINCIRLEME_ADIM_HATASI"
            mesaj = (
                f"🔍 {istek.secilen_adim}. adımın sonucu yanlış görünüyor ama bunun sebebi daha önceki bir adımda "
                f"yapılan ilk hatanın bu adıma yansıması! Hatanın ilk başladığı adımı bulmalısın."
            )
        else:
            hata_kodu = "YANLIS_ADIM"
            mesaj = f"❌ Seçtiğin {istek.secilen_adim}. adımda bir hata bulunmuyor. Diğer adımları dikkatle incele."

        return {
            "dogru_mu": False,
            "hata_kodu": hata_kodu,
            "kategori": soru["kategori"],
            "newman_basamagi": soru.get("newman_basamagi", ""),
            "mesaj": mesaj
        }

    if not istek.yazilan_islem.strip() or not str(istek.yazilan_sonuc).strip():
        return {
            "dogru_mu": False,
            "hata_kodu": "EKSIK_GIRIS",
            "kategori": soru["kategori"],
            "newman_basamagi": soru.get("newman_basamagi", ""),
            "mesaj": "✍️ Hatalı adımı doğru buldun! Şimdi bu adımdaki doğru işlemi ve bu adımın sonucunu kutucuklara yazmalısın."
        }

    try:
        ogrenci_islem_degeri = evaluate_math_expr(istek.yazilan_islem)
        ogrenci_sonuc_degeri = float(str(istek.yazilan_sonuc).strip().replace(",", "."))
    except Exception:
        return {
            "dogru_mu": False,
            "hata_kodu": "SOZDIZIMI_HATASI",
            "kategori": soru["kategori"],
            "newman_basamagi": soru.get("newman_basamagi", ""),
            "mesaj": "⚠️ Yazdığın matematiksel işlem okunamadı. Lütfen sadece sayılar ve +, -, *, / işaretlerini kullan."
        }

    gecerli_cozumler = soru.get("alternatif_cozumler", [
        {"islem": soru["beklenen_islem"], "sonuc": soru["beklenen_sonuc"]}
    ])

    islem_ve_sonuc_dogru = False
    for cozum in gecerli_cozumler:
        hedef_sonuc = float(cozum["sonuc"])
        if abs(ogrenci_islem_degeri - hedef_sonuc) < 1e-6 and abs(ogrenci_sonuc_degeri - hedef_sonuc) < 1e-6:
            islem_ve_sonuc_dogru = True
            break

    if islem_ve_sonuc_dogru:
        return {
            "dogru_mu": True,
            "hata_kodu": "DOGRU",
            "kategori": soru["kategori"],
            "newman_basamagi": soru.get("newman_basamagi", ""),
            "mesaj": f"🎉 Tebrikler! {dogru_adim}. adımdaki hatayı başarıyla tespit ettin ve düzelttin."
        }

    final_uyari = soru.get("final_cevap_uyarisi")
    if final_uyari is not None and abs(ogrenci_sonuc_degeri - float(final_uyari)) < 1e-6:
        return {
            "dogru_mu": False,
            "hata_kodu": "FINAL_CEVAP_YAZILDI",
            "kategori": soru["kategori"],
            "newman_basamagi": soru.get("newman_basamagi", ""),
            "mesaj": (
                f"💡 Bulduğun {int(final_uyari)} sayısı problemin en son cevabı! Ancak kural gereği sorunun son cevabını değil, "
                f"sadece hatalı olan {dogru_adim}. adımdaki düzeltilmiş işlemi ve o adımın sonucunu yazmalısın."
            )
        }

    for cozum in gecerli_cozumler:
        hedef_sonuc = float(cozum["sonuc"])
        if abs(ogrenci_islem_degeri - hedef_sonuc) < 1e-6 and abs(ogrenci_sonuc_degeri - hedef_sonuc) >= 1e-6:
            return {
                "dogru_mu": False,
                "hata_kodu": "ISLEM_DOGRU_SONUC_YANLIS",
                "kategori": soru["kategori"],
                "newman_basamagi": soru.get("newman_basamagi", ""),
                "mesaj": f"👍 Kurduğun işlem ({istek.yazilan_islem}) doğru! Ancak eşittirin sağındaki sonucu tekrar hesaplamalısın."
            }

    return {
        "dogru_mu": False,
        "hata_kodu": "YANLIS_DUZELTME",
        "kategori": soru["kategori"],
        "newman_basamagi": soru.get("newman_basamagi", ""),
        "mesaj": f"🎯 {dogru_adim}. adımın hatalı olduğunu doğru yakaladın! Ancak yazdığın düzeltme işlemi veya sonucu bu adım için doğru değil."
    }


@app.post("/api/kaydet-csv")
async def kaydet_csv(request: Request):
    body_bytes = await request.body()
    try:
        data = json.loads(body_bytes.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz JSON verisi")

    sorular_meta = load_sorular()
    katilimci_id = re.sub(r"[^a-zA-Z0-9_-]", "", str(data.get("katilimci_id", "anonim"))) or "anonim"
    kayitlar = data.get("kayitlar", [])
    dosya_yolu = os.path.join(DATA_DIR, f"oturum_{katilimci_id}.csv")

    alanlar = [
        "katilimci_id", "zaman_damgasi", "soru_id", "soru_baslik",
        "hata_kategorisi", "newman_basamagi", "deneme_no",
        "secilen_adim", "yazilan_islem", "yazilan_sonuc",
        "deneme_durum_kodu", "anlik_sure_sn", "soru_toplam_sure_sn",
        "kullanilan_ipucu_seviyesi", "cevap_gosterildi", "soru_genel_durumu"
    ]

    with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=alanlar, delimiter=";")
        writer.writeheader()
        for k in kayitlar:
            q_id = str(k.get("soru_id", ""))
            meta = sorular_meta.get(q_id, {})
            kategori = k.get("kategori") or meta.get("kategori", "")
            newman = k.get("newman_basamagi") or meta.get("newman_basamagi", "")
            denemeler = k.get("deneme_gecmisi", [])

            if denemeler:
                for d in denemeler:
                    writer.writerow({
                        "katilimci_id": katilimci_id,
                        "zaman_damgasi": d.get("zaman_damgasi", datetime.now().isoformat()),
                        "soru_id": q_id,
                        "soru_baslik": k.get("baslik", ""),
                        "hata_kategorisi": kategori,
                        "newman_basamagi": newman,
                        "deneme_no": d.get("deneme_no", ""),
                        "secilen_adim": d.get("secilen_adim", ""),
                        "yazilan_islem": d.get("yazilan_islem", ""),
                        "yazilan_sonuc": d.get("yazilan_sonuc", ""),
                        "deneme_durum_kodu": d.get("durum_kodu", ""),
                        "anlik_sure_sn": d.get("anlik_sure_sn", 0),
                        "soru_toplam_sure_sn": k.get("sure", 0),
                        "kullanilan_ipucu_seviyesi": d.get("ipucu_seviyesi", 0),
                        "cevap_gosterildi": "Evet" if k.get("cevap_gosterildi") else "Hayır",
                        "soru_genel_durumu": k.get("durum", "")
                    })
            else:
                writer.writerow({
                    "katilimci_id": katilimci_id,
                    "zaman_damgasi": k.get("zaman_damgasi", datetime.now().isoformat()),
                    "soru_id": q_id,
                    "soru_baslik": k.get("baslik", ""),
                    "hata_kategorisi": kategori,
                    "newman_basamagi": newman,
                    "deneme_no": 0,
                    "secilen_adim": "",
                    "yazilan_islem": "",
                    "yazilan_sonuc": "",
                    "deneme_durum_kodu": "CEVAP_VERILMEDI",
                    "anlik_sure_sn": 0,
                    "soru_toplam_sure_sn": k.get("sure", 0),
                    "kullanilan_ipucu_seviyesi": k.get("ipucu_seviyesi", 0),
                    "cevap_gosterildi": "Evet" if k.get("cevap_gosterildi") else "Hayır",
                    "soru_genel_durumu": k.get("durum", "Başlanmadı")
                })

    return {"durum": "kaydedildi", "dosya": dosya_yolu}


def _turkce_font_kaydet():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    adaylar = [
        ("C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/segoeuib.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        ("C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/calibrib.ttf"),
        ("C:/Windows/Fonts/tahoma.ttf", "C:/Windows/Fonts/tahomabd.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    ]
    for normal_yol, kalin_yol in adaylar:
        if os.path.exists(normal_yol):
            try:
                if "TRFont" not in pdfmetrics.getRegisteredFontNames():
                    pdfmetrics.registerFont(TTFont("TRFont", normal_yol))
                if os.path.exists(kalin_yol):
                    if "TRFont-Bold" not in pdfmetrics.getRegisteredFontNames():
                        pdfmetrics.registerFont(TTFont("TRFont-Bold", kalin_yol))
                    return "TRFont", "TRFont-Bold", True
                return "TRFont", "TRFont", True
            except Exception:
                continue
    return "Helvetica", "Helvetica-Bold", False


def _ascii_yedek(metin: str) -> str:
    cevir = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return str(metin).translate(cevir)


def olustur_rapor_pdf_bytes(katilimci_id: str, kayitlar: list) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

    sorular_meta = load_sorular()
    font_normal, font_bold, unicode_destek = _turkce_font_kaydet()

    def fmt(val: str) -> str:
        s = str(val or "")
        if not unicode_destek:
            s = _ascii_yedek(s)
        return html.escape(s)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title=f"Hata Avcısı Raporu - {katilimci_id}"
    )

    styles = getSampleStyleSheet()
    baslik_stili = ParagraphStyle(
        "RaporBaslik",
        parent=styles["Heading1"],
        fontName=font_bold,
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4
    )
    alt_baslik_stili = ParagraphStyle(
        "RaporAltBaslik",
        parent=styles["Normal"],
        fontName=font_normal,
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=10
    )
    hucre_stili = ParagraphStyle(
        "TabloHucre",
        parent=styles["Normal"],
        fontName=font_normal,
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1A202C")
    )
    hucre_baslik_stili = ParagraphStyle(
        "TabloBaslik",
        parent=styles["Normal"],
        fontName=font_bold,
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    elemanlar = []
    elemanlar.append(Paragraph(fmt("Hata Avcısı - Performans ve Pedagojik Analiz Raporu"), baslik_stili))
    elemanlar.append(Paragraph(fmt("Eleştirel Yapay Zeka Destekli Matematik Problem Çözme Etkinliği Sonuç Belgesi"), alt_baslik_stili))

    toplam_soru = len(kayitlar)
    tamamlanan = sum(1 for k in kayitlar if k.get("durum") == "Tamamlandı")
    cevap_gosterilen = sum(1 for k in kayitlar if k.get("durum") == "Cevap Gösterildi" or k.get("cevap_gosterildi"))
    toplam_sure = sum(int(k.get("sure", 0)) for k in kayitlar)
    toplam_deneme = sum(int(k.get("deneme", 0)) for k in kayitlar)
    toplam_ipucu = sum(int(k.get("ipucu_seviyesi", 0)) for k in kayitlar)
    tarih_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    ozet_durum_metni = f"{tamamlanan} / {toplam_soru}"
    if cevap_gosterilen > 0:
        ozet_durum_metni += f" ({fmt('Cevap Gösterilen:')} {cevap_gosterilen})"

    ozet_verisi = [
        [
            Paragraph(f"<b>{fmt('Katılımcı ID:')}</b> {fmt(katilimci_id)}", hucre_stili),
            Paragraph(f"<b>{fmt('Rapor Tarihi:')}</b> {fmt(tarih_str)}", hucre_stili),
            Paragraph(f"<b>{fmt('Çözülen:')}</b> {ozet_durum_metni}", hucre_stili),
        ],
        [
            Paragraph(f"<b>{fmt('Toplam Süre:')}</b> {toplam_sure} sn", hucre_stili),
            Paragraph(f"<b>{fmt('Toplam Deneme:')}</b> {toplam_deneme}", hucre_stili),
            Paragraph(f"<b>{fmt('Açılan İpucu:')}</b> {toplam_ipucu}", hucre_stili),
        ]
    ]
    ozet_tablosu = Table(ozet_verisi, colWidths=[62 * mm, 60 * mm, 60 * mm])
    ozet_tablosu.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elemanlar.append(ozet_tablosu)
    elemanlar.append(Spacer(1, 8 * mm))

    tablo_satirlari = [[
        Paragraph(fmt("Soru Başlığı & Durum"), hucre_baslik_stili),
        Paragraph(fmt("Hata Türü & Newman"), hucre_baslik_stili),
        Paragraph(fmt("Süre & İpucu"), hucre_baslik_stili),
        Paragraph(fmt("Öğrencinin Tüm Deneme Adımları"), hucre_baslik_stili),
    ]]

    for k in kayitlar:
        q_id = str(k.get("soru_id", ""))
        meta = sorular_meta.get(q_id, {})
        baslik = k.get("baslik") or meta.get("baslik", f"Soru {q_id}")
        kategori = k.get("kategori") or meta.get("kategori", "-")
        newman = k.get("newman_basamagi") or meta.get("newman_basamagi", "-")
        durum = k.get("durum", "Başlanmadı")
        sure = int(k.get("sure", 0))
        ipucu = int(k.get("ipucu_seviyesi", 0))
        denemeler = k.get("deneme_gecmisi", [])

        if durum == "Tamamlandı":
            durum_renk = "#22543D"
        elif durum == "Cevap Gösterildi":
            durum_renk = "#9C4221"
        else:
            durum_renk = "#744210"

        col1 = Paragraph(
            f"<b>{fmt(baslik)}</b><br/><font color='{durum_renk}'>{fmt(durum)}</font>",
            hucre_stili
        )
        col2 = Paragraph(
            f"{fmt(kategori)}<br/><i>{fmt('Newman: ' + newman)}</i>",
            hucre_stili
        )
        cevap_notu = f"<br/><font color='#9C4221'><i>{fmt('Cevap Gösterildi')}</i></font>" if k.get("cevap_gosterildi") else ""
        col3 = Paragraph(
            f"<b>{sure} sn</b><br/>{fmt('İpucu: ')}{ipucu}/2{cevap_notu}",
            hucre_stili
        )

        if denemeler:
            adim_satirlari = []
            for d in denemeler:
                d_no = d.get("deneme_no", "")
                d_sure = d.get("anlik_sure_sn", 0)
                secim = d.get("secilen_adim", "-")
                islem = d.get("yazilan_islem", "-")
                sonuc_val = d.get("yazilan_sonuc", "-")
                kod = d.get("durum_kodu", "")
                if kod == "DOGRU":
                    renk = "#22543D"
                elif kod == "CEVAP_GOSTERILDI":
                    renk = "#9C4221"
                else:
                    renk = "#9B2C2C"
                detay = "" if secim == "Hata Yok" else f" | {fmt(islem)} = {fmt(sonuc_val)}"
                etiket = fmt("Cevap Gösterildi") if kod == "CEVAP_GOSTERILDI" else f"{d_no}. {fmt('Deneme')}"
                adim_satirlari.append(
                    f"<font color='{renk}'><b>{etiket} ({d_sure}s):</b> {fmt(secim)}{detay} → <i>{fmt(kod)}</i></font>"
                )
            col4 = Paragraph("<br/>".join(adim_satirlari), hucre_stili)
        else:
            col4 = Paragraph(f"<i>{fmt('Cevap verilmedi')}</i>", hucre_stili)

        tablo_satirlari.append([col1, col2, col3, col4])

    ana_tablo = Table(tablo_satirlari, colWidths=[42 * mm, 38 * mm, 24 * mm, 78 * mm], repeatRows=1)
    ana_tablo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elemanlar.append(ana_tablo)

    doc.build(elemanlar)
    return buffer.getvalue()


@app.post("/api/rapor-pdf")
async def rapor_pdf_indir(request: Request):
    body_bytes = await request.body()
    try:
        data = json.loads(body_bytes.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Geçersiz JSON verisi")

    katilimci_id = re.sub(r"[^a-zA-Z0-9_-]", "", str(data.get("katilimci_id", "anonim"))) or "anonim"
    kayitlar = data.get("kayitlar", [])

    try:
        pdf_bytes = olustur_rapor_pdf_bytes(katilimci_id, kayitlar)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF oluşturma hatası: {str(e)}")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="hata_avcisi_{katilimci_id}.pdf"'
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
