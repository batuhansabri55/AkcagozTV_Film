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
    print("🎬 VOD & Canlı Ayrıştırıcı Başlatıldı...")
    toplam_icerik = []

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=45)
            if r.status_code == 200:
                # Blokları yakala
                bloklar = re.findall(r"(#EXTINF:[^\n]+\n+http[^\s\n]+)", r.text, re.IGNORECASE)
                toplam_icerik.extend(bloklar)
        except: pass

    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        benzersiz = list(dict.fromkeys(toplam_icerik))
        
        for madde in benzersiz:
            madde = turkcelestir(madde.strip())
            
            # --- KRİTİK AYIRMA MANTIĞI ---
            # Eğer satırda zaten bir grup varsa onu 'SİNEMA - ' ile güncelle
            # Yoksa direkt 'VOD FİLMLER' grubuna at
            if 'group-title="' in madde:
                # Mevcut grubu bul ve başına SİNEMA ekle (TiviMate ayırabilsin diye)
                madde = re.sub(r'group-title="(.*?)"', r'group-title="SİNEMA | \1"', madde)
            else:
                madde = madde.replace('#EXTINF:', '#EXTINF:-1 group-title="SİNEMA ARŞİVİ",')

            # TiviMate'e "Bu bir videodur, kanal değildir" demesi için etiket ekle
            if 'type="video"' not in madde:
                madde = madde.replace('#EXTINF:-1', '#EXTINF:-1 type="video"')
                
            f.write(madde + "\n")

    print(f"🚀 {len(benzersiz)} içerik 'SİNEMA' etiketleriyle ayrıştırıldı!")

if __name__ == "__main__":
    main()
