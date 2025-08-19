import sys
import threading
from urllib.parse import urlparse, parse_qs
import yt_dlp
import requests
import re
from PySide6.QtCore import QUrl, QObject, Signal, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QMessageBox, QDockWidget, QTextEdit, QLabel, QVBoxLayout, QWidget, QComboBox, QHBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView

class WorkerSignals(QObject):
    """
    Arka plan iş parçacığından (thread) ana GUI iş parçacığına sinyal göndermek için kullanılır.
    """
    subtitle_list_result = Signal(dict)
    subtitle_result = Signal(str)
    progress_update = Signal(str)
    finished = Signal()
    error = Signal(str)

class YouTubeSubtitleFetcher(QMainWindow):
    """
    YouTube altyazı çekme özelliğine sahip bir web tarayıcısı uygulaması.
    PySide6 kütüphanesi kullanılarak geliştirilmiştir.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Altyazı Seçici")
        self.setGeometry(100, 100, 1024, 768)

        self.signals = WorkerSignals()
        self.signals.subtitle_list_result.connect(self.populate_subtitle_languages)
        self.signals.subtitle_result.connect(self.update_subtitle_text)
        self.signals.progress_update.connect(self.update_progress_text)
        self.signals.finished.connect(self.fetching_finished)
        self.signals.error.connect(self.show_error)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.youtube.com"))
        self.setCentralWidget(self.browser)

        self.create_toolbar()
        self.create_subtitle_dock()
        
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.urlChanged.connect(self.on_url_changed)

    def create_toolbar(self):
        """Tarayıcı gezinme ve altyazı çekme butonlarını içeren araç çubuğunu oluşturur."""
        toolbar = QToolBar("Gezinme Çubuğu")
        self.addToolBar(toolbar)

        back_btn = QAction("Geri", self)
        back_btn.triggered.connect(self.browser.back)
        toolbar.addAction(back_btn)

        forward_btn = QAction("İleri", self)
        forward_btn.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_btn)
        
        reload_btn = QAction("Yenile", self)
        reload_btn.triggered.connect(self.browser.reload)
        toolbar.addAction(reload_btn)

        home_btn = QAction("Anasayfa", self)
        home_btn.triggered.connect(self.navigate_home)
        toolbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

    def create_subtitle_dock(self):
        """Altyazıları görüntülemek için sağ tarafta bir kenetlenebilir pencere (dock widget) oluşturur."""
        self.subtitle_dock = QDockWidget("Video Altyazısı", self)
        self.subtitle_dock.setAllowedAreas(Qt.RightDockWidgetArea)

        dock_content = QWidget()
        layout = QVBoxLayout()
        
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("Altyazı Dili:")
        self.lang_label.hide()
        self.lang_combo = QComboBox()
        self.lang_combo.hide()
        self.lang_combo.currentIndexChanged.connect(self.fetch_selected_subtitle)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        self.status_label = QLabel("YouTube videosu açın, mevcut altyazılar yüklenecektir.")
        layout.addWidget(self.status_label)

        self.subtitle_text = QTextEdit()
        self.subtitle_text.setReadOnly(True)
        self.subtitle_text.setStyleSheet("background-color: white; padding: 10px; color: black;")
        layout.addWidget(self.subtitle_text)

        dock_content.setLayout(layout)
        self.subtitle_dock.setWidget(dock_content)
        self.addDockWidget(Qt.RightDockWidgetArea, self.subtitle_dock)
        self.subtitle_dock.show()

    def on_url_changed(self, url):
        """URL değiştiğinde altyazı dillerini çekme işlemini başlatır."""
        video_id = self.get_video_id_from_url(url.toString())
        if video_id:
            self.status_label.setText("Altyazı dilleri aranıyor...")
            self.lang_combo.clear()
            self.lang_label.show()
            self.lang_combo.show()
            threading.Thread(target=self.fetch_subtitle_list_thread, args=(video_id,), daemon=True).start()
        else:
            self.status_label.setText("YouTube videosu açın, mevcut altyazılar yüklenecektir.")
            self.lang_combo.clear()
            self.lang_label.hide()
            self.lang_combo.hide()

    def fetch_subtitle_list_thread(self, video_id):
        """Arka planda altyazı dillerini çeker."""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            ydl_opts = {'skip_download': True, 'quiet': True, 'no_warnings': True}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                subtitles = info.get('subtitles', {})
                auto_subtitles = info.get('automatic_captions', {})

                all_langs = {}
                for lang_code, lang_list in subtitles.items():
                    all_langs[lang_code] = lang_list[0]['name']
                for lang_code, lang_list in auto_subtitles.items():
                    # Check if the language is already in the list from manual subtitles to avoid duplicates
                    if lang_code not in all_langs:
                        all_langs[lang_code] = lang_list[0]['name'] + " (Oto)"
                
                self.signals.subtitle_list_result.emit(all_langs)

        except Exception as e:
            self.signals.error.emit(f"Altyazı dillerini çekme hatası: {str(e)}")
        finally:
            self.signals.finished.emit()

    def populate_subtitle_languages(self, languages):
        """Çekilen altyazı dillerini ComboBox'a ekler."""
        if not languages:
            self.status_label.setText("Bu videoda altyazı bulunamadı.")
            self.lang_combo.hide()
            self.lang_label.hide()
            return
        
        self.lang_combo.clear()
        self.lang_combo.addItem("--- Bir dil seçin ---", "")
        for code, name in languages.items():
            self.lang_combo.addItem(name, code)
        
        self.status_label.setText(f"{len(languages)} adet altyazı dili bulundu.")
        self.lang_combo.show()
        self.lang_label.show()

    def fetch_selected_subtitle(self):
        """Kullanıcının seçtiği dilin altyazısını çeker."""
        lang_code = self.lang_combo.currentData()
        if not lang_code:
            return
        
        self.status_label.setText(f"'{self.lang_combo.currentText()}' altyazıları çekiliyor...")
        self.subtitle_text.setPlainText("")
        
        url = self.browser.url().toString()
        video_id = self.get_video_id_from_url(url)

        if not video_id:
            self.show_error("Geçersiz URL: Video kimliği bulunamadı.")
            return

        threading.Thread(target=self.fetch_subtitle_content_thread, args=(video_id, lang_code,), daemon=True).start()

    def fetch_subtitle_content_thread(self, video_id, lang_code):
        """Arka planda seçilen dilin altyazı içeriğini çeker."""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            ydl_opts = {'writesubtitles': True, 'subtitleslangs': [lang_code], 'skip_download': True, 'quiet': True, 'no_warnings': True}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                # Altyazı dosyalarını manuel ve otomatik altyazılar olarak ayırıyoruz.
                manual_subtitles = info.get('subtitles', {}).get(lang_code, [])
                auto_subtitles = info.get('automatic_captions', {}).get(lang_code, [])

                # Sadece bir adet altyazı dosyasını işlemek için bir URL bulmaya çalışalım.
                subtitle_url = None
                
                # Önce manuel altyazılara bakalım.
                for sub in manual_subtitles:
                    if sub.get('ext') == 'vtt':
                        subtitle_url = sub['url']
                        break
                
                # Manuel altyazı bulunamazsa otomatik altyazılara bakalım.
                if not subtitle_url:
                    for sub in auto_subtitles:
                        if sub.get('ext') == 'vtt':
                            subtitle_url = sub['url']
                            break

                transcript = None
                if subtitle_url:
                    response = requests.get(subtitle_url, timeout=10)
                    if response.status_code == 200:
                        transcript = self.convert_vtt_to_text(response.text)
                
            if transcript:
                self.signals.subtitle_result.emit(transcript)
            else:
                self.signals.error.emit(f"'{lang_code}' dilinde altyazı bulunamadı.")
                
        except Exception as e:
            self.signals.error.emit(f"Altyazı çekme hatası: {str(e)}")
        finally:
            self.signals.finished.emit()

    def navigate_home(self):
        """Anasayfaya (YouTube'a) gider."""
        self.browser.setUrl(QUrl("https://www.youtube.com"))

    def navigate_to_url(self):
        """URL çubuğuna girilen adrese gider."""
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))
        
    def update_url_bar(self, q):
        """Tarayıcıda yüklenen sayfanın URL'sini çubuğa yazar."""
        self.url_bar.setText(q.toString())

    def get_video_id_from_url(self, url):
        """URL'den video ID'sini bulur ve döndürür."""
        parsed_url = urlparse(url)
        
        if parsed_url.netloc in ['www.youtube.com', 'youtube.com'] and parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        
        elif parsed_url.netloc == 'youtu.be':
            return parsed_url.path[1:]
            
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

    def update_progress_text(self, text):
        """İşlem durumu mesajını günceller."""
        self.status_label.setText(text)

    def update_subtitle_text(self, text):
        """Altyazıları metin kutusuna yazar."""
        self.subtitle_text.setPlainText(text)
        self.status_label.setText("Altyazı başarıyla çekildi.")

    def fetching_finished(self):
        """İşlem bittiğinde butonları tekrar etkinleştirir."""
        pass

    def show_error(self, message):
        """Hata mesajını gösterir."""
        self.status_label.setText(f"Hata: {message}")

def main():
    app = QApplication(sys.argv)
    window = YouTubeSubtitleFetcher()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()