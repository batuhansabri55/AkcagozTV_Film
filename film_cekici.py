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

def turkcelestir(metin):
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def main():
    print("🎬 VOD Avcısı 9.0 (Sihirli Link Modu) Başlatıldı...")
    toplam_icerik = []

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=45)
            if r.status_code == 200:
                # Blokları yakala (Satır satır okuyalım)
                text = r.text
                lines = text.split('\n')
                
                current_inf = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF:"):
                        current_inf = turkcelestir(line)
                    elif line.startswith("http"):
                        # --- SENİN SİHİRLİ DOKUNUŞUN BURADA ---
                        # Linkin sonuna bakıyoruz, eğer zaten yoksa ekliyoruz
                        clean_link = line
                        if not clean_link.endswith("#/movies/"):
                            # Önce bir slash var mı kontrol et, sonra ekle
                            if not clean_link.endswith("/"):
                                clean_link += "/"
                            clean_link += "#/movies/"
                        
                        toplam_icerik.append(f"{current_inf}\n{clean_link}")
        except: pass

    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        # Benzersiz içerikler
        benzersiz = list(dict.fromkeys(toplam_icerik))
        
        for madde in benzersiz:
            # TiviMate'e bunun bir video olduğunu iyice vurgulayalım
            madde = madde.replace('#EXTINF:-1', '#EXTINF:-1 type="video"')
            f.write(madde + "\n")

    print(f"🚀 {len(benzersiz)} linkin sonuna #/movies/ eklendi ve kaydedildi!")

if __name__ == "__main__":
    main()
