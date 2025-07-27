# main.py
import cv2
import re
import requests
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
from threading import Thread

Builder.load_file("style.kv")

class CameraPreview(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            decoded = pyzbar.decode(frame)
            for obj in decoded:
                data = obj.data.decode('utf-8')
                App.get_running_app().analyze_link(data)
            frame = cv2.flip(frame, 0)
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

class MainLayout(BoxLayout):
    def show_manual_input(self):
        self.ids.menu_box.opacity = 0
        self.ids.link_input_box.opacity = 1

    def show_camera(self):
        self.ids.menu_box.opacity = 0
        self.ids.camera_box.opacity = 1

    def check_link(self):
        url = self.ids.link_input.text.strip()
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

        def _analyze():
            if not re.match(r'^https?://', url):
                self.show_result("❌ Неверный формат ссылки!", error=True)
                return
            try:
                response = requests.get(url, timeout=5)
                if any(word in response.text.lower() for word in ['malware', 'attack', 'phishing', 'virus']):
                    self.show_result(f"⚠️ Обнаружена угроза по ссылке!\n{url}", error=True)
                else:
                    self.show_result(f"✅ Ссылка безопасна:\n{url}", error=False)
            except:
                self.show_result("🚫 Не удалось проверить ссылку!", error=True)

        Thread(target=_analyze).start()

    def show_result(self, message, error=False):
        color = (1, 0, 0, 1) if error else (0, 1, 0, 1)
        popup = Popup(
            title='Результат анализа',
            content=Label(text=message, color=color),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == "__main__":
    SkaniratorApp().run()
