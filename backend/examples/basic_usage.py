#!/usr/bin/env python3
"""
Basic Usage Examples for Ramanujan Compression SDK

This script demonstrates basic usage of the Ramanujan compression library
with HuggingFace tokenizers.
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy
from ramanujan_tokenizer import RamanujanTokenizerFast, RamanujanTokenizerConfig


def basic_compression_example():
    """Demonstrate basic compression functionality."""
    print("=== Basic Compression Example ===")
    
    # Create a compressor with default configuration
    compressor = RamanujanCompressor()
    
    # Sample token sequence
    tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    print(f"Original tokens: {tokens}")
    print(f"Original length: {len(tokens)}")
    
    # Compress the tokens
    compressed_data = compressor.compress(tokens)
    print(f"Compressed data: {compressed_data['compressed']}")
    print(f"Compressed length: {len(compressed_data['compressed'])}")
    print(f"Compression ratio: {compressed_data['metadata']['compression_ratio']:.3f}")
    
    # Decompress the tokens
    decompressed_tokens = compressor.decompress(compressed_data)
    print(f"Decompressed tokens: {decompressed_tokens}")
    print(f"Decompressed length: {len(decompressed_tokens)}")
    
    # Get compression statistics
    stats = compressor.get_compression_stats(tokens, compressed_data)
    print(f"Space saved: {stats['space_saved']:.1%}")
    print(f"Bits per token: {stats['bits_per_token']:.2f}")
    print()


def different_strategies_example():
    """Demonstrate different compression strategies."""
    print("=== Different Compression Strategies ===")
    
    tokens = list(range(100))  # 0 to 99
    print(f"Testing with {len(tokens)} tokens")
    
    strategies = [
        CompressionStrategy.FOURIER_LIKE,
        CompressionStrategy.SPARSE_MODULAR,
        CompressionStrategy.HYBRID,
    ]
    
    for strategy in strategies:
        config = CompressionConfig(strategy=strategy, compression_ratio=0.3)
        compressor = RamanujanCompressor(config)
        
        compressed_data = compressor.compress(tokens)
        ratio = compressed_data['metadata']['compression_ratio']
        
        print(f"{strategy.value:15}: {ratio:.3f} compression ratio")
    print()


def tokenizer_example():
    """Demonstrate HuggingFace tokenizer integration."""
    print("=== HuggingFace Tokenizer Integration ===")
    
    # Create tokenizer configuration
    config = RamanujanTokenizerConfig(
        base_tokenizer_name="bert-base-uncased",
        enable_compression=True,
        compression_strategy="hybrid",
        compression_ratio=0.4
    )
    
    try:
        # Initialize tokenizer
        tokenizer = RamanujanTokenizerFast(config=config)
        
        # Sample text
        text = "This is a test sentence for Ramanujan compression."
        print(f"Original text: {text}")
        
        # Encode with compression
        tokens = tokenizer.encode(text)
        print(f"Encoded tokens: {tokens}")
        print(f"Number of tokens: {len(tokens)}")
        
        # Decode back to text
        decoded_text = tokenizer.decode(tokens)
        print(f"Decoded text: {decoded_text}")
        
        # Get compression statistics
        stats = tokenizer.get_compression_stats()
        if stats:
            print(f"Compression strategy: {stats['strategy']}")
            print(f"Compression ratio: {stats['compression_ratio']}")
        
    except Exception as e:
        print(f"Tokenizer example failed (this is expected without transformers installed): {e}")
    print()


def batch_processing_example():
    """Demonstrate batch processing."""
    print("=== Batch Processing Example ===")
    
    compressor = RamanujanCompressor()
    
    # Multiple token sequences
    token_batches = [
        [1, 2, 3, 4, 5],
        [10, 20, 30, 40, 50],
        [100, 200, 300, 400, 500],
    ]
    
    print(f"Processing {len(token_batches)} token sequences")
    
    # Compress each batch
    compressed_batches = []
    for i, tokens in enumerate(token_batches):
        compressed_data = compressor.compress(tokens)
        compressed_batches.append(compressed_data)
        
        ratio = compressed_data['metadata']['compression_ratio']
        print(f"Batch {i+1}: {len(tokens)} -> {len(compressed_data['compressed'])} tokens (ratio: {ratio:.3f})")
    
    # Decompress each batch
    print("\nDecompressing batches:")
    for i, compressed_data in enumerate(compressed_batches):
        decompressed = compressor.decompress(compressed_data)
        print(f"Batch {i+1}: {len(decompressed)} tokens restored")
    print()


def configuration_example():
    """Demonstrate different configuration options."""
    print("=== Configuration Options ===")
    
    tokens = list(range(50))
    
    # Different compression ratios
    ratios = [0.2, 0.5, 0.8]
    print("Testing different compression ratios:")
    
    for ratio in ratios:
        config = CompressionConfig(compression_ratio=ratio)
        compressor = RamanujanCompressor(config)
        
        compressed_data = compressor.compress(tokens)
        actual_ratio = compressed_data['metadata']['compression_ratio']
        
        print(f"Target ratio: {ratio:.1f}, Actual ratio: {actual_ratio:.3f}")
    
    # Different modular bases
    print("\nTesting different modular bases:")
    bases = [5, 7, 11, 13]
    
    for base in bases:
        config = CompressionConfig(
            strategy=CompressionStrategy.SPARSE_MODULAR,
            modular_base=base
        )
        compressor = RamanujanCompressor(config)
        
        compressed_data = compressor.compress(tokens)
        ratio = compressed_data['metadata']['compression_ratio']
        
        print(f"Modular base {base:2d}: {ratio:.3f} compression ratio")
    print()


def main():
    """Run all examples."""
    print("Ramanujan Compression SDK - Basic Usage Examples")
    print("=" * 50)
    print()
    
    try:
        basic_compression_example()
        different_strategies_example()
        tokenizer_example()
        batch_processing_example()
        configuration_example()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()