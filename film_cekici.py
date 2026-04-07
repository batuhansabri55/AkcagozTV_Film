import requests
import re
import json
import urllib.parse

# Usta, Python'da yorum satırı '#' ile yapılır, '//' hata verdirir.
# Kaynak: https://beytepe.tk//sey/back/v2/parser/parsers.js

def parser(url, lang=1, sub="", headers=None):
    try:
        if headers is None:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Referer": url
            }

        url = url.replace("?wfilmizle", "")

        # --- ROUTER (YÖNLENDİRİCİ) ---
        if "atv.com.tr" in url and "canli-yayin" not in url:
            return atv_parser(url, headers)
        
        elif "filmmakinesi" in url:
            # Buraya filmmakinesi_cek(url, lang, headers) fonksiyonunu eklemelisin
            pass
            
        elif "filmmodu" in url:
            pass
            
        elif "dizilla" in url:
            return dizilla_parser(url, lang, headers)
            
        elif "dizimom" in url:
            return dizimom_parser(url, lang, headers)
            
        elif "filmekseni" in url:
            pass
            
        elif "720pizle" in url:
            pass
            
        elif "filmatek" in url:
            pass
            
        elif "diziyou" in url and ".m3u8" not in url:
            return diziyou_parser(url, lang, headers)
            
        elif "siyahfilmizle" in url:
            pass
            
        elif "sinemafilmizle" in url:
            pass
            
        else:
            # Eğer listede yoksa direkt linki döndür veya işlem yap
            print(f"Bilinmeyen Kaynak: {url}")
            return url

    except Exception as e:
        print(f"Hata Oluştu: {str(e)}")
        # Hata bildirimini buraya ekleyebiliriz
        return None

def atv_parser(url, headers):
    headers["Referer"] = "http://www.atv.com.tr/"
    try:
        response = requests.get(url, headers=headers).text
        # Regex ile video URL'sini bulma
        match = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', response)
        if match:
            v_url = match.group(1)
            # Token alma işlemleri burada devam eder...
            return v_url
    except:
        return None

def dizilla_parser(url, lang, headers):
    headers["Referer"] = url
    try:
        response = requests.get(url, headers=headers).text
        iframe_src = re.search(r'<iframe.*?src="(.*?)"', response).group(1)
        if not iframe_src.startswith("http"):
            iframe_src = "https:" + iframe_src
        return iframe_src
    except:
        return None

# --- ANA ÇALIŞTIRICI ---
if __name__ == "__main__":
    # Test için bugün verdiğin linklerden birini deneyebilirsin
    test_url = "https://tv8.daioncdn.net/tv8/tv8_1080p.m3u8?app=tv8_web"
    sonuc = parser(test_url)
    print(f"Bulunan Link: {sonuc}")
