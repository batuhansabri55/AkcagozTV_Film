import requests

def film_listesini_guncelle():
    # Senin ana dosyan, kategorilerin burada güvende
    dosya_adi = "FilmDizi.m3u"
    
    # Eklenecek film listesi (İstediğin o özel formatla)
    eklenecek_filmler = [
        {"isim": "Açlık Oyunları: Alaycı Kuş Bölüm 2", "url": "https://vidmody.com/vs/tt1951266/"},
        # Buraya istediğin kadar ekleme yapabilirsin usta
    ]

    try:
        # 1. Power Cinema'yı zaten çekiyoruz, onu bozmayalım
        power_r = requests.get("https://tinyurl.com/power-cinema", timeout=10)
        power_data = power_r.text if power_r.status_code == 200 else ""

        # 2. Dosyayı 'a' (EKLEME) modunda açıyoruz
        # Bu mod üstteki Macera, Korku, Komedi yazılarını SİLMEZ.
        with open(dosya_adi, "a", encoding="utf-8") as f:
            
            # Power Cinema eklemesi
            f.write("\n\n# --- POWER CINEMA --- \n")
            f.write(power_data)

            # SEYIRTUR / VIDMODY Eklemesi
            f.write("\n\n# --- SEYIRTUR ÖZEL FİLMLER --- \n")
            
            for film in eklenecek_filmler:
                # KRİTİK NOKTA: URL sonuna senin istediğin o eki yapıştırıyoruz
                temiz_url = film["url"].strip()
                if not temiz_url.endswith("/"):
                    temiz_url += "/"
                
                final_url = f"{temiz_url}#/MOVIES/"
                
                f.write(f'#EXTINF:0 tvg-id="tt{film["url"].split("tt")[-1].replace("/", "")}" group-title="SEYIRTUR FILMLER", {film["isim"]}\n')
                f.write(f'{final_url}\n')

        print(f"İşlem başarılı! {dosya_adi} sonuna #/MOVIES/ eklenerek yazıldı.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_listesini_guncelle()
