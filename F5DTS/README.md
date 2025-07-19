# F5-TTS AWS デプロイ（CDK 版）

この CDK プロジェクトは、`F5-TTS完全実践ガイド(AWS_EC2).md` に記載されたとおり、F5‑TTS 音声合成ツールキット用に事前構成された EC2 インスタンスを構築します。

## 前提条件

* Python 3.8 以上
* CDK 用に設定された AWS 認証情報
* [AWS CDK ツールキット](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)（以下でインストール）

```bash
npm install -g aws-cdk
```

## セットアップ手順

```bash
# ① 仮想環境の作成と有効化
python3 -m venv .venv
source .venv/bin/activate

# ② 依存パッケージのインストール
pip install -r requirements.txt

# ③ CDK 初期化（初回のみ）
cdk bootstrap

# ④ スタックのデプロイ（キーペア名を指定）
cdk deploy -c key_name=<your-keypair-name>
```

## スタック作成内容

* SSH (22番) と Gradio UI (7860番) を許可するセキュリティグループ
* Deep Learning AMI を使った g4dn.xlarge EC2 インスタンス
* 60GB gp3 EBS（ルート）
* Elastic IP
* Git、FFmpeg のインストールおよび F5‑TTS のクローンを含むユーザーデータ

## 手動作業

```bash
# ① 音声ファイルとメタデータのアップロード
scp -i <keypair.pem> -r ./wavs ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/
scp -i <keypair.pem> metadata.csv ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/

# ② インスタンスへ SSH 接続し Gradio UI を起動
ssh -i <keypair.pem> ubuntu@<ElasticIP>
F5-tts_infer-gradio

# ③ モデル学習の実行（設定ファイルを準備して起動）
cd F5-TTS
cp configs/base_config.json configs/pocho_config.json
# ※ テキストエディタで pocho_config.json を編集
python train.py --config configs/pocho_config.json
```

## 後始末（リソース削除）

```bash
cdk destroy
```
