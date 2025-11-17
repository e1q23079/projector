import socket
import cv2
import pyautogui
import numpy as np
import struct
import time

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
        frame = cv2.resize(frame, (854, 480))   # 解像度を854x480にリサイズ | 1280x720

        frame = cv2.flip(frame, 0)  # 垂直反転
        # frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=10)  # 明るさ調整

        # フレームのエンコード
        _, buffer = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 30])
        data = buffer.tobytes()
        
        # データの送信
        size = len(data) # フレームサイズ
        client.sendall(struct.pack(">I", size))  # フレームサイズを送信
        client.sendall(data)  # フレームデータを送信
        time.sleep(0.1)  # 約30fpsで送信
        
finally:
    # クライアントソケットのクローズ
    client.close()