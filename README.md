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
   git clone https://github.com/AutoPyloter/youtube-subtitle-fetcher.git
   cd youtube-subtitle-fetcher
   ```
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
##Kullanım
  ###Modül Olarak Kullanım
    ```python
    from youtube_subtitle_fetcher import YouTubeSubtitleFetcher
    # Modülün başlatılması ve temel kullanım örneği

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
  ###Demo Olarak Çalıştırma
    ```bash
    python youtube_subtitle_fetcher.py
    ```
   
