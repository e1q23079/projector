from mss import mss
from tkinter import ttk,simpledialog,messagebox
import ctypes
import cv2
import numpy as np
import socket
import struct
import threading
import time
import tkinter as tk

ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI認識を有効化

# サーバーのホストとポート
HOST = None
PORT = 5000

# デフォルトの画面解像度
width = 1920
height = 1080

# 拡大・縮小倍率
zoom_factor = 1.0

# 倍率調整率
zoom_step = 0.01

# 垂直反転
flip_vertical = True

# アプリケーションタイトル
APP_TITLE = "Projector App"

# 画質オプションの定義
IMAGE_QUALITIES = [
    {"width":256,"height":144},
    {"width":426,"height":240},
    {"width":640,"height":360},
    {"width":854,"height":480},
    {"width":1280,"height":720},
    {"width":1920,"height":1080}
]

# 画質名を取得
def get_quality_names():
    names = []
    for image_quality in IMAGE_QUALITIES:
        names.append(f"{image_quality['height']}p ({image_quality['width']}x{image_quality['height']})")
    return names

# 状態
connected = False

# 画面キャプチャと送信を行う関数
def disp(client):
    global connected,height,width,zoom_factor,flip_vertical
    try:
        while connected:
            # フレームのキャプチャ
            with mss() as sct:
                monitor = sct.monitors[1]  # プライマリモニターを選択
                frame = sct.grab(monitor) # 画面全体をキャプチャ
            frame = cv2.cvtColor(np.array(frame), cv2.COLOR_BGRA2BGR) # BGRAからBGRに変換
            frame = cv2.resize(frame, (width, height))   # 解像度をwidthxheightにリサイズ

            if flip_vertical:
                frame = cv2.flip(frame, 0)  # 垂直反転
            # frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=10)  # 明るさ調整

            # 拡大・縮小処理
            if zoom_factor != 1.0:
                frame = cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor)

            # フレームのエンコード
            _, buffer = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY, 30])
            data = buffer.tobytes()
            
            # データの送信
            size = len(data) # フレームサイズ
            client.sendall(struct.pack(">I", size))  # フレームサイズを送信
            client.sendall(data)  # フレームデータを送信
            time.sleep(0.03)  # 約30fpsで送信
    
    except Exception as e:
        switch_disconnection(mes=False)
        messagebox.showerror(APP_TITLE, f"接続が切断されました。\nエラー: {e}")
        
    finally:
        # クライアントソケットのクローズ
        client.close()

# 接続状態に切り替え
def switch_connection():
    global connected
    connected = True # 接続状態を更新
    # ボタンのテキストを「切断」に変更
    button.config(text="切断")
    combox.config(state="disabled")  # コンボボックスを無効化
    # 情報メッセージの表示
    messagebox.showinfo(APP_TITLE, "接続しました。")

# 切断状態に切り替え
def switch_disconnection(mes=True):
    global connected
    connected = False # 接続状態を更新
    # ボタンのテキストを「接続」に変更
    button.config(text="接続")
    combox.config(state="readonly")  # コンボボックスを有効化
    # 情報メッセージの表示
    if mes:
        messagebox.showinfo(APP_TITLE, "切断しました。")

# ボタンクリック時の処理
def on_button_click():
    # グローバル変数の使用宣言
    global connected,HOST,height,width
    # HOSTが未設定の場合、設定ダイアログを表示
    if not HOST:
        messagebox.showwarning(APP_TITLE, "接続先が設定されていません。")
        return
    # 接続中の場合
    if connected:
        # 切断処理
        switch_disconnection()  # 切断状態に切り替え
        return
    # 選択された画質オプションの取得
    selected_option = combox.current()
    # クライアントソケットの作成
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        messagebox.showerror(APP_TITLE, f"接続に失敗しました。\nエラー: {e}")
        return
    # 画面キャプチャと送信を行うスレッドの開始
    height = IMAGE_QUALITIES[selected_option]["height"]
    width = IMAGE_QUALITIES[selected_option]["width"]
    switch_connection() # 接続状態に切り替え
    threading.Thread(target=disp, args=(client,), daemon=True).start()

# ウィンドウ終了時の処理
def on_exit():
    ret = messagebox.askokcancel("確認", "本当に終了しますか？")
    if ret:
        app.destroy()

# 設定
def on_setting():
    global HOST
    # 接続先IPアドレスの入力ダイアログ表示
    input = simpledialog.askstring(APP_TITLE, "接続先のデバイスのIPアドレスを入力してください。")
    # 入力がキャンセルされた場合は処理を中止
    if not input:
        return
    HOST = input
    status_bar.config(text=f"接続先：{HOST}")

# 拡大
def on_zoom_in():
    global zoom_factor,zoom_step
    zoom_factor = min(1, zoom_factor + zoom_step)

# 縮小
def on_zoom_out():
    global zoom_factor,zoom_step
    zoom_factor = max(0.1, zoom_factor - zoom_step)

# 倍率リセット
def on_zoom_reset():
    global zoom_factor
    zoom_factor = 1.0

# バージョン情報
def on_about():
    messagebox.showinfo(APP_TITLE, "Projector App\nバージョン 1.0")

# 垂直反転切り替え
def on_flip_vertical():
    global flip_vertical
    flip_vertical = not flip_vertical

app = tk.Tk()
# ウィンドウの設定
app.title(APP_TITLE)
# ウィンドウサイズの固定
app.geometry("370x125")
# リサイズ不可
app.resizable(False, False)

# メニューバー
menubar = tk.Menu(app)
app.config(menu=menubar)

# メニュー
menu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label="メニュー", menu=menu)
menu.add_command(label="接続先設定", command=on_setting)
menu.add_command(label="垂直反転切替", command=on_flip_vertical)
menu.add_command(label="終了", command=on_exit)

zoom = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="ズーム", menu=zoom)
zoom.add_command(label="ズームアウト", command=on_zoom_out)
zoom.add_command(label="ズームイン", command=on_zoom_in)
zoom.add_command(label="リセット", command=on_zoom_reset)

help_menu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="ヘルプ", menu=help_menu)
help_menu.add_command(label="バージョン情報", command=on_about)

# コンボボックスの作成
combox = ttk.Combobox(app, values=get_quality_names(),state="readonly")
combox.current(5) # デフォルト選択を1080pに設定
combox.pack(pady=5)

# ボタンの作成
button = ttk.Button(app, text="接続",width=10,command=on_button_click)
button.pack(pady=5)

# ステータスバー
status_bar = ttk.Label(app, text="接続先：未設定", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# ウィンドウ終了時のイベントバインド
app.protocol("WM_DELETE_WINDOW", on_exit)

# メインループの開始
app.mainloop()