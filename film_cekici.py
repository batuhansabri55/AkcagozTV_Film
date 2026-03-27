import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

VOD_KAYNAKLAR = [
    "https://tinyurl.com/FanatikplayFilm", # 17.000+ Film
    "https://tinyurl.com/FanatikPlayDizi", # Diziler
    "https://tinyurl.com/power-cinema"     # Yedek
]

def karakter_onari(metin):
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
    print("🚀 Link Sonu Düzenleme İşlemi Başladı...")
    final_list = []
    added_urls = set()

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                raw_text = r.content.decode('utf-8', errors='ignore')
                lines = raw_text.splitlines()
                
                temp_inf = ""
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line: continue
                    
                    if clean_line.startswith("#EXTINF:"):
                        temp_inf = karakter_onari(clean_line)
                    
                    elif clean_line.startswith("http") and temp_inf:
                        # Linkin saf halini al
                        base_link = clean_line.split('#')[0].rstrip('/')
                        
                        if base_link in added_urls: continue
                        
                        # --- DİZİ Mİ FİLM Mİ KONTROLÜ ---
                        is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon|Episode)', temp_inf, re.I) or "/series/" in clean_line
                        
                        if is_series:
                            # Dizi Formatı: Linkin sonuna #/series/ ekle
                            temp_inf = re.sub(r'group-title="(.*?)"', r'group-title="DİZİLER"', temp_inf)
                            final_link = f"{base_link}/#/series/"
                        else:
                            # Film Formatı: Linkin sonuna #/movies/ ekle
                            temp_inf = re.sub(r'group-title="(.*?)"', r'group-title="SİNEMALAR"', temp_inf)
                            final_link = f"{base_link}/#/movies/"
                        
                        final_list.append(f"{temp_inf}\n{final_link}")
                        added_urls.add(base_link)
                        temp_inf = ""

        except Exception as e:
            print(f"❌ Hata: {str(e)}")

    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        f.write("\n".join(final_list))

    print(f"✅ Tamamlandı! {len(final_list)} içerik linki güncellendi.")

if __name__ == "__main__":
    main()
