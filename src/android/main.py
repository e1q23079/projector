from kivy.config import Config
from kivy.app import App

from kivy.uix.label import Label

from kivy.clock import Clock

import io

import threading

from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

import socket

from kivy.resources import resource_add_path

is_processing = True
data = None

def start_client():
    global is_processing,data

    # ポート
    PORT = 5000

    # サーバーソケットの作成とバインド
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(("", PORT))
    print(f"client listening on port {PORT}...")

    while is_processing:
        # データの受信
        data, addr = client.recvfrom(65536)

    # サーバーソケットのクローズ
    client.close()


# Set fixed window size for the application
Config.set("graphics","width","435")
Config.set("graphics","height","245")

# Define the main application class
class ProjectorApp(App):
        def build(self):
            resource_add_path("data")
            self.kivy_img = Image(source="image.png")
            Clock.schedule_interval(self.update_image, 1.0 / 30.0)  # Update at 30 FPS
            return self.kivy_img
        def update_image(self, dt):
            global data
            if data is None:
                return
            buf = io.BytesIO(data)
            core_image = CoreImage(buf, ext="png")
            self.kivy_img.texture = core_image.texture
        def on_stop(self):
            global is_processing
            is_processing = False

# Run the application
if __name__ == "__main__":
    threading.Thread(target=start_client, daemon=True).start()
    ProjectorApp().run()