import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/" # Boşluksuz VOD takısı
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

class AkcagozFilmBotu:
    def __init__(self):
        self.kategorize_liste = {}
        self.kaynaklar = [
            {"url": "https://tinyurl.com/power-cinema"},
            {"url": "https://tinyurl.com/2bhf2qox"},
            {"url": "https://tinyurl.com/2ao2rans"}
        ]

    def veri_topla(self):
        print("🚀 TiviMate Türlere Göre Gruplandırma Başlatıldı...")
        for kaynak in self.kaynaklar:
            try:
                r = requests.get(kaynak['url'], headers=HEADERS, timeout=25, allow_redirects=True)
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*)', r.text)
                
                for ad_ham, url_ham in bulunanlar:
                    ad = ad_ham.strip()
                    # Linkin sonundaki boşluğu siliyor ve VOD takısını yapıştırıyoruz
                    vod_url = f"{url_ham.strip()}{VOD_TAG}"
                    
                    # Türü ayıkla: Parantez içindeki ilk kelimeyi (Komedi, Macera vb.) alır
                    tur_match = re.search(r'\((.*?)[-)]', ad)
                    tur = tur_match.group(1).split('-')[0].strip().upper() if tur_match else "DİĞER"
                    
                    if tur not in self.kategorize_liste:
                        self.kategorize_liste[tur] = []

                    self.kategorize_liste[tur].append({
                        "ad": ad,
                        "url": vod_url,
                        "logo": "https://via.placeholder.com/300x450?text=" + ad.replace(" ", "+")
                    })
            except Exception as e:
                print(f"❌ Hata: {e}")

    def m3u_kaydet(self):
        if not self.kategorize_liste:
            print("🛑 Liste boş, kayıt yapılmadı!")
            return

        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Kategorileri (KOMEDİ, MACERA vb.) tek tek bloklar halinde yazıyoruz
            for tur, filmler in sorted(self.kategorize_liste.items()):
                print(f"📦 {tur} kategorisi yazılıyor ({len(filmler)} film)...")
                for film in filmler:
                    f.write(f'#EXTINF:-1 tvg-logo="{film["logo"]}" group-title="{tur}",{film["ad"]}\n')
                    f.write(f'{film["url"]}\n\n')
        
        print(f"✅ Bitti! {CIKIS_DOSYASI} artık tam kategorili.")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
