# Ramanujan Compression SDK — project summary

> **Monorepo:** This SDK and the FastAPI service live under **`backend/`** in the Ramj repository. For running the API and Docker, see [**BACKEND.md**](BACKEND.md). For the full stack (with **`frontend/`**), see the [root README](../README.md).

## Project overview

The **`backend/`** tree implements a **Ramanujan-inspired compression SDK** with HuggingFace tokenizer integration, usable as a drop-in alongside BERT-style tokenizers, plus an optional **HTTP API** (`backend/app/`).

## 🏗️ Architecture

### Core Components

1. **`ramanujan_compression/`** - Core compression algorithms
   - `compressor.py` - Main compression implementation
   - `utils.py` - Utility functions and benchmarking
   - Implements 3 compression strategies: Fourier-like, Sparse Modular, Hybrid

2. **`ramanujan_tokenizer/`** - HuggingFace integration
   - `tokenization_ramanujan.py` - HuggingFace-compatible tokenizer
   - `config.py` - Configuration management
   - Drop-in replacement for existing tokenizers

3. **`ramanujan_pro/`** - Professional tier extensions
   - `gpu_compressor.py` - GPU-accelerated compression
   - `pro_compressor.py` - Advanced Pro features
   - `licensing.py` - License validation system

4. **`ramanujan_cli/`** - Command-line interface
   - `main.py` - CLI tool for compression/decompression
   - Supports batch processing and benchmarking

## 🚀 Key Features

### Core Features
- **Ramanujan-inspired compression** using modular arithmetic and sparse filtering
- **HuggingFace-compatible** tokenizer interface
- **Multiple compression strategies** (Fourier, Sparse Modular, Hybrid)
- **Configurable compression ratios** and parameters
- **Comprehensive benchmarking** tools

### Pro Tier Features
- **GPU acceleration** with CUDA support
- **Encryption-enabled compression** for security
- **Parallel processing** for batch operations
- **Learned embeddings** for better compression
- **License validation** and feature access control

### CLI Features
- **File compression/decompression** with multiple formats
- **Performance benchmarking** with various models
- **Interactive tokenization** and testing
- **Batch processing** capabilities

## 📊 Compression Strategies

### 1. Fourier-like Compression
- Uses FFT for frequency domain analysis
- Keeps only significant frequencies
- Good for smooth, periodic data

### 2. Sparse Modular Compression
- Based on Ramanujan sums and modular arithmetic
- Applies sparse filtering using mathematical properties
- Good for structured, repetitive data

### 3. Hybrid Compression
- Adaptive combination of strategies
- Chooses best method based on data characteristics
- Provides robust compression across different data types

## 🔧 Usage Examples

### Basic Compression
```python
from ramanujan_compression import RamanujanCompressor

compressor = RamanujanCompressor()
tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
compressed_data = compressor.compress(tokens)
decompressed = compressor.decompress(compressed_data)
```

### HuggingFace Integration
```python
from ramanujan_tokenizer import RamanujanTokenizerFast

tokenizer = RamanujanTokenizerFast.from_pretrained("bert-base-uncased")
tokens = tokenizer.encode("This is a test sentence.")
text = tokenizer.decode(tokens)
```

### CLI Usage
```bash
# Compress a file
ramanujan-cli compress input.txt --output compressed.json

# Benchmark performance
ramanujan-cli benchmark --model bert-base-uncased --dataset wiki

# Tokenize text
ramanujan-cli tokenize "Test sentence" --strategy hybrid
```

## 📦 Installation

### Basic Installation
```bash
pip install ramanujan-tokenizer
```

### Pro Tier Installation
```bash
pip install ramanujan-tokenizer[pro]
```

### Development installation (this monorepo)
```bash
git clone https://github.com/YOUR_ORG/ramj.git   # or your fork
cd ramj/backend
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install -r requirements-api.txt
```

For database, Redis, and one-command setup, use `./scripts/dev-setup.sh` (see [BACKEND.md](BACKEND.md)).

## 🧪 Testing

### Run All Tests
```bash
python run_tests.py --all
```

### Run Specific Test Types
```bash
python run_tests.py --type unit
python run_tests.py --type pro
python run_tests.py --type gpu
```

### Run Examples
```bash
python run_tests.py --examples
```

## 📈 Performance

### Compression Ratios
- **Fourier-like**: 0.3-0.7 (depending on data characteristics)
- **Sparse Modular**: 0.2-0.8 (depending on modular base and sparsity)
- **Hybrid**: 0.2-0.6 (adaptive based on data analysis)

### Speed
- **CPU**: ~1000 tokens/second (varies by strategy)
- **GPU**: ~10000 tokens/second (with CUDA acceleration)
- **Memory**: Low memory footprint with configurable optimization

## 🔒 Licensing

### Free OSS Tier
- MIT License
- Basic compression features
- Community support

### Pro Tier
- Commercial license
- GPU acceleration
- Advanced features
- Priority support

### Enterprise Tier
- Custom licensing
- Source code access
- Dedicated support
- Custom integrations

## 🛠️ Development Status

### Completed Features ✅
- [x] Core compression algorithms
- [x] HuggingFace tokenizer integration
- [x] CLI tool implementation
- [x] Pro tier extensions
- [x] GPU acceleration
- [x] Comprehensive testing
- [x] Documentation and examples

### Future Enhancements 🚀
- [ ] Advanced learned embeddings
- [ ] Distributed compression
- [ ] Real-time streaming compression
- [ ] Integration with more ML frameworks
- [ ] Web API for cloud deployment

## 📁 Project Structure

```
ramanujan-tokenizer/
├── ramanujan_compression/     # Core compression module
│   ├── __init__.py
│   ├── compressor.py
│   └── utils.py
├── ramanujan_tokenizer/       # HuggingFace integration
│   ├── __init__.py
│   ├── tokenization_ramanujan.py
│   ├── config.py
│   └── tokenizer_config.json
├── ramanujan_pro/             # Pro tier extensions
│   ├── __init__.py
│   ├── gpu_compressor.py
│   ├── pro_compressor.py
│   └── licensing.py
├── ramanujan_cli/             # CLI tool
│   ├── __init__.py
│   └── main.py
├── tests/                     # Test suite
│   ├── test_compressor.py
│   └── test_tokenizer.py
├── examples/                  # Usage examples
│   └── basic_usage.py
├── docs/                      # Documentation
│   └── API_REFERENCE.md
├── setup.py                   # Package configuration
├── requirements.txt           # Dependencies
├── pytest.ini               # Test configuration
├── run_tests.py             # Test runner
└── README.md                # Project documentation
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
1. Clone the repository
2. Install in development mode: `pip install -e .`
3. Install development dependencies: `pip install -e .[dev]`
4. Run tests: `python run_tests.py --all`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the mathematical work of Srinivasa Ramanujan
- Built on top of HuggingFace Transformers
- GPU acceleration powered by PyTorch and CuPy