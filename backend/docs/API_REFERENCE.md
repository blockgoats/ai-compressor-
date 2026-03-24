# Ramanujan Compression SDK - API Reference

## Core Compression Module (`ramanujan_compression`)

### RamanujanCompressor

The main compression class that implements Ramanujan-inspired compression algorithms.

#### Constructor
```python
RamanujanCompressor(config: Optional[CompressionConfig] = None)
```

**Parameters:**
- `config`: Compression configuration object. If None, uses default configuration.

#### Methods

##### `compress(tokens: List[int]) -> Dict[str, Any]`
Compress a list of token IDs.

**Parameters:**
- `tokens`: List of token IDs to compress

**Returns:**
- Dictionary containing:
  - `compressed`: List of compressed token IDs
  - `metadata`: Dictionary with compression statistics

**Example:**
```python
compressor = RamanujanCompressor()
tokens = [1, 2, 3, 4, 5]
result = compressor.compress(tokens)
print(f"Compression ratio: {result['metadata']['compression_ratio']:.3f}")
```

##### `decompress(compressed_data: Dict[str, Any]) -> List[int]`
Decompress compressed data back to tokens.

**Parameters:**
- `compressed_data`: Dictionary containing compressed data and metadata

**Returns:**
- List of decompressed token IDs

**Example:**
```python
decompressed = compressor.decompress(result)
print(f"Decompressed tokens: {decompressed}")
```

##### `get_compression_stats(original_tokens: List[int], compressed_data: Dict[str, Any]) -> Dict[str, float]`
Get detailed compression statistics.

**Returns:**
- Dictionary with statistics:
  - `original_length`: Number of original tokens
  - `compressed_length`: Number of compressed tokens
  - `compression_ratio`: Compression ratio (0.0-1.0)
  - `space_saved`: Percentage of space saved
  - `bits_per_token`: Average bits per token

### CompressionConfig

Configuration class for compression algorithms.

#### Constructor
```python
CompressionConfig(
    strategy: CompressionStrategy = CompressionStrategy.HYBRID,
    compression_ratio: float = 0.5,
    modular_base: int = 7,
    sparse_threshold: float = 0.1,
    context_length: int = 512,
    gpu_acceleration: bool = False
)
```

**Parameters:**
- `strategy`: Compression strategy to use
- `compression_ratio`: Target compression ratio (0.0-1.0)
- `modular_base`: Base for modular arithmetic
- `sparse_threshold`: Threshold for sparse filtering
- `context_length`: Context window length
- `gpu_acceleration`: Enable GPU acceleration (Pro tier)

### CompressionStrategy

Enumeration of available compression strategies.

**Values:**
- `FOURIER_LIKE`: Frequency domain compression
- `SPARSE_MODULAR`: Sparse modular arithmetic compression
- `HYBRID`: Adaptive combination of strategies

## HuggingFace Integration (`ramanujan_tokenizer`)

### RamanujanTokenizerFast

HuggingFace-compatible tokenizer with compression capabilities.

#### Constructor
```python
RamanujanTokenizerFast(
    base_tokenizer: Optional[PreTrainedTokenizerFast] = None,
    config: Optional[RamanujanTokenizerConfig] = None,
    **kwargs
)
```

#### Class Methods

##### `from_pretrained(pretrained_model_name_or_path: str, config: Optional[RamanujanTokenizerConfig] = None, **kwargs)`
Load tokenizer from pretrained model.

**Parameters:**
- `pretrained_model_name_or_path`: Path to pretrained model
- `config`: Optional configuration override
- `**kwargs`: Additional arguments

**Example:**
```python
tokenizer = RamanujanTokenizerFast.from_pretrained("bert-base-uncased")
```

#### Methods

##### `encode(text: Union[str, List[str]], **kwargs) -> Union[List[int], torch.Tensor]`
Encode text with optional compression.

**Parameters:**
- `text`: Text to encode
- `**kwargs`: Additional encoding arguments

**Returns:**
- Encoded tokens (with compression if enabled)

##### `decode(token_ids: Union[int, List[int], torch.Tensor], **kwargs) -> str`
Decode tokens with optional decompression.

**Parameters:**
- `token_ids`: Token IDs to decode
- `**kwargs`: Additional decoding arguments

**Returns:**
- Decoded text

##### `batch_encode_plus(batch_text_or_text_pairs: Union[List[str], List[Tuple[str, str]]], **kwargs) -> BatchEncoding`
Batch encode with optional compression.

**Parameters:**
- `batch_text_or_text_pairs`: Batch of texts or text pairs
- `**kwargs`: Additional encoding arguments

**Returns:**
- BatchEncoding with compressed tokens

##### `get_compression_stats() -> Optional[Dict[str, Any]]`
Get compression statistics if available.

**Returns:**
- Dictionary with compression statistics or None

##### `enable_compression(enable: bool = True)`
Enable or disable compression.

**Parameters:**
- `enable`: Whether to enable compression

##### `set_compression_config(config: CompressionConfig)`
Update compression configuration.

**Parameters:**
- `config`: New compression configuration

### RamanujanTokenizerConfig

Configuration class for Ramanujan tokenizer.

#### Constructor
```python
RamanujanTokenizerConfig(
    base_tokenizer_name: str = "bert-base-uncased",
    base_tokenizer_config: Optional[Dict[str, Any]] = None,
    compression_config: Optional[CompressionConfig] = None,
    enable_compression: bool = True,
    compression_strategy: str = "hybrid",
    compression_ratio: float = 0.5,
    modular_base: int = 7,
    sparse_threshold: float = 0.1,
    context_length: int = 512,
    gpu_acceleration: bool = False,
    pro_features: bool = False,
    max_length: int = 512,
    padding: str = "max_length",
    truncation: bool = True,
    return_tensors: str = "pt"
)
```

## Pro Tier Extensions (`ramanujan_pro`)

### ProCompressor

Professional tier compressor with advanced features.

#### Constructor
```python
ProCompressor(
    config: Optional[ProCompressionConfig] = None,
    api_key: Optional[str] = None,
    license_key: Optional[str] = None
)
```

**Parameters:**
- `config`: Pro compression configuration
- `api_key`: API key for Pro features
- `license_key`: License key for validation

#### Methods

##### `compress(tokens: List[int], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`
Advanced compression with Pro features.

##### `decompress(compressed_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> List[int]`
Advanced decompression with Pro features.

##### `batch_compress(token_batches: List[List[int]], parallel: bool = True) -> List[Dict[str, Any]]`
Batch compression with parallel processing.

##### `get_pro_stats() -> Dict[str, Any]`
Get Pro compressor statistics and capabilities.

##### `validate_license() -> bool`
Validate Pro license.

##### `upgrade_license(new_license_key: str) -> bool`
Upgrade to new license.

### GPUCompressor

GPU-accelerated compressor for high-performance applications.

#### Constructor
```python
GPUCompressor(config: Optional[CompressionConfig] = None, device: str = "cuda")
```

**Parameters:**
- `config`: Compression configuration
- `device`: CUDA device to use

#### Methods

##### `batch_compress(token_batches: List[List[int]]) -> List[Dict[str, Any]]`
Batch compression using GPU acceleration.

##### `get_gpu_info() -> Dict[str, Any]`
Get GPU information and capabilities.

## CLI Tool (`ramanujan-cli`)

### Commands

#### `compress`
Compress a text file using Ramanujan compression.

```bash
ramanujan-cli compress input.txt --output compressed.json --strategy hybrid --ratio 0.5
```

**Options:**
- `--output, -o`: Output file path
- `--strategy, -s`: Compression strategy (fourier_like, sparse_modular, hybrid)
- `--ratio, -r`: Compression ratio (0.0-1.0)
- `--modular-base, -m`: Modular base for arithmetic
- `--sparse-threshold, -t`: Sparse filtering threshold
- `--format, -f`: Output format (json, binary)

#### `decompress`
Decompress a compressed file.

```bash
ramanujan-cli decompress compressed.json --output restored.txt
```

**Options:**
- `--output, -o`: Output file path
- `--format, -f`: Input format (json, binary)

#### `benchmark`
Benchmark compression performance.

```bash
ramanujan-cli benchmark --model bert-base-uncased --dataset wiki --samples 100
```

**Options:**
- `--model, -m`: HuggingFace model name
- `--dataset, -d`: Dataset for benchmarking (wiki, news, custom)
- `--samples, -n`: Number of samples to test
- `--strategy, -s`: Compression strategy
- `--ratio, -r`: Compression ratio
- `--output, -o`: Save benchmark results to file

#### `tokenize`
Tokenize text with compression.

```bash
ramanujan-cli tokenize "This is a test sentence" --model bert-base-uncased --strategy hybrid
```

**Options:**
- `--model, -m`: HuggingFace model name
- `--strategy, -s`: Compression strategy
- `--ratio, -r`: Compression ratio

## Utility Functions

### `benchmark_compression(compressor, test_tokens: List[List[int]], iterations: int = 3) -> BenchmarkResult`
Benchmark compression performance.

### `save_compression_config(config, filepath: str)`
Save compression configuration to file.

### `load_compression_config(filepath: str) -> CompressionConfig`
Load compression configuration from file.

### `create_sample_tokens(length: int = 100, vocab_size: int = 1000) -> List[int]`
Create sample token sequence for testing.

### `validate_compression(original: List[int], compressed_data: Dict[str, Any], decompressed: List[int]) -> bool`
Validate compression/decompression round-trip.

### `setup_logging(level: str = "INFO")`
Setup logging configuration.