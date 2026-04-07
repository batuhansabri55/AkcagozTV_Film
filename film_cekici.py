import requests
import re

# 1. AYARLAR - Kanal listeni buraya ekle
KANAL_LISTESI = [
    {"ad": "TV 8 FHD", "url": "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web"},
    {"ad": "ATV FHD", "url": "https://www.atv.com.tr/canli-yayin"},
    {"ad": "Dizilla Test", "url": "https://dizilla.com/test-link"}
]

def video_bulucu(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://google.com"
    }
    try:
        # Link zaten m3u8 ise direkt döndür
        if ".m3u8" in url:
            return url
        
        # Site içeriğini indir
        response = requests.get(url, headers=headers, timeout=15).text
        
        # --- ATV ÖZEL AYIKLAYICI ---
        if "atv.com.tr" in url:
            match = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', response)
            if match:
                return match.group(1)
        
        # --- GENEL IFRAME YAKALAYICI (Dizilla ve diğerleri için) ---
        iframe = re.search(r'<iframe.*?src="(.*?)"', response)
        if iframe:
            src = iframe.group(1)
            final_src = "https:" + src if src.startswith("//") else src
            return final_src
            
        return url
    except Exception as e:
        print(f"Hata oluştu ({url}): {e}")
        return url

def m3u_yap():
    print("🎬 Liste güncelleniyor...")
    icerik = "#EXTM3U\n"
    
    for kanal in KANAL_LISTESI:
        print(f"🔄 İşleniyor: {kanal['ad']}")
        video_link = video_bulucu(kanal['url'])
        icerik += f'#EXTINF:-1 tvg-name="{kanal["ad"]}", {kanal["ad"]}\n{video_link}\n'
    
    # Dosyayı kaydet
    with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
        f.write(icerik)
    print("✅ İşlem tamamlandı! FilmDizi.m3u güncellendi.")

if __name__ == "__main__":
    m3u_yap()
