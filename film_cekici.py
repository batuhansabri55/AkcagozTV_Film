import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/"  # Bitişik VOD takısı
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

    def tur_ayikla(self, metin):
        # Parantez içindeki ilk kelimeyi yakalar: (Aksiyon-Macera -> Aksiyon)
        match = re.search(r'\((.*?)[-|\)]', metin)
        if match:
            tur = match.group(1).strip().upper()
            # Eğer sayısal bir yıl geldiyse (2024 gibi), bir sonrakine bakmayı dene
            if tur.isdigit() and len(tur) == 4:
                return "GENEL"
            return tur
        return "GENEL"

    def veri_topla(self):
        print("🚀 Kategoriler jilet gibi ayrılıyor...")
        for url in self.kaynaklar:
            try:
                r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
                # M3U içindeki isim ve URL bloklarını yakala
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http[^\s]+)', r.text)
                
                for ad_ham, url_ham in bulunanlar:
                    ad = ad_ham.strip()
                    # URL sonundaki tüm boşlukları söküp takıyı yapıştırıyoruz
                    vod_url = f"{url_ham.strip()}{VOD_TAG}"
                    
                    # Türü ayıkla (Aksiyon, Komedi, Macera vb.)
                    tur = self.tur_ayikla(ad)
                    
                    if tur not in self.kategorize_liste:
                        self.kategorize_liste[tur] = []

                    self.kategorize_liste[tur].append({
                        "ad": ad,
                        "url": vod_url,
                        "logo": "https://via.placeholder.com/300x450?text=" + ad.replace(" ", "+")
                    })
            except Exception as e:
                print(f"❌ Kaynak hatası: {e}")

    def m3u_kaydet(self):
        if not self.kategorize_liste:
            print("🛑 Liste boş!")
            return

        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Türleri alfabetik sırayla dosyaya basıyoruz
            for tur in sorted(self.kategorize_liste.keys()):
                print(f"📦 {tur} kategorisi yazılıyor...")
                for film in self.kategorize_liste[tur]:
                    # TiviMate'in kategoriyi tanıması için group-title jilet gibi olmalı
                    f.write(f'#EXTINF:-1 tvg-logo="{film["logo"]}" group-title="{tur}",{film["ad"]}\n')
                    f.write(f'{film["url"]}\n\n')
        
        print(f"✅ İşlem bitti! {CIKIS_DOSYASI} hazır.")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
