import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

VOD_KAYNAKLAR = [
    "https://tinyurl.com/FanatikplayFilm",
    "https://tinyurl.com/FanatikPlayDizi",
    "https://tinyurl.com/power-cinema"
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
    print("🚀 Akıllı Gruplandırma Sistemi Başlatıldı...")
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
                        base_link = clean_line.split('#')[0].rstrip('/')
                        if base_link in added_urls: continue
                        
                        # --- GRUP TESPİTİ VE AYIRMA ---
                        # Orijinal g-title'ı çekelim
                        match = re.search(r'group-title="(.*?)"', temp_inf)
                        org_group = match.group(1).upper() if match else "GENEL"
                        
                        # Dizi mi Film mi?
                        is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon)', temp_inf, re.I) or "/series/" in clean_line
                        
                        if is_series:
                            # Dizileri günlerine veya türüne göre bırak, başına 'DİZİ |' ekle
                            # Örn: DİZİ | PAZARTESİ, DİZİ | DRAM
                            new_group = f"DİZİ | {org_group}"
                            final_link = f"{base_link}/#/series/"
                        else:
                            # Filmleri türüne göre bırak, başına 'FİLM |' ekle
                            # Örn: FİLM | KORKU, FİLM | MACERA
                            new_group = f"FİLM | {org_group}"
                            final_link = f"{base_link}/#/movies/"
                        
                        # Yeni grubu satıra işle
                        if match:
                            temp_inf = re.sub(r'group-title=".*?"', f'group-title="{new_group}"', temp_inf)
                        else:
                            temp_inf = temp_inf.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{new_group}"')
                        
                        final_list.append(f"{temp_inf}\n{final_link}")
                        added_urls.add(base_link)
                        temp_inf = ""

        except Exception as e:
            print(f"❌ Hata: {str(e)}")

    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        f.write("\n".join(final_list))

    print(f"✅ Tamamlandı! Gruplar jilet gibi ayrıldı.")

if __name__ == "__main__":
    main()
