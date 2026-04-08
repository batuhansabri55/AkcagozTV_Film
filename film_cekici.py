import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/" # Kesinlikle boşluksuz bitişik
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

class AkcagozFilmBotu:
    def __init__(self):
        self.kategorize_liste = {}
        self.kaynaklar = [
            "https://tinyurl.com/power-cinema",
            "https://tinyurl.com/2bhf2qox",
            "https://tinyurl.com/2ao2rans"
        ]

    def tur_ayikla(self, ad):
        # Parantez içindeki ilk kelimeyi (Aksiyon, Macera, Komedi vb.) cımbızla çeker
        match = re.search(r'\(([^0-9\-|\s\)]+)', ad)
        if match:
            return match.group(1).strip().upper()
        return "DİĞER"

    def veri_topla(self):
        print("🚀 Kategoriler ayrılıyor, lütfen bekle usta...")
        for url in self.kaynaklar:
            try:
                r = requests.get(url, headers=HEADERS, timeout=15)
                # İsim ve URL'yi yakala
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http[^\s]+)', r.text)
                
                for ad_ham, url_ham in bulunanlar:
                    ad = ad_ham.strip()
                    # URL sonundaki boşluğu sil ve takıyı yapıştır
                    vod_url = f"{url_ham.strip()}{VOD_TAG}"
                    # Türü (KOMEDİ, AKSİYON vb.) ayıkla
                    tur = self.tur_ayikla(ad)
                    
                    if tur not in self.kategorize_liste:
                        self.kategorize_liste[tur] = []
                    self.kategorize_liste[tur].append({"ad": ad, "url": vod_url})
            except:
                continue

    def m3u_kaydet(self):
        if not self.kategorize_liste: return
        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Kategorileri bloklar halinde yaz ki TiviMate klasör yapsın
            for tur in sorted(self.kategorize_liste.keys()):
                for film in self.kategorize_liste[tur]:
                    # group-title="{tur}" TiviMate'te klasör ismidir
                    f.write(f'#EXTINF:-1 group-title="{tur}",{film["ad"]}\n')
                    f.write(f'{film["url"]}\n\n')
        print(f"✅ Bitti! {len(self.kategorize_liste)} kategori oluşturuldu.")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
