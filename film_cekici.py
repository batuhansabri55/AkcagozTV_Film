import requests
import re
import os
import datetime

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

VOD_KAYNAKLAR = [
    "https://tinyurl.com/2ys5fe3h",
    "https://tinyurl.com/2ao2rans",
    "https://tinyurl.com/power-cinema"
]

def karakter_onari(metin):
    """Bozuk karakterleri (Гј, вн vb.) Türkçeleştirir."""
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ",
        "вн": ""
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def main():
    print("🎬 VOD Avcısı 10.0 (Kesin URL Ekleme) Başlatıldı...")
    toplam_icerik = []

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=45)
            if r.status_code == 200:
                # Satır satır parçalayarak linkleri yakalayalım
                lines = r.text.splitlines()
                current_inf = ""
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF:"):
                        # Karakterleri onar ve INF satırını sakla
                        current_inf = karakter_onari(line)
                    elif line.startswith("http"):
                        # --- SENİN SİHİRLİ DOKUNUŞUN BURADA ---
                        # Linkin sonundaki boşlukları at, varsa slash ekle ve etiketi yapıştır
                        link = line
                        if not link.endswith("#/movies/"):
                            link = link.rstrip('/') + "/#/movies/"
                        
                        # INF satırı ile linki birleştirip listeye ekle
                        toplam_icerik.append(f"{current_inf}\n{link}")
        except: pass

    # DOSYAYA YAZMA
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        # Tekrar edenleri sil
        benzersiz = list(dict.fromkeys(toplam_icerik))
        
        for madde in benzersiz:
            # TiviMate'e video olduğunu iyice belirt (type="video")
            if 'type="video"' not in madde:
                madde = madde.replace('#EXTINF:-1', '#EXTINF:-1 type="video"')
            f.write(madde + "\n")

    print(f"🚀 Toplam {len(benzersiz)} link sonuna '#/movies/' eklenerek kaydedildi!")

if __name__ == "__main__":
    main()
