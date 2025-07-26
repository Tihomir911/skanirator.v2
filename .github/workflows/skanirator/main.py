from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("style.kv")

class MainLayout(BoxLayout):
    pass

class SkaniratorApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    SkaniratorApp().run()