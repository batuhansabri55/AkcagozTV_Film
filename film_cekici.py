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
    """Bozuk karakterleri manuel olarak eşleştirir ve düzeltir."""
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ",
        "вн": "", "Гў": "â", "вЂ™": "'"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    
    # Kalan garip UTF-8 kaçışlarını temizlemeye çalış
    try:
        return metin.encode('latin-1').decode('utf-8')
    except:
        return metin

def main():
    print("🎬 VOD Avcısı 7.0 (Ultra Fix) Başlatıldı...")
    toplam_vod = []

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=45)
            if r.status_code == 200:
                # Sayfanın dil kodlamasını zorla doğrula
                r.encoding = 'utf-8' 
                text_content = r.text
                
                # Regex ile blokları çek
                icerikler = re.findall(r"(#EXTINF:[^\n]+\n+http[^\s\n]+)", text_content, re.IGNORECASE)
                toplam_vod.extend(icerikler)
                print(f"✅ {len(icerikler)} içerik alındı.")
        except: pass

    # DOSYAYA YAZMA
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        # Benzersiz içerikler (Duplicate engelleme)
        benzersiz = list(dict.fromkeys(toplam_vod))
        
        for madde in benzersiz:
            temiz_madde = turkcelestir(madde.strip())
            f.write(temiz_madde + "\n")

    print(f"🚀 {len(benzersiz)} içerik Türkçeleştirilerek kaydedildi!")

if __name__ == "__main__":
    main()
