# F5-TTS AWS Deployment (CDK)

This CDK project provisions an EC2 instance pre-configured for the F5‑TTS voice synthesis toolkit as described in `F5-TTS完全実践ガイド(AWS_EC2).md`.

## Requirements

- Python 3.8+
- AWS credentials configured for CDK
- [AWS CDK Toolkit](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) (`npm install -g aws-cdk`)

## Setup

1. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Bootstrap the CDK (first time in an AWS account/region):

```bash
cdk bootstrap
```

4. Deploy the stack. Specify an existing EC2 key pair name via context or edit `app.py`:

```bash
cdk deploy -c key_name=<your-keypair-name>
```

The stack creates:

- Security group allowing SSH (22) and Gradio UI (7860)
- g4dn.xlarge EC2 instance with Deep Learning AMI
- 60 GB gp3 root volume
- Elastic IP attached to the instance
- User data that installs Git, FFmpeg and clones F5‑TTS

After deployment, note the Elastic IP from the outputs or the EC2 console.

## Manual Steps

1. Upload your prepared `wavs` directory and `metadata.csv` to the instance:

```bash
scp -i <keypair.pem> -r ./wavs ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/
scp -i <keypair.pem> metadata.csv ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/
```

2. SSH into the instance and start the Gradio UI for a quick test:

```bash
ssh -i <keypair.pem> ubuntu@<ElasticIP>
F5-tts_infer-gradio
```

3. To train your model, prepare a config and run:

```bash
cd F5-TTS
cp configs/base_config.json configs/pocho_config.json
# edit the config as needed
python train.py --config configs/pocho_config.json
```

### Cleaning Up

Run `cdk destroy` to remove the deployed resources when finished.
