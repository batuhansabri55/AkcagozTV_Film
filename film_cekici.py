import requests
import re
import os

# Kanal listesi - Buradaki URL'ler parser tarafından işlenip video linkine dönecek
KANALLAR = [
    {"ad": "TV 8 FHD", "url": "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web"},
    {"ad": "ATV FHD", "url": "https://www.atv.com.tr/canli-yayin"},
    {"ad": "Dizilla Test", "url": "https://dizilla.com/yabanci-dizi-izle"} 
]

def video_linki_bul(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://google.com"
    }
    try:
        # Link zaten doğrudan m3u8 ise dokunma
        if ".m3u8" in url:
            return url
        
        # Site içeriğini çek
        response = requests.get(url, headers=headers, timeout=15).text
        
        # 1. ATV için özel regex
        if "atv.com.tr" in url:
            match = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', response)
            if match:
                return match.group(1)
        
        # 2. Genel iframe yakalayıcı (Dizilla ve diğerleri için)
        iframe = re.search(r'<iframe.*?src="(.*?)"', response)
        if iframe:
            iframe_url = iframe.group(1)
            if iframe_url.startswith("//"):
                iframe_url = "https:" + iframe_url
            return iframe_url

        return url # Bulamazsa orijinali kalsın
    except Exception as e:
        print(f"Hata ({url}): {e}")
        return url

def m3u_olustur():
    print("🎬 Video linkleri ayıklanıyor...")
    satirlar = ["#EXTM3U\n"]
    
    for kanal in KANALLAR:
        print(f"🔄 İşleniyor: {kanal['ad']}")
        gercek_link = video_linki_bul(kanal['url'])
        satirlar.append(f'#EXTINF:-1 tvg-name="{kanal["ad"]}", {kanal["ad"]}\n')
        satirlar.append(f'{gercek_link}\n')
    
    with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
        f.writelines(satirlar)
    print("✅ FilmDizi.m3u güncellendi!")

if __name__ == "__main__":
    m3u_olustur()
