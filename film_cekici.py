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
    print("🚀 Dizi & Film Avcısı 14.0 Başlatıldı...")
    final_list = []

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
                        # --- DİZİ Mİ FİLM Mİ ANALİZİ ---
                        # Eğer isimde S01, E01, Bölüm gibi ifadeler varsa DİZİ'dir
                        is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon)', temp_inf, re.I)
                        
                        if is_series:
                            # Dizileri 'DİZİLER' grubuna al ve sonuna /#/series/ ekle
                            temp_inf = re.sub(r'group-title="(.*?)"', r'group-title="DİZİ | \1"', temp_inf)
                            link = f"{m3u_url.split('#')[0].rstrip('/')}/#/series/"
                        else:
                            # Filmleri 'SİNEMA' grubuna al ve sonuna /#/movies/ ekle
                            temp_inf = re.sub(r'group-title="(.*?)"', r'group-title="SİNEMA | \1"', temp_inf)
                            link = f"{m3u_url.split('#')[0].rstrip('/')}/#/movies/"
                        
                        final_list.append(f"{temp_inf}\n{link}")
                        temp_inf = ""

        except Exception as e:
            print(f"❌ Hata ({url}): {str(e)}")

    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        # Tekrarları engelle
        unique_list = list(dict.fromkeys(final_list))
        for item in unique_list:
            f.write(item + "\n")

    print(f"✅ İşlem Tamam! {len(unique_list)} içerik (Film ve Dizi) hazır.")

if __name__ == "__main__":
    main()
