import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox

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
        names.append(f"{image_quality['height']}p ({image_quality['width']}x{image_quality['height']})")
    return names

# 状態
connected = False

# ボタンクリック時の処理
def on_button_click():
    # グローバル変数の使用宣言
    global connected
    # 接続中の場合
    if connected:
        # 切断処理
        button.config(text="接続")
        messagebox.showinfo(APP_TITLE, "切断しました。")
        connected = False
        return
    # 接続先IPアドレスの入力ダイアログ表示
    input = simpledialog.askstring(APP_TITLE, "接続先のデバイスのIPアドレスを入力してください。")
    # 入力がキャンセルされた場合は処理を中止
    if not input:
        return
    # 選択された画質オプションの取得
    selected_option = combox.current()
    # ボタンのテキストを「切断」に変更
    button.config(text="切断")
    # 情報メッセージの表示
    messagebox.showinfo(APP_TITLE, "接続しました。")
    connected = True

# ウィンドウ終了時の処理
def on_exit():
    ret = messagebox.askokcancel("確認", "本当に終了しますか？")
    if ret:
        app.destroy()

app = tk.Tk()
# ウィンドウの設定
app.title(APP_TITLE)
# ウィンドウサイズの固定
app.geometry("250x70")
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