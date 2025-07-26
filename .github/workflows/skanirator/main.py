# === main.py ===
import re
import cv2
import requests
from threading import Thread
from pyzbar import pyzbar
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

Builder.load_file("style.kv")

class CameraWidget(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.scanner_line_y = 0
        Clock.schedule_interval(self.update, 1.0 / 30)

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        decoded = pyzbar.decode(frame)
        for obj in decoded:
            url = obj.data.decode('utf-8')
            App.get_running_app().analyze_link(url)

        frame = cv2.flip(frame, 0)
        buf = frame.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture

class MainLayout(BoxLayout):
    def show_scan(self):
        self.ids.menu_box.opacity = 0
        self.ids.camera_box.opacity = 1

    def show_input(self):
        self.ids.menu_box.opacity = 0
        self.ids.input_box.opacity = 1

    def send_url(self):
        url = self.ids.url_input.text.strip()
        if url:
            App.get_running_app().analyze_link(url)

class SkaniratorApp(App):
    def build(self):
        self.analyzed_links = set()
        return MainLayout()

    def analyze_link(self, url):
        if url in self.analyzed_links:
            return
        self.analyzed_links.add(url)

        def analyze():
            if not re.match(r'^https?://', url):
                self.show_result("❌ Неверный формат ссылки!")
                return
            try:
                r = requests.get(url, timeout=5)
                if any(w in r.text.lower() for w in ["malware", "phishing", "attack", "virus"]):
                    self.show_result(f"[color=#FF0000]⚠️ В ссылке найдена угроза![/color]\n{url}")
                else:
                    self.show_result(f"[color=#00FF00]✅ Ссылка безопасна:[/color]\n{url}")
            except Exception:
                self.show_result("🚫 Не удалось проверить ссылку")

        Thread(target=analyze).start()

    def show_result(self, message):
        popup = Popup(title="Результат", content=Label(text=message, markup=True), size_hint=(0.8, 0.4))
        popup.open()

if __name__ == "__main__":
    SkaniratorApp().run()


