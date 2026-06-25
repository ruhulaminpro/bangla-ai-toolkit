"""Command-line interface for bangla-ai.

Text-utility commands (normalize, tokenize, stem, translit, digits) run with
zero dependencies. ML commands (summarize, qa, sentiment, ner) need a backend
(`--backend transformers` or `--backend openai`).

Examples::

    bangla-ai normalize "বাংলা   টেক্সট"
    bangla-ai translit --to latin "বাংলাদেশ"
    bangla-ai digits --to bn "2024"
    echo "..." | bangla-ai tokenize -
    bangla-ai sentiment "আজকের দিনটি অসাধারণ ছিল!" --backend openai
"""

from __future__ import annotations
import argparse
import json
import sys

from . import text, __version__


def _read_text(value: str) -> str:
    """Return the argument, or read stdin when it is '-'."""
    if value == "-":
        return sys.stdin.read().strip()
    return value


def _make_ai(args):
    from .core import BanglaAI
    kwargs = {}
    if args.api_key:
        kwargs["api_key"] = args.api_key
    if args.model:
        kwargs["model"] = args.model
    return BanglaAI(backend=args.backend, **kwargs)


def _print(obj) -> None:
    if isinstance(obj, str):
        print(obj)
    else:
        print(json.dumps(obj, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bangla-ai", description="Bengali NLP toolkit CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_text_cmd(name, help_):
        p = sub.add_parser(name, help=help_)
        p.add_argument("text", help="input text, or '-' to read stdin")
        return p

    add_text_cmd("normalize", "normalize Bengali Unicode text")
    add_text_cmd("tokenize", "tokenize into words")
    add_text_cmd("stem", "stem each token")

    p_translit = add_text_cmd("translit", "transliterate between scripts")
    p_translit.add_argument("--to", choices=["latin", "bengali"], required=True)

    p_digits = add_text_cmd("digits", "convert digit glyphs")
    p_digits.add_argument("--to", choices=["en", "bn"], required=True)

    # ML commands share backend options
    def add_ml_cmd(name, help_):
        p = sub.add_parser(name, help=help_)
        p.add_argument("text", help="input text, or '-' to read stdin")
        p.add_argument("--backend", default="transformers", help="transformers (default) or openai")
        p.add_argument("--api-key", default=None)
        p.add_argument("--model", default=None)
        return p

    p_sum = add_ml_cmd("summarize", "summarize a passage")
    p_sum.add_argument("--max-sentences", type=int, default=3)

    p_qa = add_ml_cmd("qa", "answer a question from context")
    p_qa.add_argument("--question", required=True)

    add_ml_cmd("sentiment", "classify sentiment")
    add_ml_cmd("ner", "extract named entities")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    body = _read_text(args.text)

    if args.command == "normalize":
        _print(text.normalize(body))
    elif args.command == "tokenize":
        _print(text.tokenize(body))
    elif args.command == "stem":
        _print(text.stem_tokens(text.tokenize(body)))
    elif args.command == "translit":
        _print(text.to_latin(body) if args.to == "latin" else text.to_bengali(body))
    elif args.command == "digits":
        _print(text.to_english_digits(body) if args.to == "en" else text.to_bengali_digits(body))
    elif args.command == "summarize":
        _print(_make_ai(args).summarize(body, max_sentences=args.max_sentences))
    elif args.command == "qa":
        _print(_make_ai(args).qa(body, args.question))
    elif args.command == "sentiment":
        _print(_make_ai(args).sentiment(body))
    elif args.command == "ner":
        _print(_make_ai(args).ner(body))
    else:  # pragma: no cover - argparse enforces a valid command
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
