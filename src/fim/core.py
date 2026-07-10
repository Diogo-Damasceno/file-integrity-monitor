"""Núcleo do monitor de integridade: cálculo de hashes e comparação."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

CHUNK_SIZE = 65536


def hash_file(path: str) -> str:
    """Retorna o hash SHA-256 do conteúdo de um arquivo."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(CHUNK_SIZE)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def build_baseline(paths) -> dict:
    """Percorre os caminhos e gera um dicionário path -> hash."""
    baseline = {}
    for entry in paths:
        p = Path(entry)
        if p.is_dir():
            for root, _dirs, files in os.walk(p):
                for name in files:
                    full = os.path.join(root, name)
                    baseline[os.path.abspath(full)] = hash_file(full)
        elif p.is_file():
            baseline[os.path.abspath(str(p))] = hash_file(str(p))
    return baseline


def compare(baseline: dict, current: dict) -> dict:
    """Compara baseline com estado atual e classifica as diferenças."""
    result = {"modified": [], "added": [], "removed": []}
    baseline_keys = set(baseline.keys())
    current_keys = set(current.keys())

    for key in baseline_keys & current_keys:
        if baseline[key] != current[key]:
            result["modified"].append(key)

    for key in current_keys - baseline_keys:
        result["added"].append(key)

    for key in baseline_keys - current_keys:
        result["removed"].append(key)

    return result
