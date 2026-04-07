import requests
import re
import os

# --- USTA BURASI SENİN LİSTEN (ROUTER MANTIĞI) ---
def parser_merkezi(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://google.com"
    }
    
    try:
        # Eğer link zaten m3u8 ise direkt geç
        if ".m3u8" in url:
            return url

        # 1. SİTE TESPİTİ VE ÖZEL ÇEKİCİLER
        if "filmmakinesi" in url:
            return iframe_ayikla(url, headers)
        elif "filmmodu" in url:
            return iframe_ayikla(url, headers)
        elif "setfilmizle" in url:
            return iframe_ayikla(url, headers)
        elif "dizilla" in url:
            return dizilla_cek(url, headers)
        elif "dizimom" in url:
            return iframe_ayikla(url, headers)
        elif "filmekseni" in url:
            return iframe_ayikla(url, headers)
        elif "720pizle" in url:
            return iframe_ayikla(url, headers)
        elif "filmkovasi" in url:
            return iframe_ayikla(url, headers)
        elif "filmatek" in url:
            return iframe_ayikla(url, headers)
        elif "siyahfilmizle" in url:
            return iframe_ayikla(url, headers)
        elif "atv.com.tr" in url:
            return atv_cek(url, headers)
        
        return url # Tanımlı değilse bozma
    except:
        return url

# --- SİTELERİN İÇİNDEN VİDEO KOPARAN FONKSİYONLAR ---

def iframe_ayikla(url, headers):
    """Genel film siteleri için iframe içindeki asıl kaynağı bulur."""
    try:
        html = requests.get(url, headers=headers, timeout=10).text
        iframe = re.search(r'<iframe.*?src="(.*?)"', html)
        if iframe:
            src = iframe.group(1)
            return "https:" + src if src.startswith("//") else src
        return url
    except:
        return url

def atv_cek(url, headers):
    """ATV'nin gizli video linkini yakalar."""
    try:
        html = requests.get(url, headers=headers, timeout=10).text
        match = re.search(r'url:\s*"(https://videojs.tmgrup.com.tr/.*?)"', html)
        return match.group(1) if match else url
    except:
        return url

def dizilla_cek(url, headers):
    """Dizilla için kaynak ayıklar."""
    try:
        html = requests.get(url, headers=headers, timeout=10).text
        # Player kaynağını ara
        source = re.search(r'source:\s*"(.*?)"', html)
        if source:
            return source.group(1)
        return iframe_ayikla(url, headers)
    except:
        return url

# --- M3U DOSYASINI GÜNCELLEME ---
def listeyi_yenile():
    m3u_yolu = "FilmDizi.m3u"
    if not os.path.exists(m3u_yolu):
        print("Usta FilmDizi.m3u bulunamadı, önce dosyayı oluştur!")
        return

    with open(m3u_yolu, "r", encoding="utf-8") as f:
        satirlar = f.readlines()

    yeni_icerik = []
    for satir in satirlar:
        # Eğer satır bir URL ise ve m3u8 değilse (yani film sitesi linkiyse)
        if satir.startswith("http") and ".m3u8" not in satir:
            print(f"🔄 Link dönüştürülüyor: {satir.strip()}")
            yeni_link = parser_merkezi(satir.strip())
            yeni_icerik.append(yeni_link + "\n")
        else:
            yeni_icerik.append(satir)

    with open(m3u_yolu, "w", encoding="utf-8") as f:
        f.writelines(yeni_icerik)
    print("✅ Tüm film linkleri m3u8 formatına çevrildi!")

if __name__ == "__main__":
    listeyi_yenile()
