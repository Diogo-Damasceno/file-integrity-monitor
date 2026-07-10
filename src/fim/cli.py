"""Interface de linha de comando do file-integrity-monitor."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from fim.core import build_baseline, compare

BASELINE_FILE = ".fim-baseline.json"


def _load_baseline(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _save_baseline(path: Path, baseline: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(baseline, fh, indent=2, sort_keys=True)


def cmd_init(args: argparse.Namespace) -> int:
    baseline = build_baseline(args.paths)
    target = Path(args.output)
    _save_baseline(target, baseline)
    print(f"Baseline criado com {len(baseline)} arquivo(s) em {target}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    baseline_path = Path(args.baseline)
    baseline = _load_baseline(baseline_path)
    paths = args.paths or list(baseline.keys())
    current = build_baseline(paths)
    diff = compare(baseline, current)
    total = len(diff["modified"]) + len(diff["added"]) + len(diff["removed"])
    if total == 0:
        print("OK: nenhuma alteracao detectada.")
        return 0
    for kind in ("modified", "added", "removed"):
        for item in diff[kind]:
            print(f"[{kind.upper()}] {item}")
    return 1


def cmd_diff(args: argparse.Namespace) -> int:
    baseline_path = Path(args.baseline)
    baseline = _load_baseline(baseline_path)
    current = build_baseline(args.paths or list(baseline.keys()))
    diff = compare(baseline, current)
    print(json.dumps(diff, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fim",
        description="Monitor de integridade de arquivos baseado em hashes SHA-256.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Cria um baseline de hashes.")
    p_init.add_argument("paths", nargs="+", help="Arquivos ou diretorios.")
    p_init.add_argument("-o", "--output", default=BASELINE_FILE, help="Arquivo de baseline.")
    p_init.set_defaults(func=cmd_init)

    p_check = sub.add_parser("check", help="Verifica alteracoes vs baseline.")
    p_check.add_argument("-b", "--baseline", default=BASELINE_FILE, help="Arquivo de baseline.")
    p_check.add_argument("paths", nargs="*", help="Caminhos a verificar (padrao: baseline).")
    p_check.set_defaults(func=cmd_check)

    p_diff = sub.add_parser("diff", help="Mostra diferencas em JSON.")
    p_diff.add_argument("-b", "--baseline", default=BASELINE_FILE, help="Arquivo de baseline.")
    p_diff.add_argument("paths", nargs="*", help="Caminhos a verificar (padrao: baseline).")
    p_diff.set_defaults(func=cmd_diff)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
