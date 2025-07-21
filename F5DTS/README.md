# F5-TTS AWS Deployment (CDK)

This directory contains an AWS CDK stack that automatically builds an EC2
environment ready for the F5‑TTS voice synthesis toolkit as described in
`F5-TTS完全実践ガイド(AWS_EC2).md`.  The instructions below assume you are using
macOS (for example on a MacBook Air) and start from a blank environment.

## Prerequisites

1. **AWS account** – sign up at <https://aws.amazon.com/> and create an IAM user
   with administrative privileges.  Generate an **Access Key ID** and **Secret
   Access Key** for this user.
2. **AWS CLI** – install via Homebrew and configure your credentials:

   ```bash
   brew install awscli
   aws configure
   # enter the Access Key, Secret Key, default region (e.g. ap-northeast-1) and
   # output format (e.g. json)
   ```
   
3. **Node.js** (version 20 or 22) and the AWS CDK Toolkit:

   CDK 2.x is tested with Node 20 and Node 22.  Using a newer release such as
   Node 24 will print a warning.  On macOS you can install the LTS version and
   the CDK CLI as follows:

   ```bash
   brew install node@20
   echo 'export PATH="$(brew --prefix node@20)/bin:$PATH"' >> ~/.zprofile
   source ~/.zprofile
   npm install -g aws-cdk
   ```
4. **Python 3.8+** – available on recent macOS versions.  Verify with

   ```bash
   python3 --version
   ```

## Setup

1. Clone this repository and change into the `F5DTS` directory:

   ```bash
   git clone https://github.com/pochang6/education-notes.git
   cd education-notes/F5DTS
   ```

2. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Bootstrap the CDK (first time you use CDK in this AWS account and region):

```bash
cdk bootstrap
```

5. Deploy the stack.  Pass the name of an existing EC2 key pair via context (create one in the EC2 console if you do not have it):

```bash
cdk deploy -c key_name=<your-keypair-name>
```

The deployment takes several minutes.  When it finishes the command output will
print the allocated **Elastic IP**.  You can also find this address in the EC2
console.  The stack creates:

- Security group allowing SSH (22) and Gradio UI (7860)
- g4dn.xlarge EC2 instance with Deep Learning AMI
- the latest AMI ID is looked up automatically at deploy time
- 60 GB gp3 root volume
- Elastic IP attached to the instance
- User data that installs Git, FFmpeg and clones F5‑TTS

After deployment, note the Elastic IP from the outputs or the EC2 console.

## Manual Steps

1. In a new terminal window upload your prepared `wavs` directory and
   `metadata.csv` to the instance.  Replace `<ElasticIP>` with the address output
   from the deploy step and `<keypair.pem>` with the path to your private key:

```bash
scp -i <keypair.pem> -r ./wavs ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/
scp -i <keypair.pem> metadata.csv ubuntu@<ElasticIP>:/home/ubuntu/F5-TTS/data/pocho/
```

2. SSH into the instance and start the Gradio UI for a quick test:

```bash
ssh -i <keypair.pem> ubuntu@<ElasticIP>
f5-tts_infer-gradio
```
If the command is not found, ensure `$HOME/.local/bin` is in your `PATH` or
re-login to refresh the environment.
   Then open `http://<ElasticIP>:7860` in your browser and type some text to hear
   the synthesized voice.

3. To train your model, prepare a config and run:

```bash
cd F5-TTS
cp configs/base_config.json configs/pocho_config.json
# edit the config as needed
python train.py --config configs/pocho_config.json
```

### Cleaning Up

Run `cdk destroy` to remove all resources when you are done.  Alternatively you
can stop the EC2 instance from the AWS console while keeping the environment for
later use.
