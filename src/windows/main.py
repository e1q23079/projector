import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import threading
import socket
import cv2
from mss import mss
import numpy as np
import struct
import time
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI認識を有効化

# サーバーのホストとポート
PORT = 5000

# アプリケーションタイトル
APP_TITLE = "Projector App"

# 画質オプションの定義
IMAGE_QUALITIES = [
    {"height":256,"width":144},
    {"height":426,"width":240},
    {"height":640,"width":360},
    {"height":854,"width":480},
    {"height":1280,"width":720},
    {"height":1920,"width":1080}
]

# 画質名を取得
def get_quality_names():
    names = []
    for image_quality in IMAGE_QUALITIES:
        names.append(f"{image_quality['width']}p ({image_quality['width']}x{image_quality['height']})")
    return names

# 状態
connected = False

# 画面キャプチャと送信を行う関数
def disp(client,width:int,height:int):
    global connected
    try:
        while connected:
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
            time.sleep(0.03)  # 約30fpsで送信
    
    except Exception as e:
        messagebox.showerror(APP_TITLE, f"接続が切断されました。\nエラー: {e}")
        button.config(text="接続")
        combox.config(state="readonly")  # コンボボックスを有効化
        connected = False # 接続状態を更新
        
    finally:
        # クライアントソケットのクローズ
        client.close()

# ボタンクリック時の処理
def on_button_click():
    # グローバル変数の使用宣言
    global connected
    # 接続中の場合
    if connected:
        # 切断処理
        button.config(text="接続")
        messagebox.showinfo(APP_TITLE, "切断しました。")
        connected = False # 接続状態を更新
        combox.config(state="readonly")  # コンボボックスを有効化
        return
    # 接続先IPアドレスの入力ダイアログ表示
    input = simpledialog.askstring(APP_TITLE, "接続先のデバイスのIPアドレスを入力してください。")
    # 入力がキャンセルされた場合は処理を中止
    if not input:
        return
    # 選択された画質オプションの取得
    selected_option = combox.current()
    # クライアントソケットの作成
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # クライアントへの接続
    HOST = input
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        messagebox.showerror(APP_TITLE, f"接続に失敗しました。\nエラー: {e}")
        return
    # 画面キャプチャと送信を行うスレッドの開始
    width = IMAGE_QUALITIES[selected_option]["width"]
    height = IMAGE_QUALITIES[selected_option]["height"]
    connected = True # 接続状態を更新
    threading.Thread(target=disp, args=(client,width,height), daemon=True).start()
    # ボタンのテキストを「切断」に変更
    button.config(text="切断")
    # 情報メッセージの表示
    messagebox.showinfo(APP_TITLE, "接続しました。")
    combox.config(state="disabled")  # コンボボックスを無効化

# ウィンドウ終了時の処理
def on_exit():
    ret = messagebox.askokcancel("確認", "本当に終了しますか？")
    if ret:
        app.destroy()

app = tk.Tk()
# ウィンドウの設定
app.title(APP_TITLE)
# ウィンドウサイズの固定
app.geometry("370x90")
# リサイズ不可
app.resizable(False, False)

# コンボボックスの作成
combox = ttk.Combobox(app, values=get_quality_names(),state="readonly")
combox.current(5) # デフォルト選択を1080pに設定
combox.pack(pady=5)

# ボタンの作成
button = ttk.Button(app, text="接続",width=10,command=on_button_click)
button.pack(pady=5)

# ウィンドウ終了時のイベントバインド
app.protocol("WM_DELETE_WINDOW", on_exit)

# メインループの開始
app.mainloop()