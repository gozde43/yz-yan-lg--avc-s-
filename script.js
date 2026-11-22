const STORAGE_KEY = "hata_avcisi_oturum_v4";

let sorular = {};
let soruIdListesi = [];
let aktifIndex = 0;
let katilimciId = "";
let gecenSure = 0;
let zamanlayici = null;
let soruTamamlandi = false;
let oturumBitti = false;

let performansKayitlari = {};

const EGITSEL_GORSELLER = {
    kirtasiye: `
        <svg viewBox="0 0 300 185" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="8" width="284" height="169" rx="10" fill="#ffffff" stroke="#cbd5e0"/>
            <text x="150" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Problemdeki Veriler</text>
            <rect x="22" y="42" width="118" height="62" rx="8" fill="#ebf8ff" stroke="#63b3ed"/>
            <rect x="34" y="54" width="24" height="32" rx="3" fill="#3182ce"/>
            <line x1="39" y1="62" x2="53" y2="62" stroke="#fff" stroke-width="2"/>
            <line x1="39" y1="69" x2="53" y2="69" stroke="#fff" stroke-width="2"/>
            <text x="66" y="68" font-size="12" font-weight="bold" fill="#1a365d">12 Defter</text>
            <text x="66" y="85" font-size="11" fill="#2b6cb0">Tanesi: 45 TL</text>
            <rect x="160" y="42" width="118" height="62" rx="8" fill="#f0fff4" stroke="#68d391"/>
            <polygon points="175,84 182,58 189,84" fill="#38a169"/>
            <text x="198" y="68" font-size="12" font-weight="bold" fill="#22543d">20 Kalem</text>
            <text x="198" y="85" font-size="11" fill="#2f855a">Tanesi: 15 TL</text>
            <rect x="45" y="118" width="210" height="44" rx="8" fill="#fefcbf" stroke="#ecc94b"/>
            <text x="150" y="137" text-anchor="middle" font-size="12" font-weight="bold" fill="#744210">Kırtasiyeciye Verilen: 1000 TL</text>
            <text x="150" y="153" text-anchor="middle" font-size="11" fill="#975a16">Sorulan: Alınacak para üstü (? TL)</text>
        </svg>
    `,
    sinema: `
        <svg viewBox="0 0 300 185" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="8" width="284" height="169" rx="10" fill="#ffffff" stroke="#cbd5e0"/>
            <path d="M 45 30 Q 150 16 255 30" stroke="#2b6cb0" stroke-width="4" fill="none"/>
            <text x="150" y="44" text-anchor="middle" font-size="11" font-weight="bold" fill="#2b6cb0">SİNEMA SALONU DÜZENİ</text>
            <g fill="#63b3ed">
                <rect x="50" y="56" width="16" height="12" rx="2"/><rect x="72" y="56" width="16" height="12" rx="2"/><rect x="94" y="56" width="16" height="12" rx="2"/><text x="122" y="66" font-size="11.5" fill="#4a5568">Her sırada 24 koltuk</text>
                <rect x="50" y="74" width="16" height="12" rx="2"/><rect x="72" y="74" width="16" height="12" rx="2"/><rect x="94" y="74" width="16" height="12" rx="2"/><text x="122" y="84" font-size="11.5" fill="#4a5568">Toplam 18 sıra</text>
                <rect x="50" y="92" width="16" height="12" rx="2"/><rect x="72" y="92" width="16" height="12" rx="2"/><rect x="94" y="92" width="16" height="12" rx="2"/><text x="122" y="102" font-size="11.5" fill="#4a5568">...</text>
            </g>
            <rect x="24" y="118" width="252" height="46" rx="8" fill="#edf2f7" stroke="#cbd5e0"/>
            <text x="150" y="137" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Satılan Bilet Sayısı: 350</text>
            <text x="150" y="154" text-anchor="middle" font-size="11.5" fill="#4a5568">Sorulan: Boş kalan koltuk sayısı (?)</text>
        </svg>
    `,
    otobus: `
        <svg viewBox="0 0 300 185" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="8" width="284" height="169" rx="10" fill="#ffffff" stroke="#cbd5e0"/>
            <text x="150" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Gezi Katılımcıları ve Araç Bilgisi</text>
            <rect x="22" y="38" width="256" height="36" rx="6" fill="#ebf8ff" stroke="#63b3ed"/>
            <text x="150" y="60" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Katılımcılar: 142 Öğrenci ve 14 Öğretmen</text>
            <rect x="35" y="86" width="130" height="46" rx="8" fill="#fefcbf" stroke="#d69e2e" stroke-width="1.5"/>
            <rect x="46" y="95" width="22" height="16" rx="2" fill="#ffffff" stroke="#b7791f"/>
            <rect x="74" y="95" width="22" height="16" rx="2" fill="#ffffff" stroke="#b7791f"/>
            <rect x="102" y="95" width="22" height="16" rx="2" fill="#ffffff" stroke="#b7791f"/>
            <rect x="130" y="95" width="22" height="16" rx="2" fill="#ffffff" stroke="#b7791f"/>
            <circle cx="62" cy="134" r="8" fill="#2d3748"/>
            <circle cx="138" cy="134" r="8" fill="#2d3748"/>
            <text x="225" y="106" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#744210">1 Otobüs</text>
            <text x="225" y="122" text-anchor="middle" font-size="11" fill="#975a16">En fazla 30 yolcu</text>
            <text x="150" y="164" text-anchor="middle" font-size="11.5" fill="#4a5568">Sorulan: En az kaç otobüs gereklidir? (?)</text>
        </svg>
    `,
    ciftlik: `
        <svg viewBox="0 0 300 185" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="8" width="284" height="169" rx="10" fill="#ffffff" stroke="#cbd5e0"/>
            <text x="150" y="28" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Çiftlikte Toplanan Yumurtalar</text>
            <rect x="20" y="40" width="122" height="52" rx="8" fill="#ebf8ff" stroke="#63b3ed"/>
            <text x="81" y="61" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Pazartesi</text>
            <text x="81" y="80" text-anchor="middle" font-size="12" fill="#2b6cb0">1450 yumurta</text>
            <rect x="158" y="40" width="122" height="52" rx="8" fill="#f0fff4" stroke="#68d391"/>
            <text x="219" y="61" text-anchor="middle" font-size="12" font-weight="bold" fill="#22543d">Salı</text>
            <text x="219" y="80" text-anchor="middle" font-size="11" fill="#2f855a">Pzt'den 320 fazla</text>
            <rect x="20" y="104" width="260" height="60" rx="8" fill="#edf2f7" stroke="#cbd5e0"/>
            <text x="150" y="125" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Ayrılan Kırık Yumurta: 500 adet</text>
            <text x="150" y="143" text-anchor="middle" font-size="11.5" fill="#4a5568">Sağlam yumurtalar 10'arlı kolilere konur</text>
            <text x="150" y="159" text-anchor="middle" font-size="11" fill="#2b6cb0">Sorulan: Toplam kaç koli oluşur? (?)</text>
        </svg>
    `,
    parkur: `
        <svg viewBox="0 0 300 185" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="8" width="284" height="169" rx="10" fill="#ffffff" stroke="#cbd5e0"/>
            <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">Koşu Parkuru Bilgileri</text>
            <rect x="45" y="38" width="210" height="58" rx="29" fill="#f0fff4" stroke="#38a169" stroke-width="3"/>
            <text x="150" y="64" text-anchor="middle" font-size="12" font-weight="bold" fill="#22543d">1 Tam Tur = 400 m</text>
            <text x="150" y="81" text-anchor="middle" font-size="10.5" fill="#2f855a">Okul Bahçesi Parkuru</text>
            <rect x="22" y="108" width="256" height="56" rx="8" fill="#ebf8ff" stroke="#63b3ed"/>
            <text x="150" y="128" text-anchor="middle" font-size="11.5" fill="#1a365d">Pzt ve Salı Toplamı: 3200 m</text>
            <text x="150" y="144" text-anchor="middle" font-size="11.5" fill="#2b6cb0">Çarşamba: Pzt-Salı toplamının 2 katı</text>
            <text x="150" y="159" text-anchor="middle" font-size="11" fill="#4a5568">Sorulan: Çarşamba günü atılan tur sayısı (?)</text>
        </svg>
    `,
    kitap: `
        <svg viewBox="0 0 300 185" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="8" width="284" height="169" rx="10" fill="#ffffff" stroke="#cbd5e0"/>
            <text x="150" y="26" text-anchor="middle" font-size="12" font-weight="bold" fill="#1a365d">4 Haftalık Okuma Kampanyası</text>
            <rect x="18" y="48" width="56" height="54" rx="6" fill="#ebf8ff" stroke="#63b3ed"/>
            <text x="46" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#1a365d">1. Hafta</text>
            <text x="46" y="88" text-anchor="middle" font-size="13" font-weight="bold" fill="#2b6cb0">35</text>

            <text x="83" y="78" text-anchor="middle" font-size="11" font-weight="bold" fill="#38a169">+15</text>
            <rect x="92" y="48" width="56" height="54" rx="6" fill="#edf2f7" stroke="#cbd5e0"/>
            <text x="120" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#4a5568">2. Hafta</text>
            <text x="120" y="88" text-anchor="middle" font-size="13" fill="#4a5568">?</text>

            <text x="157" y="78" text-anchor="middle" font-size="11" font-weight="bold" fill="#38a169">+15</text>
            <rect x="166" y="48" width="56" height="54" rx="6" fill="#edf2f7" stroke="#cbd5e0"/>
            <text x="194" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#4a5568">3. Hafta</text>
            <text x="194" y="88" text-anchor="middle" font-size="13" fill="#4a5568">?</text>

            <text x="231" y="78" text-anchor="middle" font-size="11" font-weight="bold" fill="#38a169">+15</text>
            <rect x="240" y="48" width="44" height="54" rx="6" fill="#edf2f7" stroke="#cbd5e0"/>
            <text x="262" y="68" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#4a5568">4. Hft</text>
            <text x="262" y="88" text-anchor="middle" font-size="12" fill="#4a5568">?</text>

            <rect x="20" y="118" width="260" height="44" rx="8" fill="#fefcbf" stroke="#ecc94b"/>
            <text x="150" y="137" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#744210">Her hafta bir önceki haftadan 15 sayfa fazla</text>
            <text x="150" y="153" text-anchor="middle" font-size="11" fill="#975a16">Sorulan: 4 haftanın sonunda toplam sayfa (?)</text>
        </svg>
    `
};

window.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/api/sorular");
        sorular = await res.json();
        soruIdListesi = Object.keys(sorular);
        oturumKurtarmayiKontrolEt();
    } catch (err) {
        document.getElementById("durum").textContent = "Sunucu bağlantı hatası!";
    }
});

window.addEventListener("beforeunload", (e) => {
    const kayitListesi = Object.values(performansKayitlari);
    if (kayitListesi.length > 0 && !oturumBitti) {
        const payload = JSON.stringify({
            katilimci_id: katilimciId || "anonim",
            kayitlar: kayitListesi
        });
        navigator.sendBeacon("/api/kaydet-csv", payload);
        yerelDurumuKaydet();

        e.preventDefault();
        e.returnValue = "İlerlemeniz kaydedildi ancak etkinlik henüz bitmedi. Çıkmak istediğinize emin misiniz?";
    }
});

let kurtarilabilirOturum = null;

function oturumKurtarmayiKontrolEt() {
    const kayitli = localStorage.getItem(STORAGE_KEY);
    if (!kayitli) return;

    try {
        const parsed = JSON.parse(kayitli);
        if (
            parsed &&
            !parsed.oturumBitti &&
            parsed.performansKayitlari &&
            Object.keys(parsed.performansKayitlari).length > 0
        ) {
            const kayitliIndex = Number(parsed.aktifIndex) || 0;
            const toplamDeneme = Object.values(parsed.performansKayitlari).reduce(
                (acc, k) => acc + (Number(k.deneme) || 0),
                0
            );
            if (kayitliIndex > 0 || toplamDeneme > 0) {
                kurtarilabilirOturum = parsed;
                const kutu = document.getElementById("kayitli-oturum-kutusu");
                const bilgi = document.getElementById("kayitli-oturum-bilgi");
                if (kutu && bilgi) {
                    const gosterilenSoruNo = Math.min(kayitliIndex + 1, soruIdListesi.length);
                    bilgi.innerHTML = `💾 <strong>Yarım kalan oturum bulundu:</strong> Katılımcı <code>${parsed.katilimciId || "anonim"}</code> (${gosterilenSoruNo}. Soru)`;
                    kutu.style.display = "flex";
                }
            }
        }
    } catch (e) {
        localStorage.removeItem(STORAGE_KEY);
    }
}

function kayitliOturumaDevamEt() {
    if (!kurtarilabilirOturum) return;
    const parsed = kurtarilabilirOturum;

    katilimciId = parsed.katilimciId || rastgeleIdUret();
    aktifIndex = Number(parsed.aktifIndex) || 0;
    performansKayitlari = parsed.performansKayitlari;
    oturumBitti = Boolean(parsed.oturumBitti);

    document.getElementById("kurallar-alani").style.display = "none";
    document.getElementById("ust-bilgi-cubugu").style.display = "flex";
    document.getElementById("katilimci-etiket").textContent = `👤 Katılımcı: ${katilimciId}`;

    if (oturumBitti || aktifIndex >= soruIdListesi.length) {
        raporuGoster(false);
    } else {
        document.getElementById("oyun-alani").style.display = "block";
        soruyuYukle(aktifIndex);
    }
}

function rastgeleIdUret() {
    const tarih = new Date();
    const kod = Math.floor(1000 + Math.random() * 9000);
    return `OGR-${tarih.getHours()}${tarih.getMinutes()}-${kod}`;
}

function etkinligiBaslat() {
    localStorage.removeItem(STORAGE_KEY);
    performansKayitlari = {};
    kurtarilabilirOturum = null;

    const girilenKod = document.getElementById("katilimci-kodu-input").value.trim();
    katilimciId = girilenKod ? girilenKod.replace(/[^a-zA-Z0-9_-]/g, "") : rastgeleIdUret();

    soruIdListesi.forEach((id) => {
        const s = sorular[id];
        performansKayitlari[id] = {
            soru_id: id,
            baslik: s.baslik,
            kategori: "",
            newman_basamagi: "",
            durum: "Başlanmadı",
            sure: 0,
            deneme: 0,
            ipucu_seviyesi: 0,
            iki_ipucu_sonrasi_hata: false,
            cevap_gosterildi: false,
            gosterilen_cevap_metni: "",
            deneme_gecmisi: [],
            zaman_damgasi: new Date().toISOString()
        };
    });

    aktifIndex = 0;
    oturumBitti = false;
    yerelDurumuKaydet();

    document.getElementById("kurallar-alani").style.display = "none";
    document.getElementById("ust-bilgi-cubugu").style.display = "flex";
    document.getElementById("katilimci-etiket").textContent = `👤 Katılımcı: ${katilimciId}`;
    document.getElementById("oyun-alani").style.display = "block";

    soruyuYukle(0);
}

function yerelDurumuKaydet() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
        katilimciId,
        aktifIndex,
        performansKayitlari,
        oturumBitti
    }));
}

function bolmeAlgoritmasiOlustur(b) {
    return `
        <div class="bolme-sema-kapsayici" aria-label="Kalanlı bölme işlemi şeması">
            <span class="bolme-baslik">📐 Bölme İşlemi Gösterimi:</span>
            <table class="bolme-tablosu">
                <tr>
                    <td class="bolunen-hucre">${b.bolunen}</td>
                    <td class="bolen-hucre">${b.bolen}</td>
                    <td class="bolme-etiket-hucre">← Bölünen | Bölen</td>
                </tr>
                <tr>
                    <td class="carpim-hucre">${b.carpim}</td>
                    <td class="bolum-hucre">${b.bolum}</td>
                    <td class="bolme-etiket-hucre">← Bölüm</td>
                </tr>
                <tr>
                    <td class="kalan-hucre">${String(b.kalan).padStart(3, "0")}</td>
                    <td></td>
                    <td class="bolme-etiket-hucre">← <strong>Kalan: ${b.kalan}</strong></td>
                </tr>
            </table>
        </div>
    `;
}

function soruyuYukle(index) {
    const qId = soruIdListesi[index];
    const soru = sorular[qId];
    soruTamamlandi = false;

    if (!performansKayitlari[qId]) {
        performansKayitlari[qId] = {
            soru_id: qId,
            baslik: soru.baslik,
            kategori: "",
            newman_basamagi: "",
            durum: "Devam Ediyor",
            sure: 0,
            deneme: 0,
            ipucu_seviyesi: 0,
            iki_ipucu_sonrasi_hata: false,
            cevap_gosterildi: false,
            gosterilen_cevap_metni: "",
            deneme_gecmisi: [],
            zaman_damgasi: new Date().toISOString()
        };
    }

    const kayit = performansKayitlari[qId];
    if (kayit.durum === "Başlanmadı") {
        kayit.durum = "Devam Ediyor";
    }

    document.getElementById("durum").textContent = `Soru ${index + 1} / ${soruIdListesi.length}`;

    document.getElementById("soru-metni-alani").innerHTML = `
        <h3>${soru.baslik}</h3>
        <p>${soru.metin}</p>
    `;
    document.getElementById("soru-gorsel-alani").innerHTML = EGITSEL_GORSELLER[soru.gorsel_tipi] || "";

    const adimlarListesi = document.getElementById("adimlar-listesi");
    adimlarListesi.innerHTML = "";
    soru.yapay_zeka_cozumu.forEach((adimMetni, idx) => {
        const adimNo = idx + 1;
        const div = document.createElement("div");
        div.className = "adim-kart";
        let icerik = `<p class="adim-metin">${adimMetni}</p>`;
        if (soru.bolme_gorseli && soru.bolme_gorseli.adim_no === adimNo) {
            icerik += bolmeAlgoritmasiOlustur(soru.bolme_gorseli);
        }
        div.innerHTML = icerik;
        adimlarListesi.appendChild(div);
    });

    const secimAlani = document.getElementById("adim-secim-alani");
    secimAlani.innerHTML = "";

    soru.yapay_zeka_cozumu.forEach((_, idx) => {
        const adimNo = idx + 1;
        const label = document.createElement("label");
        label.innerHTML = `<input type="radio" name="adim_secim" value="${adimNo}"> ${adimNo}. Adım`;
        label.querySelector("input").addEventListener("change", () => secimGorseliniGuncelle(adimNo));
        secimAlani.appendChild(label);
    });

    const hataYokLabel = document.createElement("label");
    hataYokLabel.className = "hata-yok-secenek";
    hataYokLabel.innerHTML = `<input type="radio" name="adim_secim" value="0"> ✅ Hata Yok (Tüm adımlar doğru)`;
    hataYokLabel.querySelector("input").addEventListener("change", () => secimGorseliniGuncelle(0));
    secimAlani.appendChild(hataYokLabel);

    document.getElementById("dogru-islem-input").value = "";
    document.getElementById("dogru-sonuc-input").value = "";
    document.getElementById("duzeltme-giris-alani").style.display = "block";
    document.getElementById("geri-bildirim").style.display = "none";
    document.getElementById("ipucu-kutusu").style.display = "none";
    document.getElementById("gonder-btn").style.display = "inline-block";
    document.getElementById("gonder-btn").disabled = false;
    document.getElementById("sonraki-btn").style.display = "none";

    const toplamIpucu = soru.toplam_ipucu || 2;
    const mevcutIpucuSeviye = kayit.ipucu_seviyesi || 0;
    const ipucuBtn = document.getElementById("ipucu-btn");
    const cevabiGosterBtn = document.getElementById("cevabi-goster-btn");
    const sonrakiBtn = document.getElementById("sonraki-btn");
    const geriBildirim = document.getElementById("geri-bildirim");

    cevabiGosterBtn.style.display = "none";
    cevabiGosterBtn.disabled = false;

    if (kayit.cevap_gosterildi || kayit.durum === "Cevap Gösterildi") {
        soruTamamlandi = true;
        ipucuBtn.style.display = "none";
        document.getElementById("gonder-btn").style.display = "none";
        sonrakiBtn.style.display = "inline-block";
        sonrakiBtn.textContent = index === soruIdListesi.length - 1
            ? "Etkinliği Tamamla ve Raporu Gör 📊"
            : "Sonraki Soruya Geç →";
        if (kayit.gosterilen_cevap_metni) {
            geriBildirim.className = "geri-bildirim cevap-gosterildi";
            geriBildirim.style.display = "block";
            geriBildirim.textContent = kayit.gosterilen_cevap_metni;
        }
    } else if (kayit.durum === "Tamamlandı") {
        soruTamamlandi = true;
        ipucuBtn.style.display = "none";
        document.getElementById("gonder-btn").style.display = "none";
        sonrakiBtn.style.display = "inline-block";
        sonrakiBtn.textContent = index === soruIdListesi.length - 1
            ? "Etkinliği Tamamla ve Raporu Gör 📊"
            : "Sonraki Soruya Geç →";
    } else if (kayit.deneme > 0) {
        ipucuBtn.style.display = "inline-block";
        ipucuBtn.disabled = mevcutIpucuSeviye >= toplamIpucu;
        ipucuBtn.textContent = mevcutIpucuSeviye >= toplamIpucu
            ? `💡 Tüm İpuçları Alındı (${toplamIpucu}/${toplamIpucu})`
            : `💡 İpucu Al (${mevcutIpucuSeviye + 1}/${toplamIpucu})`;

        if (kayit.iki_ipucu_sonrasi_hata) {
            cevabiGosterBtn.style.display = "inline-block";
        }
    } else {
        ipucuBtn.style.display = "none";
    }

    clearInterval(zamanlayici);
    gecenSure = kayit.sure || 0;
    document.getElementById("sure-sayaci").textContent = `⏱️ ${gecenSure}s`;
    zamanlayici = setInterval(() => {
        if (!soruTamamlandi) {
            gecenSure++;
            kayit.sure = gecenSure;
            document.getElementById("sure-sayaci").textContent = `⏱️ ${gecenSure}s`;
            if (gecenSure % 5 === 0) yerelDurumuKaydet();
        }
    }, 1000);
}

function secimGorseliniGuncelle(secilenDeger) {
    document.querySelectorAll("#adim-secim-alani label").forEach((lbl) => {
        const inp = lbl.querySelector("input");
        lbl.classList.toggle("secili", inp && Number(inp.value) === Number(secilenDeger));
    });

    const duzeltmeAlani = document.getElementById("duzeltme-giris-alani");
    duzeltmeAlani.style.display = Number(secilenDeger) === 0 ? "none" : "block";
}

async function ipucuIste() {
    const qId = soruIdListesi[aktifIndex];
    const soru = sorular[qId];
    const kayit = performansKayitlari[qId];
    const toplamIpucu = soru.toplam_ipucu || 2;
    const yeniSeviye = (kayit.ipucu_seviyesi || 0) + 1;
    if (yeniSeviye > toplamIpucu) return;

    try {
        const res = await fetch("/api/ipucu", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ soru_id: qId, seviye: yeniSeviye })
        });
        const data = await res.json();

        kayit.ipucu_seviyesi = data.seviye;
        yerelDurumuKaydet();

        const ipucuKutusu = document.getElementById("ipucu-kutusu");
        ipucuKutusu.style.display = "block";
        ipucuKutusu.innerHTML = `<strong>💡 İpucu (${data.seviye}/${data.toplam_seviye}):</strong> ${data.ipucu_metni}`;

        const ipucuBtn = document.getElementById("ipucu-btn");
        if (data.seviye >= data.toplam_seviye) {
            ipucuBtn.disabled = true;
            ipucuBtn.textContent = `💡 Tüm İpuçları Alındı (${data.toplam_seviye}/${data.toplam_seviye})`;
        } else {
            ipucuBtn.textContent = `💡 İpucu Al (${data.seviye + 1}/${data.toplam_seviye})`;
        }
    } catch (err) {
        console.error("İpucu alınamadı:", err);
    }
}

async function dogrulaVeGonder() {
    const secilenRadio = document.querySelector('input[name="adim_secim"]:checked');
    const geriBildirim = document.getElementById("geri-bildirim");

    if (!secilenRadio) {
        geriBildirim.className = "geri-bildirim hatali";
        geriBildirim.style.display = "block";
        geriBildirim.textContent = "⚠️ Lütfen önce hatalı olduğunu düşündüğün adımı veya 'Hata Yok' seçeneğini işaretle.";
        return;
    }

    const qId = soruIdListesi[aktifIndex];
    const soru = sorular[qId];
    const kayit = performansKayitlari[qId];
    const secilenAdim = parseInt(secilenRadio.value, 10);
    const secilenAdimMetni = secilenAdim === 0 ? "Hata Yok" : `${secilenAdim}. Adım`;
    const yazilanIslem = document.getElementById("dogru-islem-input").value.trim();
    const yazilanSonuc = document.getElementById("dogru-sonuc-input").value.trim();
    const zamanDamgasi = new Date().toISOString();

    kayit.deneme += 1;
    kayit.zaman_damgasi = zamanDamgasi;

    try {
        const res = await fetch("/api/dogrula", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                katilimci_id: katilimciId,
                soru_id: qId,
                secilen_adim: secilenAdim,
                yazilan_islem: yazilanIslem,
                yazilan_sonuc: yazilanSonuc,
                gecen_sure: gecenSure,
                deneme_sayisi: kayit.deneme,
                kullanilan_ipucu_seviyesi: kayit.ipucu_seviyesi
            })
        });
        const sonuc = await res.json();

        if (sonuc.kategori) kayit.kategori = sonuc.kategori;
        if (sonuc.newman_basamagi) kayit.newman_basamagi = sonuc.newman_basamagi;

        kayit.deneme_gecmisi.push({
            deneme_no: kayit.deneme,
            zaman_damgasi: zamanDamgasi,
            secilen_adim: secilenAdimMetni,
            yazilan_islem: secilenAdim === 0 ? "-" : yazilanIslem,
            yazilan_sonuc: secilenAdim === 0 ? "-" : yazilanSonuc,
            durum_kodu: sonuc.hata_kodu,
            anlik_sure_sn: gecenSure,
            ipucu_seviyesi: kayit.ipucu_seviyesi
        });

        const ipucuBtn = document.getElementById("ipucu-btn");
        const cevabiGosterBtn = document.getElementById("cevabi-goster-btn");
        const toplamIpucu = soru.toplam_ipucu || 2;

        geriBildirim.style.display = "block";
        if (sonuc.dogru_mu) {
            soruTamamlandi = true;
            clearInterval(zamanlayici);
            kayit.durum = "Tamamlandı";
            geriBildirim.className = "geri-bildirim basarili";
            geriBildirim.textContent = sonuc.mesaj;

            ipucuBtn.style.display = "none";
            cevabiGosterBtn.style.display = "none";
            document.getElementById("gonder-btn").style.display = "none";
            const sonrakiBtn = document.getElementById("sonraki-btn");
            sonrakiBtn.style.display = "inline-block";
            sonrakiBtn.textContent = aktifIndex === soruIdListesi.length - 1
                ? "Etkinliği Tamamla ve Raporu Gör 📊"
                : "Sonraki Soruya Geç →";
        } else {
            geriBildirim.className = "geri-bildirim hatali";
            geriBildirim.textContent = sonuc.mesaj;

            ipucuBtn.style.display = "inline-block";
            ipucuBtn.disabled = kayit.ipucu_seviyesi >= toplamIpucu;
            ipucuBtn.textContent = kayit.ipucu_seviyesi >= toplamIpucu
                ? `💡 Tüm İpuçları Alındı (${toplamIpucu}/${toplamIpucu})`
                : `💡 İpucu Al (${kayit.ipucu_seviyesi + 1}/${toplamIpucu})`;

            if (kayit.ipucu_seviyesi >= toplamIpucu) {
                kayit.iki_ipucu_sonrasi_hata = true;
                cevabiGosterBtn.style.display = "inline-block";
                cevabiGosterBtn.disabled = false;
            }
        }

        yerelDurumuKaydet();
        sunucuyaCsvYedekle();
    } catch (err) {
        geriBildirim.className = "geri-bildirim hatali";
        geriBildirim.style.display = "block";
        geriBildirim.textContent = "Sunucu doğrulaması sırasında bağlantı hatası oluştu.";
    }
}

async function cevabiGoster() {
    const qId = soruIdListesi[aktifIndex];
    const kayit = performansKayitlari[qId];
    const cevabiGosterBtn = document.getElementById("cevabi-goster-btn");
    const geriBildirim = document.getElementById("geri-bildirim");

    cevabiGosterBtn.disabled = true;

    try {
        const res = await fetch("/api/cevabi-goster", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ soru_id: qId })
        });
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }
        const data = await res.json();
        const zamanDamgasi = new Date().toISOString();

        soruTamamlandi = true;
        clearInterval(zamanlayici);

        if (data.kategori) kayit.kategori = data.kategori;
        if (data.newman_basamagi) kayit.newman_basamagi = data.newman_basamagi;

        kayit.cevap_gosterildi = true;
        kayit.durum = "Cevap Gösterildi";
        kayit.gosterilen_cevap_metni = data.mesaj;
        kayit.zaman_damgasi = zamanDamgasi;

        kayit.deneme_gecmisi.push({
            deneme_no: "-",
            zaman_damgasi: zamanDamgasi,
            secilen_adim: `${data.hatali_adim_no}. Adım (Cevap Gösterildi)`,
            yazilan_islem: data.beklenen_islem,
            yazilan_sonuc: String(data.beklenen_sonuc),
            durum_kodu: "CEVAP_GOSTERILDI",
            anlik_sure_sn: gecenSure,
            ipucu_seviyesi: kayit.ipucu_seviyesi
        });

        geriBildirim.className = "geri-bildirim cevap-gosterildi";
        geriBildirim.style.display = "block";
        geriBildirim.textContent = data.mesaj;

        document.getElementById("gonder-btn").style.display = "none";
        document.getElementById("ipucu-btn").style.display = "none";
        cevabiGosterBtn.style.display = "none";

        const sonrakiBtn = document.getElementById("sonraki-btn");
        sonrakiBtn.style.display = "inline-block";
        sonrakiBtn.textContent = aktifIndex === soruIdListesi.length - 1
            ? "Etkinliği Tamamla ve Raporu Gör 📊"
            : "Sonraki Soruya Geç →";

        yerelDurumuKaydet();
        sunucuyaCsvYedekle();
    } catch (err) {
        cevabiGosterBtn.disabled = false;
        geriBildirim.className = "geri-bildirim hatali";
        geriBildirim.style.display = "block";
        geriBildirim.textContent = "Cevap getirilirken sunucu bağlantı hatası oluştu.";
    }
}

function sonrakiSoruyaGec() {
    aktifIndex++;
    yerelDurumuKaydet();

    if (aktifIndex < soruIdListesi.length) {
        soruyuYukle(aktifIndex);
    } else {
        oturumBitti = true;
        yerelDurumuKaydet();
        raporuGoster(true);
    }
}

function raporuGoster(otomatikIndir = true) {
    clearInterval(zamanlayici);
    document.getElementById("oyun-alani").style.display = "none";
    document.getElementById("rapor-alani").style.display = "block";
    document.getElementById("durum").textContent = "Etkinlik Tamamlandı ✅";

    const kayitListesi = Object.values(performansKayitlari);
    const toplamSure = kayitListesi.reduce((acc, k) => acc + (Number(k.sure) || 0), 0);
    const toplamDeneme = kayitListesi.reduce((acc, k) => acc + (Number(k.deneme) || 0), 0);
    const toplamIpucu = kayitListesi.reduce((acc, k) => acc + (Number(k.ipucu_seviyesi) || 0), 0);
    const tamamlanan = kayitListesi.filter((k) => k.durum === "Tamamlandı").length;
    const cevapGosterilen = kayitListesi.filter((k) => k.durum === "Cevap Gösterildi" || k.cevap_gosterildi).length;

    const cevapGosterilenOzet = cevapGosterilen > 0
        ? ` &nbsp;|&nbsp; <strong>Cevap Gösterilen:</strong> ${cevapGosterilen}`
        : "";

    document.getElementById("rapor-ozet-bilgi").innerHTML = `
        <strong>Katılımcı:</strong> ${katilimciId || "anonim"} &nbsp;|&nbsp;
        <strong>Çözülen:</strong> ${tamamlanan}/${soruIdListesi.length}${cevapGosterilenOzet} &nbsp;|&nbsp;
        <strong>Toplam Süre:</strong> ${toplamSure} sn &nbsp;|&nbsp;
        <strong>Toplam Deneme:</strong> ${toplamDeneme} &nbsp;|&nbsp;
        <strong>Açılan İpucu:</strong> ${toplamIpucu}
    `;

    const govde = document.getElementById("rapor-govdesi");
    govde.innerHTML = "";

    soruIdListesi.forEach((qId) => {
        const k = performansKayitlari[qId];
        const denemeler = k.deneme_gecmisi || [];
        let denemeHtml = "<small>Henüz cevap verilmedi</small>";

        if (denemeler.length > 0) {
            const maddeler = denemeler.map((d) => {
                const islemBilgisi = d.secilen_adim === "Hata Yok"
                    ? ""
                    : ` | İşlem: <code>${d.yazilan_islem || "-"}</code> = <code>${d.yazilan_sonuc || "-"}</code>`;

                let renk = "#c53030";
                let etiket = `${d.deneme_no}. Deneme`;
                if (d.durum_kodu === "DOGRU") {
                    renk = "#2f855a";
                } else if (d.durum_kodu === "CEVAP_GOSTERILDI") {
                    renk = "#9c4221";
                    etiket = "👁️ Cevap Gösterildi";
                }
                return `<li style="color:${renk};"><strong>${etiket} (${d.anlik_sure_sn}s):</strong> ${d.secilen_adim}${islemBilgisi} → <em>${d.durum_kodu}</em></li>`;
            }).join("");
            denemeHtml = `<ul class="deneme-listesi">${maddeler}</ul>`;
        }

        let rozetSinif = "beklemede";
        let rozetMetni = k.durum || "Başlanmadı";
        if (k.durum === "Tamamlandı") {
            rozetSinif = "tamamlandi";
            rozetMetni = "✅ Tamamlandı";
        } else if (k.durum === "Cevap Gösterildi" || k.cevap_gosterildi) {
            rozetSinif = "cevap-gosterildi";
            rozetMetni = "👁️ Cevap Gösterildi";
        }

        const cevapDurumNotu = (k.durum === "Cevap Gösterildi" || k.cevap_gosterildi)
            ? ` | Cevap Gösterildi: <strong>Evet</strong>`
            : "";

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${k.baslik}</strong><br><span class="durum-rozet ${rozetSinif}">${rozetMetni}</span></td>
            <td>${k.kategori || "-"}<br><small><em>Newman: ${k.newman_basamagi || "-"}</em></small></td>
            <td>${k.sure} sn</td>
            <td>Toplam Deneme: <strong>${k.deneme}</strong> | Açılan İpucu: <strong>${k.ipucu_seviyesi}/2</strong>${cevapDurumNotu}${denemeHtml}</td>
        `;
        govde.appendChild(tr);
    });

    sunucuyaCsvYedekle();
    if (otomatikIndir) {
        csvIndir(true);
    }
}

async function sunucuyaCsvYedekle() {
    const kayitListesi = Object.values(performansKayitlari);
    if (kayitListesi.length === 0) return;

    try {
        await fetch("/api/kaydet-csv", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                katilimci_id: katilimciId || "anonim",
                kayitlar: kayitListesi
            })
        });
    } catch (e) {
        console.warn("Sunucu CSV yedeği alınamadı:", e);
    }
}

function csvIndir(sessiz = false) {
    const kayitListesi = Object.values(performansKayitlari);
    if (kayitListesi.length === 0) {
        if (!sessiz) alert("Henüz indirilecek bir etkinlik verisi bulunmuyor.");
        return;
    }

    const basliklar = [
        "Katilimci_ID", "Zaman_Damgasi", "Soru_ID", "Soru_Baslik",
        "Hata_Kategorisi", "Newman_Basamagi", "Deneme_No",
        "Secilen_Adim", "Yazilan_Islem", "Yazilan_Sonuc",
        "Deneme_Durum_Kodu", "Anlik_Sure_Sn", "Soru_Toplam_Sure_Sn",
        "Kullanilan_Ipucu_Seviyesi", "Cevap_Gosterildi", "Soru_Genel_Durumu"
    ];

    const satirlar = [basliklar.join(";")];

    kayitListesi.forEach((k) => {
        const denemeler = k.deneme_gecmisi || [];
        if (denemeler.length > 0) {
            denemeler.forEach((d) => {
                const satir = [
                    katilimciId || "anonim",
                    d.zaman_damgasi || k.zaman_damgasi || new Date().toISOString(),
                    k.soru_id,
                    `"${(k.baslik || "").replace(/"/g, '""')}"`,
                    `"${(k.kategori || "").replace(/"/g, '""')}"`,
                    `"${(k.newman_basamagi || "").replace(/"/g, '""')}"`,
                    d.deneme_no,
                    `"${(d.secilen_adim || "").replace(/"/g, '""')}"`,
                    `"${(d.yazilan_islem || "").replace(/"/g, '""')}"`,
                    `"${(d.yazilan_sonuc || "").replace(/"/g, '""')}"`,
                    d.durum_kodu,
                    d.anlik_sure_sn,
                    k.sure,
                    d.ipucu_seviyesi,
                    k.cevap_gosterildi ? "Evet" : "Hayır",
                    k.durum
                ];
                satirlar.push(satir.join(";"));
            });
        } else {
            const satir = [
                katilimciId || "anonim",
                k.zaman_damgasi || new Date().toISOString(),
                k.soru_id,
                `"${(k.baslik || "").replace(/"/g, '""')}"`,
                `"${(k.kategori || "").replace(/"/g, '""')}"`,
                `"${(k.newman_basamagi || "").replace(/"/g, '""')}"`,
                0,
                `""`,
                `""`,
                `""`,
                "CEVAP_VERILMEDI",
                0,
                k.sure,
                k.ipucu_seviyesi || 0,
                k.cevap_gosterildi ? "Evet" : "Hayır",
                k.durum || "Başlanmadı"
            ];
            satirlar.push(satir.join(";"));
        }
    });

    const csvIcerik = "\uFEFF" + satirlar.join("\n");
    const blob = new Blob([csvIcerik], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `hata_avcisi_${katilimciId || "sonuclar"}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

async function pdfIndir(sessiz = false) {
    const kayitListesi = Object.values(performansKayitlari);
    if (kayitListesi.length === 0) {
        if (!sessiz) alert("Henüz indirilecek bir etkinlik verisi bulunmuyor.");
        return;
    }

    try {
        const res = await fetch("/api/rapor-pdf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                katilimci_id: katilimciId || "anonim",
                kayitlar: kayitListesi
            })
        });

        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`);
        }

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `hata_avcisi_${katilimciId || "sonuclar"}.pdf`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (err) {
        console.warn("Sunucu PDF oluşturma başarısız, yazdırma/PDF penceresine geçiliyor:", err);
        if (!sessiz) {
            window.print();
        }
    }
}

function guvenliYenidenBasla() {
    csvIndir(true);
    localStorage.removeItem(STORAGE_KEY);
    setTimeout(() => {
        location.reload();
    }, 300);
}
