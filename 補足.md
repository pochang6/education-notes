# F5-TTS AWS Deployment Guide

このドキュメントでは、AWS上でF5-TTSの音声合成モデルを学習・推論・Gradio UI公開まで行う一連の手順と、それをローカル環境や安価なインスタンスタイプに展開するための補足情報を提供します。

---

## 1. 事前準備（macOS向け）

### 1.1 AWSアカウントとIAMユーザー
- AWSアカウント作成: https://aws.amazon.com/
- 管理者権限のIAMユーザー作成
- アクセスキーIDとシークレットキーを取得

### 1.2 AWS CLIのインストールと設定
```bash
brew install awscli
aws configure
# → Access Key, Secret Key, region（例: ap-northeast-1）、出力形式（例: json）
```

### 1.3 Node.js (20 or 22) + AWS CDK
```bash
brew install node@20
echo 'export PATH="$(brew --prefix node@20)/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
npm install -g aws-cdk
```

### 1.4 Python 3.8+ と仮想環境
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 2. 環境構築

### 2.1 リポジトリのクローン
```bash
git clone https://github.com/pochang6/education-notes.git
cd education-notes/F5DTS
```

### 2.2 依存ライブラリのインストール
```bash
pip install -r requirements.txt
```

### 2.3 CDKの初期化とデプロイ
```bash
cdk bootstrap
cdk deploy -c key_name=<your-keypair-name>
```

### 2.4 デプロイ内容
- g4dn.xlarge EC2 (Deep Learning AMI)
- 60GB gp3 EBS + Elastic IP
- SSH (22) / Gradio (7860)ポート許可
- Git, FFmpeg, F5-TTS自動セットアップ

---

## 3. データアップロードと推論テスト

### 3.1 音声データとメタデータの転送
```bash
scp -i <keypair.pem> -r ./wavs ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/
scp -i <keypair.pem> metadata.csv ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/
```

### 3.2 EC2へのSSHログインとGradio起動
```bash
ssh -i <keypair.pem> ubuntu@<ElasticIP>
source ~/.bashrc
f5-tts_infer-gradio
```

→ `https://xxxx.gradio.live` が表示されたら、それを開くとWeb上で合成テストが可能

---

## 4. モデルの再学習
```bash
cd F5-TTS
cp configs/base_config.json configs/pocho_config.json
# viやnanoでconfig編集
python train.py --config configs/pocho_config.json
```

---

## 5. インスタンスタイプの切り替え戦略

| 用途               | 推奨インスタンスタイプ |
|--------------------|------------------|
| モデル学習        | g4dn.xlarge       |
| 合成テスト (1人)  | t3.large / t3.medium |
| 長期運用/低コスト | Lightsail / ローカル |

---

## 6. 後片付け
```bash
cdk destroy
```
もしくは EC2 を一時停止して費用を抑える。

---

## 7. 注意事項と補足

- `f5-tts_infer-gradio` が動かない場合 `$HOME/.local/bin` が PATH に含まれていない可能性あり。
- ポート 7860 が開いていないと Gradio UI が見えない。
- 初期Gradioは `http://<ElasticIP>:7860` だが、トンネリングで `.gradio.live` URLに変わる。

---

## 8. 今後の拡張案

- Docker化してローカル（MacBook Air）でGradio運用
- EC2 Spot Instance化でさらに低コスト化
- 推論API化（FastAPIなど）で社内サービス展開

---

以上

