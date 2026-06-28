import base64
import requests
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-4o-mini"


class PlantApp(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.image_path = None
        self.chooser = None

        self.title = Label(text="🌿 PlantDoctor AI")
        self.add_widget(self.title)

        self.btn_pick = Button(text="📷 Выбрать фото")
        self.btn_pick.bind(on_press=self.open_gallery)
        self.add_widget(self.btn_pick)

        self.btn_analyze = Button(text="🧠 Анализ")
        self.btn_analyze.bind(on_press=self.analyze)
        self.add_widget(self.btn_analyze)

        self.result = Label(text="")
        self.add_widget(self.result)

    # =====================
    # 📷 ВЫБОР ФОТО
    # =====================
    def open_gallery(self, instance):
        self.result.text = "📷 выбери фото"

        if not self.chooser:
            self.chooser = FileChooserIconView()
            self.chooser.bind(on_selection=self.on_select)
            self.add_widget(self.chooser)

    def on_select(self, chooser, selection):
        if selection:
            self.image_path = selection[0]
            self.result.text = "✅ фото выбрано"

    # =====================
    # 🧠 АНАЛИЗ
    # =====================
    def analyze(self, instance):

        if not API_KEY:
            self.result.text = "❌ нет API ключа"
            return

        if not self.image_path:
            self.result.text = "❌ нет фото"
            return

        try:
            with open(self.image_path, "rb") as f:
                img = base64.b64encode(f.read()).decode()

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Ты агроном. Определи растение, болезнь, причину и лечение."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img}"
                                }
                            }
                        ]
                    }
                ]
            }

            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )

            res = r.json()

            if "choices" in res:
                self.result.text = res["choices"][0]["message"]["content"]
            else:
                self.result.text = str(res)

        except Exception as e:
            self.result.text = str(e)


class PlantDoctorApp(App):
    def build(self):
        return PlantApp()


PlantDoctorApp().run()