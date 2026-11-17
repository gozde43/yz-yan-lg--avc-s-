let sorular = [];
let aktifSoruIndex = 0;
let saniye = 0;
let zamanlayici = null;
let denemeSayisi = 0;
let hataKayitlari = [];
let raporVerileri = [];

async function sorulariGetir() {
    try {
        const response = await fetch('/api/sorular');
        if (!response.ok) throw new Error("Sorular yüklenemedi!");
        
        const veri = await response.json();
        // Senin JSON dosyan obje {"1": {...}, "2": {...}} olduğu için diziye çeviriyoruz:
        sorular = Object.values(veri);
        
        if (sorular.length > 0) {
            soruyuEkranaBas(aktifSoruIndex);
        } else {
            document.getElementById('durum').innerText = "Hiç soru bulunamadı.";
        }
    } catch (error) {
        console.error("Hata:", error);
        document.getElementById('durum').innerText = "Sorular yüklenirken hata oluştu.";
    }
}

function sureyiBaslat() {
    clearInterval(zamanlayici);
    saniye = 0;
    document.getElementById('sure-sayaci').innerText = `⏱️ 0s`;
    zamanlayici = setInterval(() => {
        saniye++;
        document.getElementById('sure-sayaci').innerText = `⏱️ ${saniye}s`;
    }, 1000);
}

function soruyuEkranaBas(index) {
    const soru = sorular[index];
    denemeSayisi = 0;
    hataKayitlari = [];

    document.getElementById('durum').innerText = `Soru ${index + 1} / ${sorular.length} • Kategori: ${soru.kategori}`;
    document.getElementById('soru-alani').innerHTML = `<h3>${soru.baslik}</h3><p>${soru.metin}</p>`;

    const adimlarListesi = document.getElementById('adimlar-listesi');
    const adimSecimAlani = document.getElementById('adim-secim-alani');
    
    adimlarListesi.innerHTML = "";
    adimSecimAlani.innerHTML = "";

    soru.yapay_zeka_cozumu.forEach((adim, i) => {
        const adimNo = i + 1;
        adimlarListesi.innerHTML += `<p>${adim}</p>`;
        adimSecimAlani.innerHTML += `
            <label>
                <input type="radio" name="hatali_adim" value="${adimNo}"> ${adimNo}. Adım
            </label>
        `;
    });

    // Alanları sıfırla
    document.getElementById('dogru-islem-input').value = "";
    document.getElementById('dogru-sonuc-input').value = "";
    const bildirim = document.getElementById('geri-bildirim');
    bildirim.style.display = "none";
    bildirim.className = "geri-bildirim";
    
    document.getElementById('gonder-btn').style.display = "inline-block";
    document.getElementById('sonraki-btn').style.display = "none";

    sureyiBaslat();
}

function dogrulaVeGonder() {
    const soru = sorular[aktifSoruIndex];
    const secilenRadio = document.querySelector('input[name="hatali_adim"]:checked');
    const girilenIslem = document.getElementById('dogru-islem-input').value.trim();
    const girilenSonuc = Number(document.getElementById('dogru-sonuc-input').value.trim());
    const bildirim = document.getElementById('geri-bildirim');

    if (!secilenRadio) {
        alert("Lütfen önce hatalı olduğunu düşündüğün adımı seç!");
        return;
    }

    denemeSayisi++;
    const secilenAdim = Number(secilenRadio.value);
    const adimDogruMu = (secilenAdim === soru.hatali_adim_no);
    const sonucDogruMu = (girilenSonuc === soru.beklenen_sonuc);

    bildirim.style.display = "block";

    if (adimDogruMu && sonucDogruMu) {
        clearInterval(zamanlayici);
        bildirim.className = "geri-bildirim basarili";
        bildirim.innerHTML = `🎉 <strong>Tebrikler!</strong> Hatalı adımı ve doğru sonucu (${soru.beklenen_sonuc}) başarıyla buldun!`;
        
        document.getElementById('gonder-btn').style.display = "none";
        document.getElementById('sonraki-btn').style.display = "inline-block";

        raporVerileri.push({
            baslik: soru.baslik,
            kategori: soru.kategori,
            sure: saniye,
            deneme: denemeSayisi,
            hatalar: hataKayitlari.length > 0 ? hataKayitlari.join(", ") : "Tek seferde hatasız çözüm"
        });
    } else {
        bildirim.className = "geri-bildirim hatali";
        let hataMesaji = "❌ <strong>Tekrar Dene!</strong> ";
        
        if (!adimDogruMu) {
            hataMesaji += "Seçtiğin adımda hata yok. ";
            hataKayitlari.push("Yanlış adım tespiti");
        } else if (!sonucDogruMu) {
            hataMesaji += "Hatalı adımı doğru buldun ancak düzelttiğin işlem sonucu yanlış. ";
            hataKayitlari.push("İşlem/sonuç hatası");
        }
        
        hataMesaji += `<br>💡 <strong>İpucu:</strong> ${soru.ipucu}`;
        bildirim.innerHTML = hataMesaji;
    }
}

function sonrakiSoruyaGec() {
    aktifSoruIndex++;
    if (aktifSoruIndex < sorular.length) {
        soruyuEkranaBas(aktifSoruIndex);
    } else {
        raporuGoster();
    }
}

function raporuGoster() {
    clearInterval(zamanlayici);
    document.getElementById('oyun-alani').style.display = "none";
    document.querySelector('.ust-bilgi').style.display = "none";
    
    const raporAlani = document.getElementById('rapor-alani');
    const raporGovdesi = document.getElementById('rapor-govdesi');
    raporAlani.style.display = "block";
    raporGovdesi.innerHTML = "";

    raporVerileri.forEach(veri => {
        raporGovdesi.innerHTML += `
            <tr>
                <td>${veri.baslik}</td>
                <td>${veri.kategori}</td>
                <td>${veri.sure} sn</td>
                <td>${veri.deneme} deneme (${veri.hatalar})</td>
            </tr>
        `;
    });
}

window.onload = sorulariGetir;