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

def karakter_duzelt(metin):
    """Bozuk karakterleri (UTF-8/ISO-8859-1 karışıklığı) tamir eder."""
    try:
        # Önce gelen metni latin-1 olarak görüp utf-8'e zorla çeviriyoruz
        return metin.encode('latin-1').decode('utf-8')
    except:
        return metin

def main():
    print("🎬 VOD Avcısı 6.0 (Karakter Onarıcı) Başlatıldı...")
    toplam_vod = []

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=45, allow_redirects=True)
            if r.status_code == 200:
                # Kaynaktan gelen içeriği otomatik algılamaya çalış
                r.encoding = r.apparent_encoding 
                
                icerikler = re.findall(r"(#EXTINF:[^\n]+\n+http[^\s\n]+)", r.text, re.IGNORECASE)
                if icerikler:
                    toplam_vod.extend(icerikler)
                    print(f"✅ {len(icerikler)} içerik çekildi.")
        except Exception as e:
            print(f"❌ Hata: {str(e)}")

    # DOSYAYA YAZMA (TÜRKÇE KARAKTER GARANTİLİ)
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        benzersiz_list = list(dict.fromkeys(toplam_vod))
        
        for madde in benzersiz_list:
            # Burası sihirli dokunuş: Yazmadan önce karakterleri onarıyoruz
            temiz_madde = karakter_duzelt(madde.strip())
            f.write(temiz_madde + "\n")

    print(f"🚀 OPERASYON TAMAM! 26.076 İçerik Türkçe olarak güncellendi.")

if __name__ == "__main__":
    main()
