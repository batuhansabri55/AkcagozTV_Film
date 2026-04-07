import requests
import re
import json

# Usta, Python'da yorum satırı '#' ile başlar. JS'den kalan '//' işaretleri hata yaptırır.
# Hedef: https://beytepe.tk//sey/back/v2/parser/parsers.js

def parser(url, lang=1, sub="", headers=None):
    try:
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Referer": "https://google.com"
            }
        
        url = url.replace("?wfilmizle", "")

        # --- TÜM SİTE YÖNLENDİRMELERİ (ROUTER) ---
        if "filmmakinesi" in url:
            return generic_iframe_parser(url, headers)
        elif "filmmodu" in url:
            return generic_iframe_parser(url, headers)
        elif "setfilmizle" in url:
            return generic_iframe_parser(url, headers)
        elif "dizilla" in url:
            return dizilla_parser(url, headers)
        elif "dizimom" in url:
            return generic_iframe_parser(url, headers)
        elif "filmekseni" in url:
            return generic_iframe_parser(url, headers)
        elif "720pizle" in url:
            return generic_iframe_parser(url, headers)
        elif "kultfilmler" in url:
            return generic_iframe_parser(url, headers)
        elif "filmkovasi" in url:
            return generic_iframe_parser(url, headers)
        elif "filmatek" in url:
            return generic_iframe_parser(url, headers)
        elif "dizimia" in url:
            return generic_iframe_parser(url, headers)
        elif "diziyou" in url and ".m3u8" not in url:
            return generic_iframe_parser(url, headers)
        elif "siyahfilmizle" in url:
            return generic_iframe_parser(url, headers)
        elif "sinemafilmizle" in url:
            return generic_iframe_parser(url, headers)
        elif "atv.com.tr" in url and "canli-yayin" not in url:
            return atv_parser(url, headers)
        else:
            # Tanımlı değilse linki bozmadan geri döndür (Görsel 3'teki TV8 örneği gibi)
            print(f"Bilinmeyen Kaynak: {url}")
            return url

    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        return url

# --- ÖZEL PARSER FONKSİYONLARI ---

def generic_iframe_parser(url, headers):
    """Çoğu film sitesi için iframe içindeki video linkini bulur."""
    try:
        res = requests.get(url, headers=headers, timeout=10).text
        # Iframe src yakalama (JS mantığının Python hali)
        iframe = re.search(r'<iframe.*?src="(.*?)"', res)
        if iframe:
            src = iframe.group(1)
            return "https:" + src if src.startswith("//") else src
        return url
    except:
        return url

def dizilla_parser(url, headers):
    """Dizilla için özel yapılandırma."""
    try:
        res = requests.get(url, headers=headers, timeout=10).text
        # Player veya iframe bilgisini çek
        match = re.search(r'source:\s*"(.*?)"', res)
        if match:
            return match.group(1)
        return generic_iframe_parser(url, headers)
    except:
        return url

def atv_parser(url, headers):
    """ATV videoları için özel token/url yakalayıcı."""
    try:
        res = requests.get(url, headers=headers, timeout=10).text
        m = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', res)
        if m:
            return m.group(1)
        return url
    except:
        return url

# --- LİSTE GÜNCELLEME TETİKLEYİCİ ---
if __name__ == "__main__":
    # Örnek test kullanımı
    test_urls = [
        "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web",
        "https://www.atv.com.tr/diziler/kurulus-osman/izle"
    ]
    
    for link in test_urls:
        sonuc = parser(link)
        print(f"Giriş: {link}\nBulunan Link: {sonuc}\n{'-'*20}")
