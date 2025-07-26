import re
import requests
import cv2
from pyzbar import pyzbar
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from threading import Thread

Builder.load_file("style.kv")

class CameraPreview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.image = BoxLayout()
        self.add_widget(self.image)
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
            img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.canvas.clear()
            with self.image.canvas:
                from kivy.graphics import Rectangle
                Rectangle(texture=img_texture, pos=self.pos, size=self.size)

class MainLayout(BoxLayout):
    def manual_input(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        text_input = TextInput(hint_text='Вставьте ссылку', multiline=False, size_hint_y=0.6)
        check_button = Button(text='Проверить', size_hint_y=0.4)
        content.add_widget(text_input)
        content.add_widget(check_button)
        popup = Popup(title='Ручной ввод ссылки', content=content, size_hint=(0.9, 0.4))

        def on_check(_):
            url = text_input.text.strip()
            if url:
                App.get_running_app().analyze_link(url)
                popup.dismiss()

        check_button.bind(on_press=on_check)
        popup.open()

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
                self.show_result("❌ Неверный формат ссылки!")
                return
            try:
                response = requests.get(url, timeout=5)
                if any(word in response.text.lower() for word in ['malware', 'attack', 'phishing', 'virus']):
                    self.show_result(f"❗ В ссылке найдена угроза:
{url}")
                else:
                    self.show_result(f"✅ Ссылка безопасна:
{url}")
            except Exception:
                self.show_result("🚫 Не удалось проверить ссылку!")

        Thread(target=_analyze).start()

    def show_result(self, message):
        popup = Popup(
            title='Результат анализа',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == "__main__":
    SkaniratorApp().run()