```markdown
# YouTube Altyazı Çekici Modülü

Bu Python modülü, YouTube videolarından altyazı bilgilerini çekmek için kullanılır. Hem manuel hem de otomatik altyazıları destekler.

## Özellikler
- YouTube URL'sinden video ID'sini otomatik çıkarır
- Videodaki mevcut altyazı dillerini listeler
- Belirtilen dildeki altyazı metnini çeker
- VTT formatını temiz metne dönüştürür
- Konsol tabanlı demo içerir

## Kurulum
1. Bu depoyu klonlayın:
   ```bash
   git clone https://github.com/kullanici_adiniz/youtube-subtitle-fetcher.git
   cd youtube-subtitle-fetcher
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım
### Modül Olarak Kullanım
```python
from youtube_subtitle_fetcher import YouTubeSubtitleFetcher

# Modülü başlat
fetcher = YouTubeSubtitleFetcher()

# Video URL'sini ayarla
video_url = "https://www.youtube.com/watch?v=VIDEO_ID"
if fetcher.set_video_url(video_url):
    # Mevcut dilleri listele
    languages = fetcher.get_available_languages()
    print("Mevcut diller:", languages)
    
    # Belirli bir dilin altyazısını çek
    subtitle = fetcher.get_subtitle_text("tr")
    print("Altyazı:", subtitle[:100] + "...")
```

### Demo Olarak Çalıştırma
```bash
python youtube_subtitle_fetcher.py
```

## Metotlar
### `set_video_url(url)`
- **Açıklama**: Video URL'sini ayarlar ve video ID'sini çıkarır
- **Parametre**: `url` (str) - YouTube video URL'si
- **Dönüş**: `bool` - URL geçerliyse True, değilse False

### `get_available_languages()`
- **Açıklama**: Videoda mevcut olan altyazı dillerini çeker
- **Dönüş**: `dict` - {dil_kodu: dil_adı} formatında sözlük
- **Örnek**: `{'en': 'English', 'tr': 'Turkish (Oto)'}`

### `get_subtitle_text(language_code)`
- **Açıklama**: Belirtilen dildeki altyazı metnini çeker
- **Parametre**: `language_code` (str) - Dil kodu (örn: 'en', 'tr')
- **Dönüş**: `str` - Altyazı metni veya None (hata durumunda)

## Demo Çıktısı
```
YouTube Altyazı Çekici Demo
========================================
Video URL'si: https://www.youtube.com/watch?v=dQw4w9WgXcQ
✅ Video URL'si başarıyla ayarlandı

Mevcut altyazı dilleri çekiliyor...
✅ 15 adet altyazı dili bulundu:
----------------------------------------
• English (en)
• Turkish (tr)
• German (de) (Oto)
• Spanish (es) (Oto)
...

========================================
Interaktif Demo (Çıkmak için 'q' yazın)
========================================

YouTube URL'si girin: https://www.youtube.com/watch?v=...
Altyazı dilleri çekiliyor...
✅ 8 dil bulundu:
1. Turkish (tr)
2. English (en)
3. German (de) (Oto)
...

Dil numarası seçin: 1
'Turkish' altyazısı çekiliyor...
✅ Altyazı başarıyla çekildi:
----------------------------------------
Bu bir örnek altyazı metnidir.
Videonun içeriği hakkında bilgi verir.
...
----------------------------------------

Dosyaya kaydetmek ister misiniz? (e/h): e
✅ 'VIDEO_ID_tr.txt' dosyasına kaydedildi
```

## Gereksinimler
- Python 3.6+
- yt-dlp
- requests

## Lisans
Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

## Katkıda Bulunma
Katkılarınızı memnuniyetle karşılıyoruz! Lütfen değişiklik yapmadan önce aşağıdaki adımları izleyin:
1. Depoyu fork edin
2. Yeni bir dal oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi yapın ve commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Dalı pushlayın (`git push origin feature/yeni-ozellik`)
5. Bir Pull Request oluşturun

## Yazar
- [Kullanıcı Adınız](https://github.com/kullanici_adiniz)

## Destek
Sorularınız veya önerileriniz için lütfen [Issues](https://github.com/kullanici_adiniz/youtube-subtitle-fetcher/issues) bölümünü kullanın.
```

### 2. requirements.txt
```
yt-dlp
requests
```

### 3. LICENSE
```
MIT License

Copyright (c) 2023 YouTube Altyazı Çekici Modülü

İzni burada verilir, ücretsiz olarak, bu yazılımın ve ilgili belge dosyalarının ("Yazılım") kopyalarını elde eden herkese, Yazılımı kısıtlama olmaksızın kullanma, kopyalama, değiştirme, birleştirme, yayma, alt lisanslama ve/veya satma hakkı verilir, ve Yazılımı sağlanan kişilere izin vermek için, aşağıdaki koşullara tabidir:

Yukarıdaki telif hakkı bildirimi ve bu izin bildirimi, Yazılımın tüm kopyalarında veya önemli bölümlerinde bulunacaktır.

YAZILIM "OLDUĞU GİBİ" SAĞLANIR, HİÇBİR TÜRLÜ TAAHHÜT OLMAKSIZIN, İFADE EDİLEN VEYA İMA EDİLEN HERHANGİ BİR GARANTİ DAHİL OLMAK ÜZERE, TİCARİ ELVERİŞLİLİK, BELİRLİ BİR AMACA UYGUNLUK VE İHLAL ETMEME GARANTİLERİ. HİÇBİR DURUMDA YAZARLAR VEYA TELİF HAKKI SAHİPLERİ, YAZILIMIN KULLANIMINDAN KAYNAKLANAN HERHANGİ BİR TALEP, HASAR VEYA DİĞER SORUMLULUK İÇİN SORUMLU OLMAYACAKTIR, BUNLAR DAHİL OLMAK ÜZERE ANLAŞMA, HAKSIZ FİİL VEYA BAŞKA BİR İŞLEMDEN KAYNAKLANAN VEYA YAZILIMLA İLİŞKİLİ VEYA YAZILIMIN KULLANIMINDAN VEYA BAŞKA İŞLEMLERDEN KAYNAKLANAN.
```

### 4. youtube_subtitle_fetcher.py
```python
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
```

### GitHub Deposu Oluşturma Adımları:

1. GitHub'da yeni depo oluşturun:
   - Repository name: `youtube-subtitle-fetcher`
   - Description: `YouTube videolarından altyazı çekmek için Python modülü`
   - Public/Private seçeneğini belirleyin
   - "Add a README file" seçeneğini işaretleyin
   - "Create repository" butonuna tıklayın

2. Dosyaları yükleyin:
   - Depo ana sayfasında "Add file" > "Upload files" seçeneğini kullanın
   - Yukarıdaki 4 dosyayı (README.md, requirements.txt, LICENSE, youtube_subtitle_fetcher.py) yükleyin
   - Her bir dosya için "Commit changes" butonuna tıklayın

3. Projenizi kullanmak için:
   ```bash
   git clone https://github.com/kullanici_adiniz/youtube-subtitle-fetcher.git
   cd youtube-subtitle-fetcher
   pip install -r requirements.txt
   python youtube_subtitle_fetcher.py
   ```

Bu yapılandırmayla projeniz:
- Açık kaynaklı bir GitHub deposuna sahip olacak
- Türkçe dokümantasyon içerecek
- Kolay kurulum ve kullanım sağlayacak
- MIT lisansı ile paylaşılabilir olacak
- Hem modül olarak hem de demo olarak kullanılabilecek
- Gereksinimler ve kullanım talimatları net bir şekilde belirtilecek