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

def karakter_temizle(metin):
    """Görüntülerdeki tüm bozuk UTF-8 çıktılarını pırıl pırıl yapar."""
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ",
        "вн": "", "вн©": "Ç", "вн–": "Ö", "вн‡": "İ",
        "внї": "ü", "вн”": "ö", "вн№": "ş"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def main():
    print("🚀 VOD Avcısı 12.0 (Final Force) Başlatıldı...")
    final_list = []

    for url in VOD_KAYNAKLAR:
        try:
            print(f"📡 Kaynak taranıyor: {url}")
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                # İçeriği ham bayt olarak alıp UTF-8'e zorluyoruz
                raw_text = r.content.decode('utf-8', errors='ignore')
                lines = raw_text.splitlines()
                
                temp_inf = ""
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line: continue
                    
                    if clean_line.startswith("#EXTINF:"):
                        # Karakterleri onar ve grup ekle
                        inf = karakter_temizle(clean_line)
                        if 'group-title="' in inf:
                            inf = re.sub(r'group-title="(.*?)"', r'group-title="SİNEMA | \1"', inf)
                        else:
                            inf = inf.replace("#EXTINF:-1", '#EXTINF:-1 group-title="SİNEMA ARŞİVİ"')
                        temp_inf = inf
                    
                    elif clean_line.startswith("http"):
                        # --- SENİN SİHİRLİ DOKUNUŞUN: ZORLA EKLEME ---
                        # Linkin sonundaki tüm slash ve etiketleri temizle, sonra senin ekini çak
                        temiz_link = clean_line.split('#')[0].rstrip('/')
                        # FORCED URL: Linkin sonuna tam olarak istediğin yapıyı kuruyoruz
                        forced_link = f"{temiz_link}/#/movies/"
                        
                        if temp_inf:
                            final_list.append(f"{temp_inf}\n{forced_link}")
        except Exception as e:
            print(f"❌ Hata: {str(e)}")

    # DOSYAYA YAZMA
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        # Benzersiz içerikler (Duplicate check)
        for item in list(dict.fromkeys(final_list)):
            f.write(item + "\n")

    print(f"✅ OPERASYON BAŞARILI! {len(final_list)} içerik '#/movies/' etiketiyle hazır.")

if __name__ == "__main__":
    main()
