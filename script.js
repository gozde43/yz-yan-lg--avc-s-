let sorular = {};
let soruKeys = [];
let mevcutsoruIndex = 0;
let ogrenciSonuclari = {}; 

let soruBaslangicZamani = 0;
let timerInterval = null;

async function sorulariGetir() {
    try {
        const response = await fetch('/sorular');
        sorular = await response.json();
        soruKeys = Object.keys(sorular);
        mevcutsoruIndex = 0;
        
        soruKeys.forEach(id => {
            ogrenciSonuclari[id] = { 
                denemeSayisi: 0, 
                sureSaniye: 0, 
                hataTurleri: [] 
            };
        });

        soruYukle();
    } catch (err) {
        console.error("Sorular yüklenemedi:", err);
    }
}

function soruYukle() {
    const currentId = soruKeys[mevcutsoruIndex];
    const soru = sorular[currentId];
    if (!soru) return;

    document.getElementById('soruBaslik').innerText = soru.baslik;
    document.getElementById('soruMetin').innerHTML = soru.metin;

    const adimlarUl = document.getElementById('cozumAdimlari');
    adimlarUl.innerHTML = '';
    soru.yapay_zeka_cozumu.forEach((adim) => {
        const li = document.createElement('li');
        li.innerText = adim;
        adimlarUl.appendChild(li);
    });

    const radioContainer = document.getElementById('adimRadioContainer');
    radioContainer.innerHTML = '';
    
    soru.yapay_zeka_cozumu.forEach((_, index) => {
        const stepNum = index + 1;
        const label = document.createElement('label');
        label.innerHTML = `<input type="radio" name="secilenAdim" value="${stepNum}"> ${stepNum}. Adımda Hata Var`;
        radioContainer.appendChild(label);
    });

    const noErrorLabel = document.createElement('label');
    noErrorLabel.innerHTML = `<input type="radio" name="secilenAdim" value="0"> Hata Yok (Tüm adımlar doğru)`;
    radioContainer.appendChild(noErrorLabel);

    // Girdi kutularını temizle
    document.getElementById('islemInput').value = '';
    document.getElementById('sonucInput').value = '';
    document.getElementById('result-box').style.display = 'none';
    document.getElementById('btnNext').style.display = 'none';

    // Kronometre
    soruBaslangicZamani = Date.now();
    clearInterval(timerInterval);
    let saniyeSayac = 0;
    timerInterval = setInterval(() => {
        saniyeSayac++;
        document.getElementById('timerBadge').innerText = `⏱️ ${saniyeSayac}s`;
        ogrenciSonuclari[currentId].sureSaniye = saniyeSayac;
    }, 1000);
}

async function dogrula() {
    const currentId = soruKeys[mevcutsoruIndex];
    const islemVal = document.getElementById('islemInput').value;
    const sonucVal = document.getElementById('sonucInput').value;
    const resultBox = document.getElementById('result-box');
    const btnNext = document.getElementById('btnNext');

    ogrenciSonuclari[currentId].denemeSayisi++;

    const selectedRadio = document.querySelector('input[name="secilenAdim"]:checked');
    if (!selectedRadio) {
        resultBox.className = 'error';
        resultBox.innerHTML = '⚠️ Lütfen önce yapay zekanın hangi adımda hata yaptığını seç!';
        resultBox.style.display = 'block';
        return;
    }

    const secilenAdimNo = parseInt(selectedRadio.value);

    if (!islemVal.trim() || !sonucVal.trim()) {
        resultBox.className = 'error';
        resultBox.innerHTML = '⚠️ Lütfen hem işlem kutusunu hem de sonuç kutusunu eksiksiz doldur!';
        resultBox.style.display = 'block';
        return;
    }

    try {
        const response = await fetch('/dogrula', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                soru_id: parseInt(currentId), 
                secilen_adim: secilenAdimNo,
                islem_girdisi: islemVal,
                sonuc_girdisi: sonucVal
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            clearInterval(timerInterval);
            resultBox.className = 'success';
            resultBox.innerHTML = '🎉 <strong>' + data.mesaj + '</strong>';
            btnNext.style.display = 'block'; 
        } else {
            resultBox.className = 'error';
            let hataTuru = data.hata_turu || "İşlem Hatası";
            ogrenciSonuclari[currentId].hataTurleri.push(hataTuru);

            let html = '❌ <strong>' + (data.mesaj || data.detail) + '</strong>';
            if (data.ipucu) {
                html += '<div class="hint-box">💡 <strong>İpucu:</strong> ' + data.ipucu + '</div>';
            }
            resultBox.innerHTML = html;
            btnNext.style.display = 'none';
        }
    } catch (err) {
        resultBox.className = 'error';
        resultBox.innerText = 'Bağlantı hatası oluştu!';
    }
    resultBox.style.display = 'block';
}

function sonrakiSoruyaGec() {
    if (mevcutsoruIndex < soruKeys.length - 1) {
        mevcutsoruIndex++;
        soruYukle();
    } else {
        clearInterval(timerInterval);
        document.getElementById('quizContainer').style.display = 'none';
        document.getElementById('analysisCard').style.display = 'block';
        raporuDoldur();
    }
}

function raporuDoldur() {
    const tbody = document.getElementById('reportTbody');
    tbody.innerHTML = '';

    let toplamSure = 0;
    let kusursuzSayisi = 0;
    let toplamHataTuruSayaci = {};

    soruKeys.forEach(id => {
        const soru = sorular[id];
        const sonuc = ogrenciSonuclari[id];
        toplamSure += sonuc.sureSaniye;

        if (sonuc.denemeSayisi === 1) {
            kusursuzSayisi++;
        }

        sonuc.hataTurleri.forEach(hata => {
            toplamHataTuruSayaci[hata] = (toplamHataTuruSayaci[hata] || 0) + 1;
        });

        let durumMetni = "";
        let badgeClass = "";

        if (sonuc.denemeSayisi === 1) {
            durumMetni = "✨ 1. Denemede Kusursuz Çözüm";
            badgeClass = "badge-correct";
        } else {
            let yanlislarStr = sonuc.hataTurleri.join(", ");
            durumMetni = `💡 ${sonuc.denemeSayisi}. Denemede Başarılı (${sonuc.denemeSayisi - 1} hata: ${yanlislarStr})`;
            badgeClass = "badge-retry";
        }

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${soru.baslik}</strong></td>
            <td><span style="color: #555; font-size: 14px;">${soru.kategori || 'Genel'}</span></td>
            <td>⏱️ ${sonuc.sureSaniye} sn</td>
            <td><span class="${badgeClass}">${durumMetni}</span></td>
        `;
        tbody.appendChild(tr);
    });

    const summaryDiv = document.getElementById('profileSummaryContent');
    let profilYorumu = `<h3>🎯 Genel Performans Özetin</h3>`;
    profilYorumu += `<p>Toplam <strong>${soruKeys.length}</strong> soruyu toplam <strong>${toplamSure} saniyede</strong> tamamladın. Soruların <strong>${kusursuzSayisi}</strong> tanesini hiç hata yapmadan ilk denemede çözmeyi başardın!</p>`;
    
    if (Object.keys(toplamHataTuruSayaci).length > 0) {
        profilYorumu += `<p style="margin-top: 8px;">🔍 Yapılan hata dağılımı incelendiğinde en sık karşılaşılan alanlar: <em>`;
        for (let [hata, adet] of Object.entries(toplamHataTuruSayaci)) {
            profilYorumu += `<strong>${hata}</strong> (${adet} kez), `;
        }
        profilYorumu = profilYorumu.slice(0, -2) + `</em>. Bu konuları tekrar etmek problem çözme hızını daha da artıracaktır.</p>`;
    } else {
        profilYorumu += `<p style="margin-top: 8px; color: #166534;">🏆 Harika! Hiç hata yapmadan tüm testi kusursuz tamamladın. Matematiksel muhakeme becerin çok güçlü!</p>`;
    }

    summaryDiv.innerHTML = profilYorumu;
}

sorulariGetir();