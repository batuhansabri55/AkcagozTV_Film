import requests

def power_cinema_ekle():
    # Artık çalışan gerçek linkimiz
    GERCEK_LINK = "https://tinyurl.com/power-cinema"
    dosya_adi = "tr.m3u"

    try:
        # 1. Power Cinema'dan güncel filmleri çek
        print("Filmler çekiliyor...")
        r = requests.get(GERCEK_LINK, timeout=15)
        r.raise_for_status() # Bağlantı hatası varsa burada durur, dosyayı bozmaz
        
        yeni_filmler = r.text

        # 2. Dosyayı 'a' (append) yani EKLEME modunda açıyoruz.
        # Bu mod dosyanın başındaki mevcut kategorileri SİLMEZ, sadece sonuna yazar.
        with open(dosya_adi, "a", encoding="utf-8") as f:
            # Önce bir alt satıra geç ki eski filmlerle birbirine girmesin
            f.write("\n\n# --- POWER CINEMA YENI EKLENENLER ---\n")
            f.write(yeni_filmler)
            
        print("İşlem başarılı! Mevcut film kategorilerin korundu, yeniler sona eklendi.")

    except Exception as e:
        # Bir hata olursa (internet koparsa vs.) mevcut dosyana hiç dokunmaz
        print(f"Hata oluştu ama mevcut listen güvende: {e}")

if __name__ == "__main__":
    power_cinema_ekle()
