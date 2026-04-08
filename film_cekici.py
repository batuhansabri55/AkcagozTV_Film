import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/"  # URL sonuna sıfır boşlukla yapışır
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

class AkcagozFilmBotu:
    def __init__(self):
        self.kategorize_liste = {}
        self.kaynaklar = [
            "https://tinyurl.com/power-cinema",
            "https://tinyurl.com/2bhf2qox",
            "https://tinyurl.com/2ao2rans"
        ]

    def tur_bul(self, ad):
        # Parantez içindeki ilk kelimeyi (Aksiyon, Komedi vb.) yakalar
        match = re.search(r'\((.*?)[-+)]', ad)
        if match:
            tur = match.group(1).strip().upper()
            # Eğer yıl gelirse (2024 gibi), sonrakine bakmak yerine 'GENEL'den kurtarır
            if not (tur.isdigit() and len(tur) == 4):
                return tur
        return "DİĞER"

    def veri_topla(self):
        for url in self.kaynaklar:
            try:
                r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http[^\s]+)', r.text)
                
                for ad_ham, url_ham in bulunanlar:
                    ad = ad_ham.strip()
                    # URL sonundaki boşluğu silip #/movies/ ekliyoruz
                    vod_url = f"{url_ham.strip()}{VOD_TAG}"
                    
                    # Türü (KOMEDİ, MACERA vb.) ayıklıyoruz
                    tur = self.tur_bul(ad)
                    
                    if tur not in self.kategorize_liste:
                        self.kategorize_liste[tur] = []

                    self.kategorize_liste[tur].append({
                        "ad": ad,
                        "url": vod_url,
                        "logo": "https://via.placeholder.com/300x450?text=" + ad.replace(" ", "+")
                    })
            except: pass

    def m3u_kaydet(self):
        if not self.kategorize_liste: return

        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Kategorileri TiviMate'in anlaması için bloklar halinde yazıyoruz
            for tur in sorted(self.kategorize_liste.keys()):
                for film in self.kategorize_liste[tur]:
                    # group-title="{tur}" kısmı klasörleri oluşturur
                    f.write(f'#EXTINF:-1 tvg-logo="{film["logo"]}" group-title="{tur}",{film["ad"]}\n')
                    f.write(f'{film["url"]}\n\n')

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
