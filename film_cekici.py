import requests
import re
import os

# 1. AYARLAR - Linkleri buraya ekle
KANAL_LISTESI = [
    {"ad": "TV 8 FHD", "url": "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web"},
    {"ad": "ATV FHD", "url": "https://www.atv.com.tr/canli-yayin"},
    {"ad": "Dizilla Test", "url": "https://dizilla.com/test-link"} # Örnek
]

def parser(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Referer": "https://google.com"
    }
    try:
        # Eğer zaten m3u8 ise direkt döndür
        if ".m3u8" in url:
            return url
        
        # Siteye git ve iframe/video ara
        res = requests.get(url, headers=headers, timeout=10).text
        
        # Genel Iframe Yakalayıcı (JS mantığının Python hali)
        iframe = re.search(r'<iframe.*?src="(.*?)"', res)
        if iframe:
            src = iframe.group(1)
            return "https:" + src if src.startswith("//") else src
            
        # ATV Özel Yakalayıcı
        atv_match = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', res)
        if atv_match:
            return atv_match.group(1)
            
        return url
    except:
        return url

def m3u_olustur():
    print("M3U Listesi Hazırlanıyor...")
    icerik = "#EXTM3U\n"
    
    for kanal in KANAL_LISTESI:
        print(f"İşleniyor: {kanal['ad']}")
        final_url = parser(kanal['url'])
        icerik += f'#EXTINF:-1 tvg-name="{kanal["ad"]}", {kanal["ad"]}\n{final_url}\n'
    
    # Dosyaya kaydet
    with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
        f.write(icerik)
    print("FilmDizi.m3u başarıyla güncellendi!")

if __name__ == "__main__":
    m3u_olustur()
