"""Núcleo do monitor de integridade: cálculo de hashes e comparação."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

CHUNK_SIZE = 65536
KIND_MODIFIED = "modified"
KIND_ADDED = "added"
KIND_REMOVED = "removed"


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


def _normalize(path: str) -> str:
    """Normaliza um caminho para a forma absoluta usada no baseline."""
    return os.path.abspath(path)


def _walk_files(root: str) -> list[str]:
    """Lista arquivos (caminhos absolutos) dentro de um diretório."""
    found = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            found.append(_normalize(os.path.join(dirpath, name)))
    return found


def collect_files(paths) -> list[str]:
    """Expande arquivos e diretórios em uma lista plana de caminhos."""
    collected = []
    for entry in paths:
        p = Path(entry)
        if p.is_dir():
            collected.extend(_walk_files(str(p)))
        elif p.is_file():
            collected.append(_normalize(str(p)))
    return collected


def build_baseline(paths) -> dict:
    """Percorre os caminhos e gera um dicionário path -> hash."""
    baseline = {}
    for full in collect_files(paths):
        baseline[full] = hash_file(full)
    return baseline


def compare(baseline: dict, current: dict) -> dict:
    """Compara baseline com estado atual e classifica as diferenças."""
    result = {KIND_MODIFIED: [], KIND_ADDED: [], KIND_REMOVED: []}
    baseline_keys = set(baseline.keys())
    current_keys = set(current.keys())

    for key in baseline_keys & current_keys:
        if baseline[key] != current[key]:
            result[KIND_MODIFIED].append(key)

    for key in current_keys - baseline_keys:
        result[KIND_ADDED].append(key)

    for key in baseline_keys - current_keys:
        result[KIND_REMOVED].append(key)

    return result
