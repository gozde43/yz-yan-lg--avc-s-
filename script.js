let sorular = [];
let aktifSoruIndex = 0;

async function sorularıGetir() {
    try {
        const response = await fetch('/api/sorular');
        if (!response.ok) throw new Error("Sorular yüklenemedi!");
        sorular = await response.json();
        
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

function soruyuEkranaBas(index) {
    const soru = sorular[index];
    const soruAlani = document.getElementById('soru-alani');
    const adimlarListesi = document.getElementById('adimlar-listesi');
    const adimSecimAlani = document.getElementById('adim-secim-alani');

    soruAlani.innerHTML = `<h3>Soru ${index + 1}:</h3><p><b>${soru.soru_metni}</b></p>`;
    
    adimlarListesi.innerHTML = "";
    adimSecimAlani.innerHTML = "";

    soru.yapay_zeka_cozumu.forEach((adim, i) => {
        adimlarListesi.innerHTML += `<p><b>Adım ${i + 1}:</b> ${adim}</p>`;
        adimSecimAlani.innerHTML += `<label><input type="radio" name="hatali_adim" value="${i}"> Adım ${i + 1}</label><br>`;
    });
}

function dogrulaVeGonder() {
    alert("Cevabınız kontrol ediliyor!");
}

function sonrakiSoruyaGec() {
    aktifSoruIndex++;
    if (aktifSoruIndex < sorular.length) {
        soruyuEkranaBas(aktifSoruIndex);
    } else {
        alert("Tüm soruları tamamladınız!");
    }
}

// Sayfa açıldığında soruları yükle
window.onload = sorularıGetir;