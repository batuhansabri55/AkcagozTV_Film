import requests
import re
import json

# Usta, Python'da yorum satırı '#' ile başlar.
# Kaynak: https://beytepe.tk//sey/back/v2/parser/parsers.js

def parser(url, lang=1, sub="", headers=None):
    try:
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            }
        
        # URL temizleme
        url = url.replace("?wfilmizle", "")

        # --- YÖNLENDİRİCİ (ROUTER) ---
        if "atv.com.tr" in url and "canli-yayin" not in url:
            return atv_parser(url, headers)
        elif "dizilla" in url:
            return dizilla_parser(url, lang, headers)
        elif "dizimia" in url:
            return dizimia_parser(url, lang, headers)
        elif "diziwatch" in url:
            return diziwatch_parser(url, lang, headers)
        elif "filmmakinesi" in url or "filmmodu" in url or "720pizle" in url:
            # Diğer desteklenen siteler için genel iframe çekici
            return genel_iframe_parser(url, headers)
        else:
            # Bilinmeyen kaynaklarda direkt linki döndürür (Görsel 3'teki gibi)
            print(f"Bilinmeyen Kaynak: {url}")
            return url

    except Exception as e:
        print(f"Hata: {str(e)}")
        return None

def atv_parser(url, headers):
    try:
        res = requests.get(url, headers=headers).text
        m = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', res)
        if m:
            return m.group(1)
    except:
        return None

def dizilla_parser(url, lang, headers):
    try:
        res = requests.get(url, headers=headers).text
        iframe = re.search(r'<iframe.*?src="(.*?)"', res).group(1)
        return "https:" + iframe if iframe.startswith("//") else iframe
    except:
        return None

def dizimia_parser(url, lang, headers):
    try:
        res = requests.get(url, headers=headers).text
        iframe = re.search(r'<iframe.*?src="(.*?)"', res).group(1)
        return "https:" + iframe if iframe.startswith("//") else iframe
    except:
        return None

def diziwatch_parser(url, lang, headers):
    try:
        res = requests.get(url, headers=headers).text
        if "playlist" in res:
            json_url = re.search(r"'/playlist/(.*?).json';", res).group(1)
            final_res = requests.get(f"https://videoseyred.in/playlist/{json_url}.json", headers=headers).json()
            return final_res[0]['sources'][0]['file']
    except:
        return None

def genel_iframe_parser(url, headers):
    try:
        res = requests.get(url, headers=headers).text
        iframe = re.search(r'<iframe.*?src="(.*?)"', res).group(1)
        return iframe
    except:
        return None

# --- ANA ÇALIŞTIRICI ---
if __name__ == "__main__":
    # Test linki (Görseldeki TV 8 linki gibi)
    test_url = "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web"
    sonuc = parser(test_url)
    print(f"Bulunan Link: {sonuc}")
