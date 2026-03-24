"""
Ramanujan CLI - Main Entry Point

Command-line interface for Ramanujan compression operations.
"""

import click
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional, List

from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy, benchmark_compression
from ramanujan_tokenizer import RamanujanTokenizerFast, RamanujanTokenizerConfig

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--quiet', '-q', is_flag=True, help='Suppress output except errors')
def cli(verbose: bool, quiet: bool):
    """Ramanujan Compression CLI - Advanced token compression tools."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif quiet:
        logging.getLogger().setLevel(logging.ERROR)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--strategy', '-s', 
              type=click.Choice(['fourier_like', 'sparse_modular', 'hybrid']),
              default='hybrid', help='Compression strategy')
@click.option('--ratio', '-r', type=float, default=0.5, help='Compression ratio (0.0-1.0)')
@click.option('--modular-base', '-m', type=int, default=7, help='Modular base for arithmetic')
@click.option('--sparse-threshold', '-t', type=float, default=0.1, help='Sparse filtering threshold')
@click.option('--format', '-f', type=click.Choice(['json', 'binary']), default='json', help='Output format')
def compress(input_file: str, output: Optional[str], strategy: str, ratio: float, 
            modular_base: int, sparse_threshold: float, format: str):
    """Compress a text file using Ramanujan compression."""
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        click.echo(f"Error reading input file: {e}", err=True)
        sys.exit(1)
    
    # Create compressor
    config = CompressionConfig(
        strategy=CompressionStrategy(strategy),
        compression_ratio=ratio,
        modular_base=modular_base,
        sparse_threshold=sparse_threshold,
    )
    compressor = RamanujanCompressor(config)
    
    # Convert text to tokens (simple word-based tokenization for demo)
    tokens = text.split()
    token_ids = [hash(word) % 10000 for word in tokens]  # Simple tokenization
    
    # Compress
    try:
        compressed_data = compressor.compress(token_ids)
        
        # Prepare output
        if output is None:
            output = f"{input_file}.compressed.{format}"
        
        if format == 'json':
            # Add metadata for decompression
            output_data = {
                "original_text": text,
                "original_tokens": tokens,
                "compressed_data": compressed_data,
                "config": {
                    "strategy": strategy,
                    "ratio": ratio,
                    "modular_base": modular_base,
                    "sparse_threshold": sparse_threshold,
                }
            }
            
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
        else:
            # Binary format (simplified)
            import pickle
            with open(output, 'wb') as f:
                pickle.dump(compressed_data, f)
        
        # Show statistics
        stats = compressor.get_compression_stats(token_ids, compressed_data)
        click.echo(f"Compression completed!")
        click.echo(f"Original size: {stats['original_length']} tokens")
        click.echo(f"Compressed size: {stats['compressed_length']} tokens")
        click.echo(f"Compression ratio: {stats['compression_ratio']:.3f}")
        click.echo(f"Space saved: {stats['space_saved']:.1%}")
        click.echo(f"Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"Compression failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'binary']), default='json', help='Input format')
def decompress(input_file: str, output: Optional[str], format: str):
    """Decompress a compressed file."""
    
    try:
        if format == 'json':
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            compressed_data = data["compressed_data"]
            config_dict = data.get("config", {})
            
            # Recreate compressor with original config
            config = CompressionConfig(
                strategy=CompressionStrategy(config_dict.get("strategy", "hybrid")),
                compression_ratio=config_dict.get("ratio", 0.5),
                modular_base=config_dict.get("modular_base", 7),
                sparse_threshold=config_dict.get("sparse_threshold", 0.1),
            )
        else:
            # Binary format
            import pickle
            with open(input_file, 'rb') as f:
                compressed_data = pickle.load(f)
            
            # Use default config for binary format
            config = CompressionConfig()
        
        compressor = RamanujanCompressor(config)
        
        # Decompress
        decompressed_tokens = compressor.decompress(compressed_data)
        
        # Convert back to text (simplified)
        if format == 'json' and "original_tokens" in data:
            # Use original token mapping
            token_to_word = {hash(word) % 10000: word for word in data["original_tokens"]}
            words = [token_to_word.get(token_id, f"<UNK_{token_id}>") for token_id in decompressed_tokens]
            text = " ".join(words)
        else:
            # Fallback to token IDs
            text = " ".join(map(str, decompressed_tokens))
        
        # Write output
        if output is None:
            output = f"{input_file}.decompressed.txt"
        
        with open(output, 'w', encoding='utf-8') as f:
            f.write(text)
        
        click.echo(f"Decompression completed!")
        click.echo(f"Restored {len(decompressed_tokens)} tokens")
        click.echo(f"Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"Decompression failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--model', '-m', default='bert-base-uncased', help='HuggingFace model name')
@click.option('--dataset', '-d', type=click.Choice(['wiki', 'news', 'custom']), 
              default='wiki', help='Dataset for benchmarking')
@click.option('--samples', '-n', type=int, default=100, help='Number of samples to test')
@click.option('--strategy', '-s', 
              type=click.Choice(['fourier_like', 'sparse_modular', 'hybrid']),
              default='hybrid', help='Compression strategy')
@click.option('--ratio', '-r', type=float, default=0.5, help='Compression ratio')
@click.option('--output', '-o', type=click.Path(), help='Save benchmark results to file')
def benchmark(model: str, dataset: str, samples: int, strategy: str, ratio: float, output: Optional[str]):
    """Benchmark compression performance."""
    
    click.echo(f"Benchmarking {model} with {dataset} dataset...")
    
    try:
        # Load tokenizer
        tokenizer = RamanujanTokenizerFast.from_pretrained(model)
        
        # Generate test data
        test_texts = _generate_test_data(dataset, samples)
        
        # Tokenize texts
        test_tokens = []
        for text in test_texts:
            tokens = tokenizer.encode(text, add_special_tokens=True)
            if isinstance(tokens, list):
                test_tokens.append(tokens)
            else:
                test_tokens.append(tokens.tolist())
        
        # Create compressor
        config = CompressionConfig(
            strategy=CompressionStrategy(strategy),
            compression_ratio=ratio,
        )
        compressor = RamanujanCompressor(config)
        
        # Run benchmark
        results = benchmark_compression(compressor, test_tokens, iterations=3)
        
        # Display results
        click.echo("\n" + "="*50)
        click.echo("BENCHMARK RESULTS")
        click.echo("="*50)
        click.echo(f"Model: {model}")
        click.echo(f"Dataset: {dataset}")
        click.echo(f"Samples: {samples}")
        click.echo(f"Strategy: {strategy}")
        click.echo(f"Compression Ratio: {results.compression_ratio:.3f}")
        click.echo(f"Compression Time: {results.compression_time:.3f}s")
        click.echo(f"Decompression Time: {results.decompression_time:.3f}s")
        click.echo(f"Memory Usage: {results.memory_usage:.2f} MB")
        click.echo(f"Quality Score: {results.quality_score:.3f}")
        click.echo("="*50)
        
        # Save results if requested
        if output:
            results_dict = {
                "model": model,
                "dataset": dataset,
                "samples": samples,
                "strategy": strategy,
                "compression_ratio": results.compression_ratio,
                "compression_time": results.compression_time,
                "decompression_time": results.decompression_time,
                "memory_usage": results.memory_usage,
                "quality_score": results.quality_score,
            }
            
            with open(output, 'w') as f:
                json.dump(results_dict, f, indent=2)
            
            click.echo(f"Results saved to: {output}")
        
    except Exception as e:
        click.echo(f"Benchmark failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('text', type=str)
@click.option('--model', '-m', default='bert-base-uncased', help='HuggingFace model name')
@click.option('--strategy', '-s', 
              type=click.Choice(['fourier_like', 'sparse_modular', 'hybrid']),
              default='hybrid', help='Compression strategy')
@click.option('--ratio', '-r', type=float, default=0.5, help='Compression ratio')
def tokenize(text: str, model: str, strategy: str, ratio: float):
    """Tokenize text with compression."""
    
    try:
        # Load tokenizer
        config = RamanujanTokenizerConfig(
            base_tokenizer_name=model,
            compression_strategy=strategy,
            compression_ratio=ratio,
        )
        tokenizer = RamanujanTokenizerFast.from_pretrained(model, config=config)
        
        # Tokenize
        tokens = tokenizer.encode(text)
        
        # Decode back
        decoded = tokenizer.decode(tokens)
        
        # Show results
        click.echo(f"Original text: {text}")
        click.echo(f"Token IDs: {tokens}")
        click.echo(f"Decoded text: {decoded}")
        
        # Show compression stats
        stats = tokenizer.get_compression_stats()
        if stats:
            click.echo(f"Compression strategy: {stats['strategy']}")
            click.echo(f"Compression ratio: {stats['compression_ratio']}")
        
    except Exception as e:
        click.echo(f"Tokenization failed: {e}", err=True)
        sys.exit(1)


def _generate_test_data(dataset: str, samples: int) -> List[str]:
    """Generate test data for benchmarking."""
    
    if dataset == 'wiki':
        # Generate Wikipedia-style text
        return [
            f"This is sample text {i} for benchmarking the Ramanujan compression algorithm. "
            f"It contains various words and phrases to test the compression effectiveness. "
            f"Sample {i} includes technical terms and common language patterns."
            for i in range(samples)
        ]
    elif dataset == 'news':
        # Generate news-style text
        return [
            f"Breaking news sample {i}: Scientists have discovered new compression techniques "
            f"inspired by mathematical principles. The research shows significant improvements "
            f"in data compression ratios while maintaining high quality reconstruction."
            for i in range(samples)
        ]
    else:  # custom
        # Generate custom text
        return [
            f"Custom sample {i} with random content for testing compression algorithms. "
            f"This text contains various patterns and structures to evaluate performance."
            for i in range(samples)
        ]


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()