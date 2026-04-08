import requests

def power_cinema_ekle():
    source_url = "https://www.power.cinema" # Buradaki URL'yi tam linkiyle değiştir usta
    
    try:
        # Mevcut tr.m3u dosyasını oku (Filmlerini ve kategorilerini korumak için)
        with open("tr.m3u", "r", encoding="utf-8") as f:
            mevcut_icerik = f.read()
    except FileNotFoundError:
        mevcut_icerik = "#EXTM3U\n"

    try:
        # Sadece Power Cinema verisini çek
        r = requests.get(source_url, timeout=10)
        if r.status_code == 200:
            yeni_veri = r.text
            
            # Eğer Power Cinema zaten dosyanın içindeyse tekrar ekleme yapma (Çorbaya dönmesin)
            if source_url not in mevcut_icerik:
                with open("tr.m3u", "a", encoding="utf-8") as f:
                    f.write("\n" + yeni_veri)
                print("Power Cinema verisi filmlerin altına eklendi.")
    except Exception as e:
        print(f"Hata oluştu ama mevcut dosyana dokunulmadı: {e}")

if __name__ == "__main__":
    power_cinema_ekle()
