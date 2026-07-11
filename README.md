# file-integrity-monitor

Ferramenta defensiva de linha de comando que monitora a integridade de
arquivos por meio de hashes SHA-256. Cria um **baseline** e, depois, detecta
modificações, criações e remoções comparando o estado atual com o baseline.

> ⚠️ Ferramenta **defensiva e educacional**. Detecta alterações em arquivos **seus**.

## Instalação

Pré-requisitos: **Python 3.10+**.

```bash
git clone https://github.com/Diogo-Damasceno/file-integrity-monitor.git
cd file-integrity-monitor
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

Após instalar, o comando do projeto fica disponível dentro do venv.
Para usar fora dele, crie um atalho:

```bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/.venv/bin/fim" ~/.local/bin/fim
```

> Dica: se `~/.local/bin` não estiver no teu `PATH`, rode
> `export PATH="$HOME/.local/bin:$PATH"` (e adicione ao `~/.bashrc`/`~/.zshrc`).


## Uso

```bash
# 1) cria o baseline de arquivos/diretorios
fim baseline /etc /home/diogo/docs

# 2) verifica se algo mudou desde o baseline
fim check

# 3) verifica caminhos especificos contra um baseline custom
fim check /etc --baseline /opt/fim/baseline.json
```

O baseline padrão fica em `~/.local/share/fim/baseline.json` (ou o informado
por `-o/--output`).

## Licença

MIT — veja `LICENSE`.
