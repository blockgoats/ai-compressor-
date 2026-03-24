# Ramanujan Compression SDK

This directory is the **Python package** shipped in the **Ramj** monorepo: compression libraries plus the **FastAPI** service (package name **`app`**, path `backend/app/`).

| Doc | Use when |
|-----|----------|
| [**BACKEND.md**](BACKEND.md) | Running the API locally, Docker, routes, env, venv troubleshooting |
| [**PROJECT_SUMMARY.md**](PROJECT_SUMMARY.md) | SDK layout, strategies, CLI, tests |
| [**docs/API_REFERENCE.md**](docs/API_REFERENCE.md) | Python module API |
| [Root README](../README.md) | Full stack with `frontend/` |
| [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) | How backend and frontend connect |

---

Ramanujan-inspired compression with HuggingFace tokenizer integration, suitable as a drop-in alongside BERT-style tokenizers.

## Features

- Ramanujan-inspired compression (modular / sparse / hybrid strategies)
- HuggingFace-compatible tokenizer integration
- Optional Pro tier (GPU, licensing) via extras
- CLI for batch and benchmarking

## Installation (from PyPI)

```bash
pip install ramanujan-tokenizer
# optional Pro extras:
pip install ramanujan-tokenizer[pro]
```

## Development install (this repo)

From the repository root:

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install -r requirements-api.txt
```

Or run `./scripts/dev-setup.sh` — see [BACKEND.md](BACKEND.md).

## Quick usage

```python
from ramanujan_tokenizer import RamanujanTokenizerFast

tokenizer = RamanujanTokenizerFast.from_pretrained("bert-base-uncased")
tokens = tokenizer.encode("This is a test sentence.")
text = tokenizer.decode(tokens)
```

```bash
ramanujan-cli compress input.txt --output compressed.json
```

## Package layout

- `ramanujan_compression/` — core algorithms  
- `ramanujan_tokenizer/` — HuggingFace integration  
- `ramanujan_pro/` — Pro extensions  
- `ramanujan_cli/` — CLI  
- `app/` — FastAPI application (HTTP API)

## License

MIT — see [LICENSE](LICENSE). Pro tier may add separate commercial terms.

## Contributing

See the repository [Contributing guide](../CONTRIBUTING.md).
