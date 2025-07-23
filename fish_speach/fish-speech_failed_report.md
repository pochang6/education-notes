# Fish-Speech ローカルTTS構築失敗レポート

## 📅 実施日
2025年07月23日

## 🧭 実行環境

- **OS**: macOS (Apple Silicon, MacBook Air)
- **Python**: 3.11 (venv環境)
- **プロジェクトルート**: `~/develop/fish-speech-local/fish-speech`
- **仮想環境**: `.venv` 配下に構築済み

---

## 🛠️ 試行内容一覧（成功/失敗）

### ✅ 1. 仮想環境のセットアップとパッケージ準備

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### ✅ 2. 必要パッケージのインストール

```bash
pip install numpy Cython setuptools
pip install cymem murmurhash preshed thinc blis
```

### ❌ 3. audiotools の導入失敗

```bash
pip install audiotools
# → 「No matching distribution found for audiotools」
```

→ 対応策として `audiocraft` 経由での間接導入を試行

---

## 🔁 Audiocraft を使った回避策の試行

### ❌ Audiocraft 最新版での導入失敗（spacy==3.7.6ビルド失敗）

```bash
pip install git+https://github.com/facebookresearch/audiocraft --no-build-isolation
# → Cythonエラー（spacy/lexeme.pyx: undeclared name not builtin: long）
```

### 🔁 対応策：`spacy==3.7.3` ダウングレード

```bash
pip install spacy==3.7.3
# → 依存解決失敗（numpyやthincなど再ダウングレードが発生）
```

→ `audiocraft` ビルド継続不能

---

## 🔚 結果として確認された問題

- `audiotools` モジュール単体での pip 導入が不可能
- `audiocraft` を通じて導入するも、macOS + Python 3.11 環境では `spacy` のCythonビルドが通らない
- Fish-Speech の `inference_engine` が `audiotools.AudioSignal` に依存しており、実行不能

---

## 🧯 リカバリーとして試した内容

- spacyのバージョンダウン（3.7.6 → 3.7.3 → 3.7.2）
- `--no-build-isolation` を付けて依存解決回避を試みたが効果なし
- `audiocraft` の任意コミットID導入試行 → 該当コミット存在せず失敗

---

## 📌 結論

Fish-Speechの現時点GitHub公開版は、Apple Silicon環境においては以下の理由により**正常動作困難**：

- `audiotools` 非公開 or 廃止パッケージで代替不可
- `spacy` ビルドでCython互換性エラー
- `run_webui.py` は `audiotools` に強く依存しているため、置き換えも難しい

---

## 🗒️ 備考・ログ保存

- pip install / 実行コマンドは script コマンドを使って記録済み
- 今後は F5-TTS や別モデルへの移行を検討予定
