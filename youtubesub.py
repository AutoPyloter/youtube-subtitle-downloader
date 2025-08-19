import sys
import re
from urllib.parse import urlparse, parse_qs
import yt_dlp
import requests

class YouTubeSubtitleModel:
    """
    YouTube videolarından altyazı çekmek için kullanılan model sınıfı.
    Form arayüzü olmadan doğrudan konsoldan çalışır.
    """
    def __init__(self):
        self.video_url = None
        self.video_id = None
        self.available_languages = {}
    
    def set_video_url(self, url):
        """Video URL'sini ayarlar ve video ID'sini çıkarır."""
        self.video_url = url
        self.video_id = self.get_video_id_from_url(url)
        return self.video_id is not None
    
    def get_video_id_from_url(self, url):
        """URL'den video ID'sini bulur ve döndürür."""
        parsed_url = urlparse(url)
        
        if parsed_url.netloc in ['www.youtube.com', 'youtube.com'] and parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        
        elif parsed_url.netloc == 'youtu.be':
            return parsed_url.path[1:]
            
        return None
    
    def fetch_available_languages(self):
        """Mevcut altyazı dillerini çeker ve sözlük olarak döndürür."""
        if not self.video_id:
            return False
        
        try:
            video_url = f"https://www.youtube.com/watch?v={self.video_id}"
            ydl_opts = {'skip_download': True, 'quiet': True, 'no_warnings': True}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                subtitles = info.get('subtitles', {})
                auto_subtitles = info.get('automatic_captions', {})
                all_langs = {}
                
                for lang_code, lang_list in subtitles.items():
                    all_langs[lang_code] = lang_list[0]['name']
                
                for lang_code, lang_list in auto_subtitles.items():
                    if lang_code not in all_langs:
                        all_langs[lang_code] = lang_list[0]['name'] + " (Oto)"
                
                self.available_languages = all_langs
                return True
                
        except Exception as e:
            print(f"Altyazı dillerini çekme hatası: {str(e)}")
            return False
    
    def get_subtitle(self, lang_code):
        """Belirtilen dil koduna göre altyazı metnini çeker ve döndürür."""
        if not self.video_id or not lang_code:
            return None
        
        try:
            video_url = f"https://www.youtube.com/watch?v={self.video_id}"
            ydl_opts = {'writesubtitles': True, 'subtitleslangs': [lang_code], 
                        'skip_download': True, 'quiet': True, 'no_warnings': True}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                manual_subtitles = info.get('subtitles', {}).get(lang_code, [])
                auto_subtitles = info.get('automatic_captions', {}).get(lang_code, [])
                subtitle_url = None
                
                # Önce manuel altyazılara bak
                for sub in manual_subtitles:
                    if sub.get('ext') == 'vtt':
                        subtitle_url = sub['url']
                        break
                
                # Manuel altyazı yoksa otomatik altyazılara bak
                if not subtitle_url:
                    for sub in auto_subtitles:
                        if sub.get('ext') == 'vtt':
                            subtitle_url = sub['url']
                            break
                
                if subtitle_url:
                    response = requests.get(subtitle_url, timeout=10)
                    if response.status_code == 200:
                        return self.convert_vtt_to_text(response.text)
                
                return None
                
        except Exception as e:
            print(f"Altyazı çekme hatası: {str(e)}")
            return None
    
    def convert_vtt_to_text(self, vtt_content):
        """VTT formatını temiz metne dönüştürür ve ardışık tekrarları filtreler."""
        lines = vtt_content.split('\n')
        text_lines = []
        previous_line = None
        
        for line in lines:
            if '-->' in line or line.strip() == '' or line.startswith('WEBVTT'):
                continue
            line = re.sub(r'<.*?>', '', line)
            line = line.strip()
            
            # Aynı satır ardışık olarak geliyorsa, eklemiyoruz
            if line and line != previous_line:
                text_lines.append(line)
                previous_line = line
                
        return '\n'.join(text_lines)
    
    def list_languages(self):
        """Mevcut dilleri kullanıcıya listeler."""
        if not self.available_languages:
            print("Mevcut altyazı dili bulunamadı.")
            return False
        
        print("\nMevcut Altyazı Dilleri:")
        print("-" * 30)
        for i, (code, name) in enumerate(self.available_languages.items(), 1):
            print(f"{i}. {name} ({code})")
        
        return True

def main():
    print("YouTube Altyazı Çekici")
    print("=" * 30)
    
    model = YouTubeSubtitleModel()
    
    # Kullanıcıdan video URL'sini al
    while True:
        video_url = input("\nYouTube video URL'sini girin (çıkmak için 'q'): ")
        if video_url.lower() == 'q':
            sys.exit(0)
        
        if model.set_video_url(video_url):
            break
        print("Geçersiz YouTube URL'si. Lütfen tekrar deneyin.")
    
    # Mevcut dilleri çek
    print("Altyazı dilleri çekiliyor...")
    if not model.fetch_available_languages():
        print("Altyazı dilleri çekilemedi. Lütfen URL'yi kontrol edin.")
        return
    
    # Dilleri listele
    if not model.list_languages():
        return
    
    # Kullanıcıdan dil seçimi al
    while True:
        lang_choice = input("\nİstediğiniz dilin numarasını girin (çıkmak için 'q'): ")
        if lang_choice.lower() == 'q':
            sys.exit(0)
        
        try:
            lang_index = int(lang_choice) - 1
            lang_codes = list(model.available_languages.keys())
            if 0 <= lang_index < len(lang_codes):
                selected_lang = lang_codes[lang_index]
                break
            print("Geçersiz seçim. Lütfen listedeki numaralardan birini girin.")
        except ValueError:
            print("Lütfen geçerli bir numara girin.")
    
    # Seçilen dilin altyazısını çek
    print(f"'{model.available_languages[selected_lang]}' altyazıları çekiliyor...")
    subtitle_text = model.get_subtitle(selected_lang)
    
    if subtitle_text:
        print("\nAltyazı Metni:")
        print("-" * 30)
        print(subtitle_text)
        
        # Kullanıcıya kaydetme seçeneği sun
        save_choice = input("\nAltyazıyı dosyaya kaydetmek ister misiniz? (e/h): ")
        if save_choice.lower() == 'e':
            filename = f"{model.video_id}_{selected_lang}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(subtitle_text)
            print(f"Altyazı '{filename}' dosyasına kaydedildi.")
    else:
        print("Seçilen dilde altyazı bulunamadı veya çekilemedi.")

if __name__ == "__main__":
    main()