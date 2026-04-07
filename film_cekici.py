import requests
import re
import json

# Usta, Python'da yorum satırı '#' ile olur. '//' kullanırsan sistem çalışmaz.
# Kaynak: https://beytepe.tk//sey/back/v2/parser/parsers.js

def parser(url, lang=1, sub="", headers=None):
    try:
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Referer": url
            }
        
        url = url.replace("?wfilmizle", "")

        # --- YÖNLENDİRİCİLER ---
        if "filmmakinesi" in url:
            return iframe_cekici(url, headers)
        elif "filmmodu" in url:
            return iframe_cekici(url, headers)
        elif "dizilla" in url:
            return dizilla_ozel(url, headers)
        elif "dizimia" in url:
            return iframe_cekici(url, headers)
        elif "diziyou" in url and ".m3u8" not in url:
            return iframe_cekici(url, headers)
        elif "atv.com.tr" in url and "canli-yayin" not in url:
            return atv_ozel(url, headers)
        else:
            # Tanımlı değilse linki olduğu gibi bırak (Panelde görünmesi için)
            return url

    except Exception as e:
        print(f"Hata: {str(e)}")
        return url

def iframe_cekici(url, headers):
    try:
        res = requests.get(url, headers=headers, timeout=10).text
        iframe = re.search(r'<iframe.*?src="(.*?)"', res)
        if iframe:
            src = iframe.group(1)
            return "https:" + src if src.startswith("//") else src
        return url
    except:
        return url

def dizilla_ozel(url, headers):
    try:
        res = requests.get(url, headers=headers, timeout=10).text
        # Dizilla bazen farklı kaynak kullanır, iframe yoksa linki döndür
        iframe = re.search(r'<iframe.*?src="(.*?)"', res)
        return iframe.group(1) if iframe else url
    except:
        return url

def atv_ozel(url, headers):
    try:
        res = requests.get(url, headers=headers, timeout=10).text
        m = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', res)
        return m.group(1) if m else url
    except:
        return url

# --- LİSTEYİ GÜNCELLE VE DOSYAYA YAZ ---
if __name__ == "__main__":
    # Burası senin mevcut m3u oluşturma mantığına bağlanmalı
    # Örnek test:
    print("Film listesi güncelleniyor...")
    test_link = "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web"
    print(f"Sonuç: {parser(test_link)}")
