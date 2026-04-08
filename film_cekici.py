import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

class AkcagozFilmBotu:
    def __init__(self):
        self.kategorize_liste = {}
        self.kaynaklar = [
            "https://tinyurl.com/power-cinema",
            "https://tinyurl.com/2bhf2qox",
            "https://tinyurl.com/2ao2rans"
        ]

    def tur_bul(self, ad):
        # Parantez içindeki ilk kelimeyi yakalar (Örn: Aksiyon)
        match = re.search(r'\(([^0-9\-|\)]+)', ad)
        if match:
            return match.group(1).strip().upper()
        return "GENEL"

    def veri_topla(self):
        for url in self.kaynaklar:
            try:
                # Timeout'u 10 saniye yaptım ki aksiyon takılmasın
                r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
                r.encoding = 'utf-8'
                # İsim ve URL'yi hızlıca ayıkla
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http[^\s]+)', r.text)
                
                for ad_ham, url_ham in bulunanlar:
                    ad = ad_ham.strip()
                    vod_url = f"{url_ham.strip()}{VOD_TAG}"
                    tur = self.tur_bul(ad)
                    
                    if tur not in self.kategorize_liste:
                        self.kategorize_liste[tur] = []
                    self.kategorize_liste[tur].append({"ad": ad, "url": vod_url})
            except:
                continue

    def m3u_kaydet(self):
        if not self.kategorize_liste: return
        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for tur in sorted(self.kategorize_liste.keys()):
                for film in self.kategorize_liste[tur]:
                    f.write(f'#EXTINF:-1 group-title="{tur}",{film["ad"]}\n')
                    f.write(f'{film["url"]}\n\n')

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
