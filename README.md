# 🎙️ Vozia

Conversor de texto em áudio usando modelos Piper VITS via `sherpa-onnx`.

## ⚙️ Requisitos

- 🐍 Python 3.10+
- 📦 Dependências Python listadas em `requirements.txt`

Instale tudo com:

```bash
pip install -r requirements.txt
```

Certifique-se de baixar um modelo e extraí-lo em `./vits-piper-pt_BR-dii-high`
(padrão atual do projeto) ou utilize os parâmetros descritos abaixo.

## ⬇️ Download do modelo PT-BR

Clonar o repositório:

```bash
git clone https://github.com/leoberbert/Vozia.git

cd Vozia

```

Após clonar o repositório, baixe o modelo PT-BR recomendado:

```bash
wget https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-pt_BR-dii-high.tar.bz2
tar -xjf vits-piper-pt_BR-dii-high.tar.bz2
```

Isso criará o diretório `vits-piper-pt_BR-dii-high` esperado pela CLI (ou ajuste com `--model-dir`).

## ▶️ Uso

```bash
python vozia_cli.py \
  --text "Olá! Esta é uma demonstração da Vozia." \
  --output saida.wav \
  --speaker-id 0 \
  --speed 1.0
```

### 🛠️ Parâmetros principais

- 📝 `--text` ou `--text-file`: **obrigatório** informar um dos dois; use texto direto ou aponte para um arquivo UTF-8 (`python vozia_cli.py --text-file texto.txt`).
- 💾 `--output`: caminho para o arquivo gerado (sempre `.wav`; outras extensões são substituídas por `.wav`).
- 🎚️ `--speaker-id` e `--speed`: personalizam a voz e ritmo.
- 🗂️ `--model-dir`, `--model-file`, `--tokens-file`, `--data-dir`: permitem apontar para outros modelos Piper.
- ♻️ `--overwrite`: permite sobrescrever arquivos existentes.

Execute `python vozia_cli.py --help` para ver a lista completa.

## ℹ️ Observações

- ✅ A CLI valida se todos os arquivos necessários do modelo estão presentes antes da síntese.
- 🎧 O áudio é exportado apenas em WAV para evitar dependências extras.

## 🔗 Referências

- Projeto base do mecanismo TTS: [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
