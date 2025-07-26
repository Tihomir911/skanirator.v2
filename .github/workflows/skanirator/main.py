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
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from threading import Thread

Builder.load_file("style.kv")


class CameraPreview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        self.image = Widget()
        self.add_widget(self.image)

        self.scan_line_pos = 0
        Clock.schedule_interval(self.update, 1.0 / 30)

        with self.image.canvas:
            self.texture = None
            self.bg = Rectangle(pos=self.pos, size=self.size)
            Color(1, 0, 0, 1)
            self.scan_line = Line(points=[], width=2)
            self.frame_lines = []
            Color(1, 1, 1, 0.3)
            self.mask = Rectangle(pos=self.pos, size=self.size)

        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.mask.pos = self.pos
        self.mask.size = self.size

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
                Rectangle(texture=img_texture, pos=self.pos, size=self.size)
                self.draw_frame_and_line()

    def draw_frame_and_line(self):
        x, y = self.pos
        w, h = self.size
        margin = 60

        fx1, fy1 = x + margin, y + margin
        fx2, fy2 = x + w - margin, y + h - margin

        Color(1, 0, 0, 0.8)
        Line(rectangle=(fx1, fy1, fx2 - fx1, fy2 - fy1), width=2)

        self.scan_line_pos += 3
        if self.scan_line_pos > (fy2 - fy1):
            self.scan_line_pos = 0

        y_line = fy1 + self.scan_line_pos
        Color(0, 1, 0, 0.8)
        Line(points=[fx1, y_line, fx2, y_line], width=2)

        Color(0, 0, 0, 0.5)
        Line(rectangle=(x, y, w, h), width=0)
        Rectangle(pos=(x, y), size=(w, fy1 - y))
        Rectangle(pos=(x, fy2), size=(w, y + h - fy2))
        Rectangle(pos=(x, fy1), size=(fx1 - x, fy2 - fy1))
        Rectangle(pos=(fx2, fy1), size=(x + w - fx2, fy2 - fy1))


class RootWidget(BoxLayout):
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


class QRScannerApp(App):
    def build(self):
        self.analyzed_links = set()
        return RootWidget()

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
                    self.show_result(f"⚠️ Обнаружена угроза по ссылке!\n{url}")
                else:
                    self.show_result(f"✅ Ссылка безопасна:\n{url}")
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
    QRScannerApp().run()
