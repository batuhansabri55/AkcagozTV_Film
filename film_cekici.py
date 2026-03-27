import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

VOD_KAYNAKLAR = [
    "https://tinyurl.com/2ys5fe3h",
    "https://tinyurl.com/2ao2rans",
    "https://tinyurl.com/power-cinema"
]

def karakter_onari(metin):
    """Grup isimlerindeki ve başlıklardaki tüm bozuklukları tamir eder."""
    # En sık rastlanan bozuk kombinasyonlar (image_f4e6c0 baz alınmıştır)
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ",
        "вн": "", "вн©": "Ç", "вн–": "Ö", "вн‡": "İ",
        "внї": "ü", "вн”": "ö", "вн№": "ş", "внљ": "Ş",
        "внћ": "ğ", "внќ": "Ğ", "вн\x9f": "ş", "вн±": "ı"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    
    # Kalan garip sembolleri ve çift tırnak hatalarını temizle
    metin = metin.replace('вн', '').replace('Гў', 'â')
    return metin

def main():
    print("🚀 VOD Avcısı 13.0 (Karakter Fix) Başlatıldı...")
    final_list = []

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                # İçeriği en güvenli şekilde utf-8 olarak oku
                raw_text = r.content.decode('utf-8', errors='ignore')
                lines = raw_text.splitlines()
                
                temp_inf = ""
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line: continue
                    
                    if clean_line.startswith("#EXTINF:"):
                        # Önce tüm satırı onar
                        inf = karakter_onari(clean_line)
                        # Grup ismini düzenle ve 'SİNEMA |' ekle
                        if 'group-title="' in inf:
                            inf = re.sub(r'group-title="(.*?)"', r'group-title="SİNEMA | \1"', inf)
                            # Grup isminin içindeki bozuklukları tekrar temizle (garanti olsun)
                            inf = karakter_onari(inf)
                        else:
                            inf = inf.replace("#EXTINF:-1", '#EXTINF:-1 group-title="SİNEMA ARŞİVİ"')
                        
                        # TiviMate için video tipini zorla
                        if 'type="video"' not in inf:
                            inf = inf.replace("#EXTINF:", '#EXTINF:-1 type="video"')
                        temp_inf = inf
                    
                    elif clean_line.startswith("http"):
                        # Linkin sonuna senin meşhur ekini yapıştır
                        base_link = clean_line.split('#')[0].rstrip('/')
                        forced_link = f"{base_link}/#/movies/"
                        
                        if temp_inf:
                            final_list.append(f"{temp_inf}\n{forced_link}")
        except Exception as e:
            print(f"❌ Hata: {str(e)}")

    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        # Benzersiz içerikler
        for item in list(dict.fromkeys(final_list)):
            f.write(item + "\n")

    print(f"✅ İşlem Tamam! {len(final_list)} içerik onarıldı.")

if __name__ == "__main__":
    main()
