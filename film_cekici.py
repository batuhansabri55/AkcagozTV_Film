import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/" # Kesinlikle boşluksuz
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

    def tur_ayikla(self, ad):
        # Parantez içindeki (Aksiyon-Macera...) yapısını yakalar
        match = re.search(r'\((.*?)\)', ad)
        if match:
            icerik = match.group(1).strip()
            # Tire veya artı işaretine kadar olan ilk kelimeyi (Tür) al
            tur = re.split(r'[-+]', icerik)[0].strip().upper()
            # Eğer yıl denk gelirse (2024 gibi) onu geç, türü bulmaya çalış
            if not tur.isdigit():
                return tur
        return "GENEL"

    def veri_topla(self):
        print("🚀 17.000+ İçerik Türlerine Göre Ayrılıyor...")
        for url in self.kaynaklar:
            try:
                r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
                # İsim ve URL ayıklama (Boşluksuz URL yakalama)
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http[^\s]+)', r.text)
                
                for ad_ham, url_ham in bulunanlar:
                    ad = ad_ham.strip()
                    # URL sonundaki boşluğu sil ve VOD takısını yapıştır
                    vod_url = f"{url_ham.strip()}{VOD_TAG}"
                    
                    # Türü (AKSİYON, KOMEDİ vb.) ayıkla
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
            print("🛑 Veri bulunamadı!")
            return

        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Kategorileri alfabetik bloklar halinde yaz (TiviMate Menüsü İçin)
            for tur in sorted(self.kategorize_liste.keys()):
                for film in self.kategorize_liste[tur]:
                    f.write(f'#EXTINF:-1 tvg-logo="{film["logo"]}" group-title="{tur}",{film["ad"]}\n')
                    f.write(f'{film["url"]}\n\n')
        
        print(f"✅ İşlem bitti! TiviMate için {len(self.kategorize_liste)} kategori oluşturuldu.")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
