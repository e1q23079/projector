import socket
import cv2
import pyautogui
import numpy as np

# サーバーのホストとポート
HOST = input("Enter server IP address: ")
PORT = 5000

# クライアントソケットの作成
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # フレームのキャプチャ
        frame = pyautogui.screenshot() # 画面全体をキャプチャ
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (320, 240))   # 解像度を320x240にリサイズ

        # フレームのエンコード
        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()
        
        # データの送信
        server.sendto(data, (HOST, PORT))
finally:
    # クライアントソケットのクローズ
    server.close()