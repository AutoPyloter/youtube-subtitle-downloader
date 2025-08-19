import re
from urllib.parse import urlparse, parse_qs
import yt_dlp
import requests

class YouTubeSubtitleFetcher:
    """
    YouTube videolarından altyazı bilgilerini çekmek için kullanılan modül.
    
    Özellikler:
    - YouTube URL'sinden video ID'sini çıkarır
    - Mevcut altyazı dillerini listeler
    - Belirtilen dildeki altyazı metnini çeker
    """
    
    def __init__(self):
        """Modül başlatılırken gerekli değişkenleri hazırlar"""
        self.video_url = None
        self.video_id = None
        self.available_languages = {}
    
    def set_video_url(self, url):
        """
        Video URL'sini ayarlar ve video ID'sini çıkarır
        
        Args:
            url (str): YouTube video URL'si
            
        Returns:
            bool: URL geçerliyse True, değilse False
        """
        self.video_url = url
        self.video_id = self._extract_video_id(url)
        return self.video_id is not None
    
    def _extract_video_id(self, url):
        """
        URL'den video ID'sini çıkarır
        
        Args:
            url (str): YouTube video URL'si
            
        Returns:
            str: Video ID'si veya None (geçersiz URL ise)
        """
        parsed_url = urlparse(url)
        
        # Standart YouTube URL formatı: https://www.youtube.com/watch?v=VIDEO_ID
        if parsed_url.netloc in ['www.youtube.com', 'youtube.com'] and parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        
        # Kısa URL formatı: https://youtu.be/VIDEO_ID
        elif parsed_url.netloc == 'youtu.be':
            return parsed_url.path[1:]
            
        return None
    
    def get_available_languages(self):
        """
        Videoda mevcut olan altyazı dillerini çeker
        
        Returns:
            dict: {dil_kodu: dil_adı} formatında sözlük
                  Örnek: {'en': 'English', 'tr': 'Turkish (Oto)'}
                  Hata durumunda None döner
        """
        if not self.video_id:
            return None
        
        try:
            video_url = f"https://www.youtube.com/watch?v={self.video_id}"
            ydl_opts = {
                'skip_download': True,
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                subtitles = info.get('subtitles', {})
                auto_subtitles = info.get('automatic_captions', {})
                all_langs = {}
                
                # Manuel altyazıları ekle
                for lang_code, lang_list in subtitles.items():
                    all_langs[lang_code] = lang_list[0]['name']
                
                # Otomatik altyazıları ekle (duplicates olmamak şartıyla)
                for lang_code, lang_list in auto_subtitles.items():
                    if lang_code not in all_langs:
                        all_langs[lang_code] = f"{lang_list[0]['name']} (Oto)"
                
                self.available_languages = all_langs
                return all_langs
                
        except Exception as e:
            print(f"Hata: {str(e)}")
            return None
    
    def get_subtitle_text(self, language_code):
        """
        Belirtilen dildeki altyazı metnini çeker
        
        Args:
            language_code (str): Dil kodu (örn: 'en', 'tr')
            
        Returns:
            str: Altyazı metni veya None (hata durumunda)
        """
        if not self.video_id or not language_code:
            return None
        
        try:
            video_url = f"https://www.youtube.com/watch?v={self.video_id}"
            ydl_opts = {
                'writesubtitles': True,
                'subtitleslangs': [language_code],
                'skip_download': True,
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                manual_subtitles = info.get('subtitles', {}).get(language_code, [])
                auto_subtitles = info.get('automatic_captions', {}).get(language_code, [])
                subtitle_url = None
                
                # Önce manuel altyazıları dene
                for sub in manual_subtitles:
                    if sub.get('ext') == 'vtt':
                        subtitle_url = sub['url']
                        break
                
                # Manuel altyazı yoksa otomatik altyazıları dene
                if not subtitle_url:
                    for sub in auto_subtitles:
                        if sub.get('ext') == 'vtt':
                            subtitle_url = sub['url']
                            break
                
                if subtitle_url:
                    response = requests.get(subtitle_url, timeout=10)
                    if response.status_code == 200:
                        return self._convert_vtt_to_text(response.text)
                
                return None
                
        except Exception as e:
            print(f"Hata: {str(e)}")
            return None
    
    def _convert_vtt_to_text(self, vtt_content):
        """
        VTT formatındaki altyazıyı temiz metne dönüştürür
        
        Args:
            vtt_content (str): VTT formatındaki altyazı içeriği
            
        Returns:
            str: Temizlenmiş metin
        """
        lines = vtt_content.split('\n')
        text_lines = []
        previous_line = None
        
        for line in lines:
            # Z damgaları ve boş satırları atla
            if '-->' in line or line.strip() == '' or line.startswith('WEBVTT'):
                continue
            
            # HTML etiketlerini temizle
            line = re.sub(r'<.*?>', '', line)
            line = line.strip()
            
            # Ardışık tekrar eden satırları engelle
            if line and line != previous_line:
                text_lines.append(line)
                previous_line = line
                
        return '\n'.join(text_lines)


def main():
    """
    Modülün kullanımını gösteren demo fonksiyonu
    """
    print("YouTube Altyazı Çekici Demo")
    print("=" * 40)
    
    # Örnek YouTube URL'si (Rick Astley - Never Gonna Give You Up)
    demo_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # 1. Modülü başlat
    fetcher = YouTubeSubtitleFetcher()
    
    # 2. Video URL'sini ayarla
    print(f"Video URL'si: {demo_url}")
    if not fetcher.set_video_url(demo_url):
        print("❌ Geçersiz YouTube URL'si!")
        return
    
    print("✅ Video URL'si başarıyla ayarlandı")
    
    # 3. Mevcut dilleri listele
    print("\nMevcut altyazı dilleri çekiliyor...")
    languages = fetcher.get_available_languages()
    
    if not languages:
        print("❌ Altyazı bulunamadı veya hata oluştu!")
        return
    
    print(f"✅ {len(languages)} adet altyazı dili bulundu:")
    print("-" * 40)
    for code, name in languages.items():
        print(f"• {name} ({code})")
    
    # 4. İlk dili seçerek altyazıyı çek
    if languages:
        first_lang = list(languages.keys())[0]
        print(f"\n'{languages[first_lang]}' altyazısı çekiliyor...")
        
        subtitle_text = fetcher.get_subtitle_text(first_lang)
        
        if subtitle_text:
            print("✅ Altyazı başarıyla çekildi")
            print("-" * 40)
            # İlk 300 karakteri göster
            print(subtitle_text[:300] + "...")
            print("-" * 40)
            print(f"(Toplam {len(subtitle_text)} karakter)")
        else:
            print("❌ Altyazı çekilemedi!")
    
    # 5. Kullanıcıdan URL alarak interaktif demo
    print("\n" + "=" * 40)
    print("Interaktif Demo (Çıkmak için 'q' yazın)")
    print("=" * 40)
    
    while True:
        user_url = input("\nYouTube URL'si girin: ")
        if user_url.lower() == 'q':
            break
        
        if not fetcher.set_video_url(user_url):
            print("❌ Geçersiz URL!")
            continue
        
        print("Altyazı dilleri çekiliyor...")
        user_languages = fetcher.get_available_languages()
        
        if not user_languages:
            print("❌ Altyazı bulunamadı!")
            continue
        
        print(f"✅ {len(user_languages)} dil bulundu:")
        for i, (code, name) in enumerate(user_languages.items(), 1):
            print(f"{i}. {name} ({code})")
        
        lang_choice = input("\nDil numarası seçin: ")
        try:
            lang_index = int(lang_choice) - 1
            lang_codes = list(user_languages.keys())
            if 0 <= lang_index < len(lang_codes):
                selected_lang = lang_codes[lang_index]
                print(f"'{user_languages[selected_lang]}' altyazısı çekiliyor...")
                
                user_subtitle = fetcher.get_subtitle_text(selected_lang)
                
                if user_subtitle:
                    print("✅ Altyazı başarıyla çekildi:")
                    print("-" * 40)
                    print(user_subtitle[:500] + "...")
                    print("-" * 40)
                    
                    save = input("\nDosyaya kaydetmek ister misiniz? (e/h): ")
                    if save.lower() == 'e':
                        filename = f"{fetcher.video_id}_{selected_lang}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(user_subtitle)
                        print(f"✅ '{filename}' dosyasına kaydedildi")
                else:
                    print("❌ Altyazı çekilemedi!")
            else:
                print("❌ Geçersiz seçim!")
        except ValueError:
            print("❌ Lütfen geçerli bir numara girin!")


if __name__ == "__main__":
    main()