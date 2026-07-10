# file-integrity-monitor (FIM)

Ferramenta defensiva de linha de comando que monitora a integridade de
arquivos por meio de hashes SHA-256. Ela cria um **baseline** de hashes e,
posteriormente, detecta modificações, criações e remoções comparando o
estado atual com esse baseline.

## ⚠️ Aviso ético

Esta é uma ferramenta **defensiva e educacional**. Ela serve para detectar
alterações em sistemas **de sua propriedade ou nos quais você tenha
autorização explícita** para monitorar. Não a utilize para inspecionar
arquivos de terceiros sem permissão. O autor não se responsabiliza por uso
inadequado.

## Requisitos

- Python 3.10+
- Apenas biblioteca padrão (sem dependências externas).

## Instalação

```bash
pip install -e .
```

## Uso

Criar um baseline de arquivos/diretórios:

```bash
fim init /etc /home/voce/documentos
```

O baseline é salvo em `.fim-baseline.json` (use `-o` para outro caminho).

Verificar alterações (retorna código 1 se houver diferenças):

```bash
fim check
```

Mostrar diferenças em JSON:

```bash
fim diff
```

## Como funciona

1. `init` percorre os caminhos informados (arquivos ou diretórios) e armazena
   o hash SHA-256 de cada arquivo em um JSON.
2. `check`/`diff` recalcula os hashes e os compara com o baseline,
   classificando cada arquivo em `modified`, `added` ou `removed`.

## Testes

```bash
pytest
```

## Licença

MIT — Copyright (c) 2026 Diogo Damasceno.
