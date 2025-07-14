# 【F5-TTS 完全実践ガイド (AWS EC2編)】

---

## 🔰 目的

本手順は、録音済みの自分の音声（WAVファイル）をもとに、AWS EC2上で\*\*F5-TTS (FFAMDTS)\*\*を用いて独自音声合成モデルを学習・推論可能な状態にするための完全ガイドです。

---

## ✅ 前提条件

- AWSアカウント保有済み
- ローカルに音声ファイル（WAV）と `metadata.csv` がある（Whisper等で作成済）
- Python/SSH の基本操作ができる

---

## 🧱 ステップ0：音声データの前処理（参考：今回はスキップ）

※ここは準備済みであれば読み飛ばしてOK。今後他人に伝えるために記載。

### ◯ 0-1. 音源のWAV化

- Audacityなどで録音ファイル（m4aなど）を `16bit PCM / 44.1kHz` のWAVに変換

### ◯ 0-2. Whisperで文字起こし

```bash
whisper input.wav --language Japanese --task transcribe --output_format tsv
```

### ◯ 0-3. Pythonスクリプトで分割

- Whisperの出力TSVを使い、区間ごとに音声を分割（例：`split_wav_by_tsv.py`）
- `wavs/0001.wav`〜と `metadata.csv` を作成

---

## 🚀 ステップ1：EC2インスタンスの作成

### ◯ 1-1. AMI選択

- マーケットプレイスから以下を選択：

```
Deep Learning AMI GPU PyTorch 1.13.1 (Ubuntu 20.04) - ami-0f36dc4944df7a3d6（東京）
```

### ◯ 1-2. インスタンスタイプ

- **g4dn.xlarge**（NVIDIA T4 GPU搭載、RAM 16GB）

### ◯ 1-3. ストレージ

- ルートボリューム：**60GB〜100GB (gp3)** を推奨（AMI化やキャッシュ保存のため）

### ◯ 1-4. セキュリティグループ

- ポート開放：
  - TCP 22（SSH）
  - TCP 7860（Gradio UI）

---

## 🔌 ステップ2：SSH接続 & 初期セットアップ

### ◯ 2-1. 接続

```bash
ssh -i ~/.ssh/your-key.pem ubuntu@<EC2のパブリックIP>
```

### ◯ 2-2. パッケージとGit環境

```bash
sudo apt update && sudo apt install -y git ffmpeg
```

### ◯ 2-3. F5-TTSのクローンとインストール

```bash
git clone https://github.com/SWivid/F5-TTS.git
cd F5-TTS
pip install -e .
```

---

## 📦 ステップ3：音声データのアップロード

```bash
scp -i ~/.ssh/your-key.pem -r ./wavs ubuntu@<EC2アドレス>:/home/ubuntu/F5-TTS/data/pocho/
scp -i ~/.ssh/your-key.pem metadata.csv ubuntu@<EC2アドレス>:/home/ubuntu/F5-TTS/data/pocho/
```

> ※ `pocho` は任意のspeaker名。変更する場合は `config.json` も合わせること

---

## 🌐 ステップ4：Gradio UI起動（推論テスト）

```bash
F5-tts_infer-gradio
```

- ブラウザで `http://<ElasticIP>:7860` にアクセス
- テキスト入力 → 合成音声再生 or DL

---

## 🏋️ ステップ5：モデル学習の開始

### ◯ 5-1. configファイルの用意

```bash
cp configs/base_config.json configs/pocho_config.json
nano configs/pocho_config.json
```

- 修正箇所：
  - `speaker_name`: "pocho"
  - `data_path`: "data/pocho"
  - `output_path`: "output/pocho"

### ◯ 5-2. 学習コマンド

```bash
python train.py --config configs/pocho_config.json
```

> 進行中は `output/pocho/` に `.pt` ファイルが出力される

---

## 📣 ステップ6：モデル完成後の推論

- 再度 Gradio UI を開き、学習済みモデルを使って推論可能
- または、CLIからの合成も可能（後述）

---

## 💡 ステップ7：Elastic IP の関連（簡易）

- EC2停止時でも IPが変わらないようにするには Elastic IP 割当を推奨
- VPC・サブネット・セキュリティグループ設定は任意（既存でOK）

---

## 💰 コスト感（2025年時点）

| 項目              | 単価例          | 時間  | 小計          |
| --------------- | ------------ | --- | ----------- |
| EC2 g4dn.xlarge | 約50円/時（東京）   | 20h | 約1000円      |
| EBS（60GB）       | 約13円/GB・月    |     | 約780円       |
| Elastic IP      | 割当中無料／未使用時有料 |     | 0円〜         |
| **合計（目安）**      |              |     | **1780円程度** |

---

## ✅ 成果物（期待される）

- `/output/pocho/` に `.pt` モデルファイル（独自音声モデル）
- Gradio上でのリアルタイム推論
- AMI化して社内/個人再利用も可能

---

## 🔁 補足：AMI化のすすめ

- `EC2 > イメージ > イメージの作成` でAMI化可能
- チーム共有や再構築が楽

---

## ✅ 参考リンク

- GitHub: [https://github.com/SWivid/F5-TTS](https://github.com/SWivid/F5-TTS)
- Gradio: [https://www.gradio.app/](https://www.gradio.app/)

---

この手順をベースに、ひろさんが公開できる形式（GitHub Projects/Wiki/README）などへ自由に変換してご活用ください。

