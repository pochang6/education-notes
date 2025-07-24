# 日本語音声クローン生成ガイド（XTTS v2 + Coqui TTS）

この手順は、**macOS または Windows 環境で、10秒以内の日本語音声をもとに高精度な音声合成を行う**ためのセットアップ手順です。  

---

## 📁 1. 作業ディレクトリの作成

### ✅ macOS の場合

```bash
mkdir -p ~/develop/xtts_v2_jp
cd ~/develop/xtts_v2_jp
```

### ✅ Windows の場合（PowerShell）

```powershell
mkdir $HOME\develop\xtts_v2_jp
cd $HOME\develop\xtts_v2_jp
```

---

## 🐍 2. Python仮想環境を作成・有効化

### ✅ macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### ✅ Windows

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

---

## 📦 3. 必要パッケージのインストール（共通）

```bash
pip install --upgrade pip
pip install TTS torch
```

---

## 🔊 4. 音声ファイルの準備

10秒以内の日本語音声（例：「input.wav」）を `wavs/` に配置してください：

```bash
mkdir wavs
# Finderやエクスプローラーで input.wav を wavs/ に入れる
```

---

## 📝 5. 推論スクリプトの作成

「generate.py」という名前で以下のコードを保存：

```python
from TTS.api import TTS
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)

tts.tts_to_file(
    text="おはようございます。今日はいい天気ですね。",
    speaker_wav="wavs/input.wav",
    language="ja",
    file_path="output.wav"
)
```

---

## ▶️ 6. 音声生成を実行

```bash
python generate.py
```

---

## 🎧 7. 音声の再生

### ✅ macOS

```bash
afplay output.wav
```

### ✅ Windows

```powershell
start output.wav
```

---

## 🗂 8. ディレクトリ構成

```
develop/xtts_v2_jp/
├── .venv/             ← Python仮想環境
├── wavs/
│   └── input.wav      ← 入力音声
├── generate.py        ← 推論スクリプト
└── output.wav         ← 出力音声
```

---

## ✅ ヒントと注意点

- `language="ja"` は**必ず指定**してください。
- CPU環境では長文は時間がかかるため、**短文単位で生成**しましょう。
- 音源は静かで明瞭な音声を使うと精度が上がります。

---

この手順に従えば、**MacでもWindowsでもXTTS v2を使った日本語音声クローンがローカルで実現**できます。
