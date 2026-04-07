import requests, re, os

def parser_merkezi(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        if ".m3u8" in url: return url
        # FULL SİTE LİSTESİ VE AYIKLAYICILAR
        if any(x in url for x in ["filmmakinesi", "filmmodu", "setfilmizle", "dizimom", "filmekseni", "720pizle", "filmkovasi", "filmatek", "siyahfilmizle", "dizilla"]):
            html = requests.get(url, headers=headers, timeout=10).text
            # Iframe içindeki asıl video kaynağını bulur
            iframe = re.search(r'<iframe.*?src="(.*?)"', html)
            if iframe:
                src = iframe.group(1)
                return "https:" + src if src.startswith("//") else src
        elif "atv.com.tr" in url:
            html = requests.get(url, headers=headers, timeout=10).text
            match = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', html)
            return match.group(1) if match else url
        return url
    except: return url

def listeyi_yenile():
    # FilmDizi.m3u dosyasını okur ve içindeki site linklerini m3u8'e çevirir
    if os.path.exists("FilmDizi.m3u"):
        with open("FilmDizi.m3u", "r", encoding="utf-8") as f: satirlar = f.readlines()
        yeni_icerik = [parser_merkezi(s.strip()) + "\n" if s.startswith("http") and ".m3u8" not in s else s for s in satirlar]
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f: f.writelines(yeni_icerik)

if __name__ == "__main__": listeyi_yenile()
