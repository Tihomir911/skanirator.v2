import re
import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from threading import Thread

Builder.load_file("style.kv")


class MainScreen(BoxLayout):
    def show_scanner(self):
        self.ids.main_menu.opacity = 0
        self.ids.link_area.opacity = 0
        self.ids.scanner_area.opacity = 1
        self.ids.result_label.text = ""
        self.ids.result_label.color = (1, 1, 1, 1)

        # Имитируем анимацию сканера
        anim = Animation(opacity=0, duration=0.5) + Animation(opacity=1, duration=0.5)
        anim.repeat = True
        anim.start(self.ids.scanner_area)

        # Запуск фейковой проверки через 3 сек
        Clock.schedule_once(lambda dt: self.analyze_qr("https://example.com"), 3)

    def show_link_input(self):
        self.ids.main_menu.opacity = 0
        self.ids.scanner_area.opacity = 0
        self.ids.link_area.opacity = 1
        self.ids.result_label.text = ""

    def analyze_link(self, url):
        self.ids.result_label.text = "Проверка..."
        self.ids.result_label.color = (1, 1, 1, 1)

        def check():
            if not re.match(r'^https?://', url):
                self.show_result("❌ Неверный формат ссылки", is_danger=True)
                return

            try:
                response = requests.get(url, timeout=5)
                if any(word in response.text.lower() for word in ['malware', 'attack', 'phishing', 'virus']):
                    self.show_result("🚫 В ссылке была найдена угрожающая тебе активность: вирус или фишинг", is_danger=True)
                else:
                    self.show_result("✅ Ссылка чиста, можешь переходить!", is_danger=False)
            except Exception:
                self.show_result("❌ Не удалось проверить ссылку", is_danger=True)

        Thread(target=check).start()

    def analyze_qr(self, url):
        self.analyze_link(url)

    def show_result(self, msg, is_danger=False):
        self.ids.result_label.text = msg
        self.ids.result_label.color = (1, 0, 0, 1) if is_danger else (0, 1, 0, 1)


class SkaniratorApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    SkaniratorApp().run()

