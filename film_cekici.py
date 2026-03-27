import requests
import re
import os

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
    # --- ADIM 1: ESKİ DOSYAYI YERELDE SİL ---
    if os.path.exists(VOD_FILE):
        os.remove(VOD_FILE)
        print(f"🗑️ Eski {VOD_FILE} yerelde silindi, temiz sayfa açılıyor...")

    print("🚀 Film Avcısı Başlatıldı...")
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
                        # Dizileri ayıkla (İstemiyordun ya usta)
                        if any(x in line.upper() for x in ["S01", "S02", "BÖLÜM", "SEZON", "EPISODE"]):
                            temp_inf = ""
                            continue
                        temp_inf = karakter_onari(line)
                    
                    elif line.startswith("http") and temp_inf:
                        # Linkin sonuna #/movies/ ekle
                        link = f"{line.split('#')[0].rstrip('/')}/#/movies/"
                        # Grubu düzelt
                        temp_inf = re.sub(r'group-title="(.*?)"', r'group-title="SİNEMA | \1"', temp_inf)
                        
                        final_list.append(f"{temp_inf}\n{link}")
                        temp_inf = ""

        except Exception as e:
            print(f"❌ Hata ({url}): {str(e)}")

    # --- ADIM 2: DOSYAYI SIFIRDAN OLUŞTUR ---
    # 'w' modu dosyayı açar açmaz içini boşaltır, sonra yenisini yazar.
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        unique_list = list(dict.fromkeys(final_list))
        for item in unique_list:
            f.write(item + "\n")

    print(f"✅ İşlem Tamam! {len(unique_list)} yeni film yüklendi. Eski liste tarih oldu.")

if __name__ == "__main__":
    main()
