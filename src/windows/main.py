import socket
import cv2
import pyautogui
import numpy as np
import struct

# サーバーのホストとポート
HOST = input("Enter server IP address: ")
PORT = 5000

# クライアントソケットの作成
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# クライアントへの接続
client.connect((HOST, PORT))

try:
    while True:
        # フレームのキャプチャ
        frame = pyautogui.screenshot() # 画面全体をキャプチャ
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        # frame = cv2.resize(frame, (320, 240))   # 解像度を320x240にリサイズ

        # フレームのエンコード
        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()
        
        # データの送信
        size = len(data) # フレームサイズ
        client.sendall(struct.pack(">I", size))  # フレームサイズを送信
        client.sendall(data)  # フレームデータを送信
finally:
    # クライアントソケットのクローズ
    client.close()