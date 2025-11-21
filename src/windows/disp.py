import socket
import cv2
from mss import mss
import numpy as np
import struct
import time

"""画面キャプチャを指定したIPアドレスに送信する関数

Args:
    ip (str): 送信先のIPアドレス
    width (int): 送信するフレームの幅
    height (int): 送信するフレームの高さ
"""
def disp(ip:str,width:int,height:int):

    # サーバーのホストとポート
    HOST = ip
    PORT = 5000

    # クライアントソケットの作成
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # クライアントへの接続
    client.connect((HOST, PORT))

    try:
        while True:
            # フレームのキャプチャ
            monitor = mss().monitors[1]  # プライマリモニターを選択
            frame = mss().grab(monitor) # 画面全体をキャプチャ
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGRA2BGR)
            frame = cv2.resize(frame, (height, width))   # 解像度をheightxwidthにリサイズ

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

if __name__ == "__main__":
    disp("127.0.0.1", 720, 1280)