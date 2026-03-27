import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

VOD_KAYNAKLAR = [
    "https://tinyurl.com/FanatikplayFilm",
    "https://tinyurl.com/power-cinema"
]

def karakter_onari(metin):
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def main():
    print("🚀 Dizi & Film Avcısı 14.0 (Kategori Birleştirme) Başlatıldı...")
    
    # Kategorileri gruplamak için sözlük kullanıyoruz
    # Yapı: { "SİNEMA | Korku": ["film1_bilgisi", "film2_bilgisi"], ... }
    kategorize_veriler = {}

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                raw_text = r.content.decode('utf-8', errors='ignore')
                lines = raw_text.splitlines()
                
                temp_inf = ""
                for i in range(len(lines)):
                    line = lines[i].strip()
                    if line.startswith("#EXTINF:"):
                        temp_inf = karakter_onari(line)
                    
                    elif line.startswith("http") and temp_inf:
                        m3u_url = line
                        
                        # --- ANALİZ ---
                        is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon)', temp_inf, re.I)
                        
                        # Mevcut group-title'ı çekelim
                        g_match = re.search(r'group-title="([^"]+)"', temp_inf)
                        mevcut_g = g_match.group(1) if g_match else "Genel"
                        
                        if is_series:
                            yeni_kategori = f"DİZİ | {mevcut_g}"
                            link = f"{m3u_url.split('#')[0].rstrip('/')}/#/series/"
                        else:
                            yeni_kategori = f"SİNEMA | {mevcut_g}"
                            link = f"{m3u_url.split('#')[0].rstrip('/')}/#/movies/"
                        
                        # Satırı yeni kategori ismiyle güncelle
                        temp_inf = re.sub(r'group-title="([^"]+)"', f'group-title="{yeni_kategori}"', temp_inf)
                        entry = f"{temp_inf}\n{link}"

                        # Sözlüğe ekle (Kategoriye göre grupla)
                        if yeni_kategori not in kategorize_veriler:
                            kategorize_veriler[yeni_kategori] = set() # Tekrarı önlemek için 'set'
                        
                        kategorize_veriler[yeni_kategori].add(entry)
                        temp_inf = ""

        except Exception as e:
            print(f"❌ Hata ({url}): {str(e)}")

    # --- DOSYAYA YAZMA ---
    toplam_icerik = 0
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        # Kategorileri alfabetik sıraya dizerek yazdırır (Opsiyonel)
        for kategori in sorted(kategorize_veriler.keys()):
            for item in kategorize_veriler[kategori]:
                f.write(item + "\n")
                toplam_icerik += 1

    print(f"✅ İşlem Tamam! {toplam_icerik} içerik kategorilere göre birleştirildi.")

if __name__ == "__main__":
    main()
