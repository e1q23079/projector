from kivy.config import Config
from kivy.app import App

from kivy.uix.label import Label

from kivy.clock import Clock

import io

import threading

from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image

import socket
import struct

from kivy.resources import resource_add_path,resource_find

is_processing = True
data = None

# ポート
PORT = 5000

# 指定サイズのデータを全て受信する関数
def recv_all(sock, size):
    buf = b""
    while len(buf) < size:
        packet = sock.recv(size - len(buf))
        if not packet:
            return None
        buf += packet
    return buf

# クライアントの開始関数
def start_client():
    global is_processing,data

    while is_processing:
        try:

            # サーバーソケットの作成とバインド
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("", PORT))
            server.listen(1)
            client, addr = server.accept()
            client.settimeout(5.0)  # タイムアウトを5秒に設定

            while is_processing:
                # データの受信
                recv_data = recv_all(client, 4) # フレームサイズを受信
                if recv_data is None:
                    data = None
                    break
                size = struct.unpack(">I", recv_data)[0] # フレームサイズを取得
                frame_data = recv_all(client, size) # フレームデータを受信
                if frame_data is None:
                    data = None
                    break
                data = frame_data
        
        except Exception as e:
            data = None

        finally:

            # クライアントソケットのクローズ
            client.close()
            # サーバーソケットのクローズ
            server.close()

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
            resource_add_path("data")
            if data is None:
                self.kivy_img.source = resource_find("image.png")
                self.kivy_img.reload()
                return
            buf = io.BytesIO(data)
            core_image = CoreImage(buf, ext="jpg")
            self.kivy_img.texture = core_image.texture
        def on_stop(self):
            global is_processing
            is_processing = False

# Run the application
if __name__ == "__main__":
    threading.Thread(target=start_client, daemon=True).start()
    ProjectorApp().run()