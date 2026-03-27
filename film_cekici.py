import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

VOD_KAYNAKLAR = [
    "https://tinyurl.com/FanatikplayFilm",
    "https://tinyurl.com/FanatikPlayDizi",
    "https://tinyurl.com/power-cinema"
]

def karakter_onari(metin):
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ",
        "вн": ""
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def grup_belirle(isim, orijinal_grup):
    isim = isim.upper()
    orijinal_grup = orijinal_grup.upper()
    
    # --- DİZİ GÜNLERİ VE KATEGORİLERİ ---
    if any(x in orijinal_grup or x in isim for x in ["PAZARTESİ", "SALI", "ÇARŞAMBA", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]):
        for gun in ["PAZARTESİ", "SALI", "ÇARŞAMBA", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]:
            if gun in orijinal_grup or gun in isim: return f"DİZİ | {gun}"
        return "DİZİ | GÜNCEL"

    # --- FİLM KATEGORİLERİ ---
    kategoriler = {
        "KORKU": ["KORKU", "HORROR", "GERİLİM", "THRILLER"],
        "MACERA": ["MACERA", "ADVENTURE", "AKSİYON", "ACTION"],
        "KOMEDİ": ["KOMEDİ", "COMEDY"],
        "BİLİM KURGU": ["BİLİM KURGU", "SCI-FI", "FANTASTİK"],
        "ANİMASYON": ["ANİMASYON", "CARTOON", "ÇİZGİ FILM"],
        "BELGESEL": ["BELGESEL", "DOCUMENTARY"],
        "YERLİ": ["YERLİ", "TURKISH"]
    }

    for grup, anahtarlar in kategoriler.items():
        if any(a in orijinal_grup or a in isim for a in anahtarlar):
            return f"FİLM | {grup}"
    
    # Hiçbirine uymuyorsa dizi/film ayrımına göre genel gruba at
    if any(x in isim for x in ["S01", "S02", "BÖLÜM", "SEZON"]):
        return "DİZİ | ARŞİV"
    return "FİLM | ARŞİV"

def main():
    print("🚀 Akıllı Grup Eşleme v19.0 Başlatıldı...")
    final_list = []
    added_urls = set()

    for url in VOD_KAYNAKLAR:
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            if r.status_code == 200:
                raw_text = r.content.decode('utf-8', errors='ignore')
                lines = raw_text.splitlines()
                
                temp_inf = ""
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line: continue
                    
                    if clean_line.startswith("#EXTINF:"):
                        temp_inf = karakter_onari(clean_line)
                    
                    elif clean_line.startswith("http") and temp_inf:
                        base_link = clean_line.split('#')[0].rstrip('/')
                        if base_link in added_urls: continue
                        
                        # Kanal ismini ve varsa orijinal grubu çek
                        name_match = re.search(r', (.*)$', temp_inf)
                        group_match = re.search(r'group-title="(.*?)"', temp_inf)
                        
                        ch_name = name_match.group(1) if name_match else "İsimsiz"
                        old_group = group_match.group(1) if group_match else ""
                        
                        # --- YENİ GRUP ATAMASI ---
                        new_group = grup_belirle(ch_name, old_group)
                        
                        # Link sonu eklemeleri
                        is_series = "DİZİ" in new_group
                        final_link = f"{base_link}/#/series/" if is_series else f"{base_link}/#/movies/"
                        
                        # Satırı güncelle
                        if group_match:
                            temp_inf = re.sub(r'group-title=".*?"', f'group-title="{new_group}"', temp_inf)
                        else:
                            temp_inf = temp_inf.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{new_group}"')
                        
                        final_list.append(f"{temp_inf}\n{final_link}")
                        added_urls.add(base_link)
                        temp_inf = ""
        except: pass

    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n" + "\n".join(final_list))
    print("✅ İşlem bitti usta. Gruplar temizlendi.")

if __name__ == "__main__":
    main()
