# Fish-Speech 導入マニュアル（Windows WSL2 / Mac 対応）

## 🎯 目的

本マニュアルは、「F5-TTS」による独自音声モデル構築を試みたが、技術的ハードルが高く断念した経験を踏まえ、より安定性と導入性の高い「Fish-Speech」を用いて、**自分の声によるTTS（テキスト音声合成）環境**を構築するための手順を丁寧に記録したものです。

## 🐟 Fish-Speechとは？

- オープンソースの多言語・ゼロショット音声クローン TTS モデル。
- HuggingFace 上で公開されており、**10秒程度の音声から簡易モデルを生成**し、テキスト音声合成が可能。
- 日本語にも対応済。
- GUI（Web UI）・CLI（コマンドライン）どちらでも利用可能。
- CPUでも動作可能（GPU推奨）。

## 💻 対応環境

| 項目     | 内容                                           |
| ------ | -------------------------------------------- |
| OS     | Windows（WSL2 Ubuntu 22.04） / macOS（12以降）     |
| 必要なソフト | Git / Python 3.10〜3.11 / ffmpeg / sox / wget |
| 推奨環境   | VRAM 4GB 以上のGPU（なくても可）                       |

---

## 📁 ディレクトリ構成（推奨）

```
fish-speech-local/
├── audio/               # 音声サンプルを入れる（*.wav）
├── output/              # 合成音声の出力先
├── fish-speech/         # GitHubからクローンした本体
└── README.md            # 本マニュアル
```

---

## 🔧 セットアップ手順

### 1. Python仮想環境の作成（共通）

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows WSL2 も Mac も同様
```

### 2. 依存ライブラリのインストール（共通）

```bash
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
pip install -e .
```

### 3. その他依存ツールのインストール

#### ■ macOS

```bash
brew install ffmpeg sox wget
```

#### ■ Windows（WSL2 Ubuntu）

```bash
sudo apt update && sudo apt install ffmpeg sox wget
```

---

## 🎤 自分の音声の準備

1. `audio/` ディレクトリを作成し、\*\*自分の声の `.wav` ファイル（1〜3個程度）\*\*を格納。
2. 音声は 16bit PCM / mono / 24kHz 推奨。
3. 名前は `myvoice1.wav` など分かりやすく。

---

## 🧪 ゼロショット声クローン＋合成の実行

### `infer_cli.py` を直接叩く（コマンドライン）

```bash
python3 infer_cli.py \
  -r audio/myvoice1.wav \
  -t "こんにちは、私はテキストから音声を作っています。" \
  -w output/output.wav \
  --device cpu
```

> ✅ `-r`：参照音声（クローン元） ✅ `-t`：発話させるテキスト（UTF-8 日本語対応） ✅ `-w`：出力先 wav ファイル

---

## 🌐 Web UIで試す

```bash
python3 app.py --device cpu
```

- ブラウザで `http://localhost:7860` を開く。
- 参照音声とテキストを指定するだけで音声合成可能。

---

## 📌 注意点

- モデルやボコーダーは初回実行時に HuggingFace から自動ダウンロード（1.5GB 以上）されます。
- 合成後の `.wav` は `output/` 以下に保存。
- 音質を上げたい場合は GPU（VRAM 4GB〜）使用推奨。

---

## 🏁 今後の展望

- 現在の環境は\*\*即席音声合成（ゼロショット）\*\*であり、
  - より精度を高めたい場合は少量ファインチューニングも可（別マニュアル）。
- 合成結果の精度は**音声品質×明瞭な発話**に左右される。

---

## 🙏 最後に

F5-TTSでは困難だった "独自音声で日本語をしゃべらせる" という目的を、Fish-Speechなら比較的手軽に実現可能です。 本マニュアルが迷子にならず導入を進められる助けとなれば幸いです。
