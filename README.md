# Projector Application

プロジェクター・投影のための、小規模なクロスプラットフォームプロジェクト（Windows と Android 向け）のプログラムです。プログラムは Python ベースで、プラットフォームごとに `src/android` と `src/windows` にエントリポイントがあります。

## 実行手順（概要）

### Windows（送信側）

1. 仮想環境を作成して有効化:

    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate
    ```

2. 依存関係をインストール:

    ```powershell
    pip install -r requirements.txt
    ```

3. アプリを起動:

    ```powershell
    python src/windows/main.py
    ```

4. ウィンドウの「メニュー」→「接続先設定」で受信側（表示機）の IP アドレスを入力し、「接続」ボタンを押します。

### Android / Kivy（受信側）

- 開発中に PC 上で動かす場合（Kivy がインストール済みの環境）:

    ```bash
    cd src/android
    python main.py
    ```

- 実機向けにパッケージ化する場合は `buildozer` を利用します（通常は WSL2 または Linux 上で実行）:

    ```bash
    cd src/android
    pip install buildozer
    buildozer -v android debug
    ```

    ※ Kivy／Buildozer のインストールや Android SDK/NDK の設定は環境に依存します。詳細は Buildozer のドキュメントを参照してください。

## プログラム（ファイル一覧）

- `src/windows/main.py` — Windows 側の画面キャプチャ送信アプリ（GUI）
- `src/android/main.py` — Kivy を使った受信・表示アプリ
- `src/android/buildozer.spec` — Android パッケージ化用設定
- `src/android/data/` — アプリで使う画像リソース（`image.png`, `icon.png`, `presplash.png` など）
- `requirements.txt` — Python 依存
