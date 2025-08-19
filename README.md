### 1. README.md
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
- [AutoPyloter](https://github.com/AutoPyloter)

## Destek
Sorularınız veya önerileriniz için lütfen [Issues](https://github.com/AutoPyloter/youtube-subtitle-fetcher/issues) bölümünü kullanın.


