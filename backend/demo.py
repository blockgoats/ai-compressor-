#!/usr/bin/env python3
"""
Ramanujan Compression SDK - Demonstration Script

This script demonstrates the key features and capabilities of the SDK.
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_basic_compression():
    """Demonstrate basic compression capabilities."""
    print("🔬 Basic Compression Demo")
    print("-" * 40)
    
    from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy
    
    # Create sample data
    tokens = list(range(1, 101))  # 1 to 100
    print(f"Original tokens: {len(tokens)} items")
    print(f"Sample: {tokens[:10]}...")
    
    # Test different strategies
    strategies = [
        (CompressionStrategy.FOURIER_LIKE, "Fourier-like"),
        (CompressionStrategy.SPARSE_MODULAR, "Sparse Modular"),
        (CompressionStrategy.HYBRID, "Hybrid"),
    ]
    
    for strategy, name in strategies:
        config = CompressionConfig(strategy=strategy, compression_ratio=0.3)
        compressor = RamanujanCompressor(config)
        
        # Time the compression
        start_time = time.time()
        compressed_data = compressor.compress(tokens)
        compress_time = time.time() - start_time
        
        # Time the decompression
        start_time = time.time()
        decompressed = compressor.decompress(compressed_data)
        decompress_time = time.time() - start_time
        
        # Calculate statistics
        ratio = compressed_data['metadata']['compression_ratio']
        space_saved = (1 - ratio) * 100
        
        print(f"\n{name:15}:")
        print(f"  Compression ratio: {ratio:.3f}")
        print(f"  Space saved: {space_saved:.1f}%")
        print(f"  Compress time: {compress_time:.4f}s")
        print(f"  Decompress time: {decompress_time:.4f}s")
        print(f"  Tokens restored: {len(decompressed)}")
    
    print()

def demo_configuration_options():
    """Demonstrate configuration options."""
    print("⚙️  Configuration Options Demo")
    print("-" * 40)
    
    from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy
    
    tokens = list(range(50))
    
    # Test different compression ratios
    print("Testing different compression ratios:")
    ratios = [0.2, 0.5, 0.8]
    for ratio in ratios:
        config = CompressionConfig(compression_ratio=ratio)
        compressor = RamanujanCompressor(config)
        result = compressor.compress(tokens)
        actual_ratio = result['metadata']['compression_ratio']
        print(f"  Target: {ratio:.1f}, Actual: {actual_ratio:.3f}")
    
    # Test different modular bases
    print("\nTesting different modular bases:")
    bases = [5, 7, 11, 13]
    for base in bases:
        config = CompressionConfig(
            strategy=CompressionStrategy.SPARSE_MODULAR,
            modular_base=base
        )
        compressor = RamanujanCompressor(config)
        result = compressor.compress(tokens)
        ratio = result['metadata']['compression_ratio']
        print(f"  Base {base:2d}: {ratio:.3f} compression ratio")
    
    print()

def demo_compression_quality():
    """Demonstrate compression quality."""
    print("📊 Compression Quality Demo")
    print("-" * 40)
    
    from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy
    from ramanujan_compression.utils import validate_compression
    
    # Test with different data patterns
    test_cases = [
        ("Sequential", list(range(1, 51))),
        ("Random", [42, 17, 8, 91, 3, 67, 25, 84, 12, 56] * 5),
        ("Repeated", [1, 2, 3, 1, 2, 3, 1, 2, 3] * 10),
        ("Sparse", [0, 0, 0, 100, 0, 0, 0, 200, 0, 0] * 5),
    ]
    
    for name, tokens in test_cases:
        config = CompressionConfig(strategy=CompressionStrategy.HYBRID)
        compressor = RamanujanCompressor(config)
        
        # Compress and decompress
        compressed_data = compressor.compress(tokens)
        decompressed = compressor.decompress(compressed_data)
        
        # Validate compression
        is_valid = validate_compression(tokens, compressed_data, decompressed)
        
        # Calculate quality metrics
        ratio = compressed_data['metadata']['compression_ratio']
        space_saved = (1 - ratio) * 100
        
        print(f"{name:12}: {ratio:.3f} ratio, {space_saved:.1f}% saved, Valid: {is_valid}")
    
    print()

def demo_performance():
    """Demonstrate performance characteristics."""
    print("🚀 Performance Demo")
    print("-" * 40)
    
    from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy
    
    # Test with different data sizes
    sizes = [100, 500, 1000, 5000]
    
    for size in sizes:
        tokens = list(range(size))
        
        config = CompressionConfig(strategy=CompressionStrategy.HYBRID)
        compressor = RamanujanCompressor(config)
        
        # Time compression
        start_time = time.time()
        compressed_data = compressor.compress(tokens)
        compress_time = time.time() - start_time
        
        # Time decompression
        start_time = time.time()
        decompressed = compressor.decompress(compressed_data)
        decompress_time = time.time() - start_time
        
        # Calculate throughput
        compress_throughput = size / compress_time
        decompress_throughput = size / decompress_time
        
        ratio = compressed_data['metadata']['compression_ratio']
        
        print(f"Size {size:4d}: {compress_throughput:6.0f} tokens/s compress, "
              f"{decompress_throughput:6.0f} tokens/s decompress, "
              f"{ratio:.3f} ratio")
    
    print()

def demo_utility_functions():
    """Demonstrate utility functions."""
    print("🛠️  Utility Functions Demo")
    print("-" * 40)
    
    from ramanujan_compression.utils import (
        create_sample_tokens, 
        validate_compression,
        setup_logging
    )
    from ramanujan_compression import RamanujanCompressor
    
    # Create sample tokens
    print("Creating sample tokens...")
    sample_tokens = create_sample_tokens(100, 1000)
    print(f"Generated {len(sample_tokens)} sample tokens")
    print(f"Range: {min(sample_tokens)} to {max(sample_tokens)}")
    
    # Test compression validation
    print("\nTesting compression validation...")
    compressor = RamanujanCompressor()
    compressed_data = compressor.compress(sample_tokens)
    decompressed = compressor.decompress(compressed_data)
    
    is_valid = validate_compression(sample_tokens, compressed_data, decompressed)
    print(f"Compression validation: {'✓ Passed' if is_valid else '✗ Failed'}")
    
    # Setup logging
    print("\nSetting up logging...")
    setup_logging("INFO")
    print("Logging configured")
    
    print()

def main():
    """Run all demonstrations."""
    print("🎯 Ramanujan Compression SDK - Feature Demonstration")
    print("=" * 60)
    print()
    
    try:
        demo_basic_compression()
        demo_configuration_options()
        demo_compression_quality()
        demo_performance()
        demo_utility_functions()
        
        print("🎉 All demonstrations completed successfully!")
        print("\nThe Ramanujan Compression SDK is ready for use!")
        print("\nNext steps:")
        print("1. Install with: pip install -e .")
        print("2. Try the CLI: python -m ramanujan_cli.main --help")
        print("3. Check examples: python examples/basic_usage.py")
        print("4. Run tests: python test_basic.py")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())