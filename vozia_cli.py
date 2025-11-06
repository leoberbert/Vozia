#!/usr/bin/env python3
"""CLI simples para converter texto em fala usando sherpa-onnx.

Projeto original: https://github.com/k2-fsa/sherpa-onnx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Tuple

import sherpa_onnx
import soundfile as sf


DEFAULT_MODEL_DIR = Path(__file__).resolve().parent / "vits-piper-pt_BR-dii-high"
DEFAULT_MODEL_FILE = "pt_BR-dii-high.onnx"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Converte texto em áudio usando modelos Piper VITS via sherpa-onnx.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=DEFAULT_MODEL_DIR,
        help="Diretório contendo o modelo Piper e os arquivos auxiliares.",
    )
    parser.add_argument(
        "--model-file",
        type=Path,
        default=None,
        help="Arquivo .onnx (padrão: <model-dir>/pt_BR-dii-high.onnx).",
    )
    parser.add_argument(
        "--tokens-file",
        type=Path,
        default=None,
        help="Arquivo tokens.txt (padrão: <model-dir>/tokens.txt).",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Diretório espeak-ng-data (padrão: <model-dir>/espeak-ng-data).",
    )

    text_group = parser.add_mutually_exclusive_group(required=True)
    text_group.add_argument(
        "--text",
        help="Texto em linha para síntese.",
    )
    text_group.add_argument(
        "--text-file",
        type=Path,
        help="Arquivo UTF-8 com o texto a ser sintetizado.",
    )

    parser.add_argument(
        "--speaker-id",
        type=int,
        default=0,
        help="ID do locutor. Consulte a documentação do modelo.",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Fator de velocidade (1.0 = normal).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("saida.wav"),
        help="Arquivo de saída.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescreve o arquivo de saída caso já exista.",
    )
    return parser.parse_args()


def resolve_model_paths(args: argparse.Namespace) -> Tuple[Path, Path, Path]:
    model_dir = args.model_dir
    model_path = args.model_file or (model_dir / DEFAULT_MODEL_FILE)
    tokens_path = args.tokens_file or (model_dir / "tokens.txt")
    data_dir = args.data_dir or (model_dir / "espeak-ng-data")

    missing = [p for p in (model_path, tokens_path, data_dir) if not Path(p).exists()]
    if missing:
        missing_fmt = "\n  ".join(str(Path(p).resolve()) for p in missing)
        raise FileNotFoundError(
            "Não foi possível localizar os arquivos necessários:\n  " + missing_fmt
        )
    return Path(model_path), Path(tokens_path), Path(data_dir)


def load_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text.strip()
    if args.text_file:
        path = args.text_file
        if not path.exists():
            raise FileNotFoundError(f"Arquivo de texto não encontrado: {path}")
        return path.read_text(encoding="utf-8").strip()
    raise ValueError("Informe --text ou --text-file.")


def infer_output(args: argparse.Namespace) -> Path:
    output = args.output
    if output.suffix.lower() != ".wav":
        output = output.with_suffix(".wav")
    return output


def build_tts(model_path: Path, tokens_path: Path, data_dir: Path) -> sherpa_onnx.OfflineTts:
    model_config = sherpa_onnx.OfflineTtsModelConfig()
    model_config.vits.model = str(model_path)
    model_config.vits.tokens = str(tokens_path)
    model_config.vits.data_dir = str(data_dir)
    config = sherpa_onnx.OfflineTtsConfig(model=model_config)
    print(f"Carregando modelo em '{model_path.parent}'...")
    return sherpa_onnx.OfflineTts(config)


def save_audio(audio, output_path: Path, overwrite: bool) -> None:
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"O arquivo '{output_path}' já existe. Use --overwrite para substituir."
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output_path, audio.samples, samplerate=audio.sample_rate)
    print(f"Áudio salvo em '{output_path}' (WAV).")


def main() -> None:
    args = parse_args()
    model_path, tokens_path, data_dir = resolve_model_paths(args)
    text = load_text(args)
    output_path = infer_output(args)

    tts = build_tts(model_path, tokens_path, data_dir)
    print("Modelo carregado. Iniciando síntese...")
    audio = tts.generate(text, sid=int(args.speaker_id), speed=float(args.speed))
    save_audio(audio, output_path, args.overwrite)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        sys.exit(130)
    except Exception as exc:  # pragma: no cover - logging simples
        print(f"Erro: {exc}")
        sys.exit(1)
