#!/usr/bin/env python3
"""
Basic test script for Ramanujan Compression SDK
Tests core functionality without external dependencies
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_compression():
    """Test core compression functionality."""
    print("Testing core compression...")
    
    try:
        from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy
        
        # Test different strategies
        strategies = [
            CompressionStrategy.FOURIER_LIKE,
            CompressionStrategy.SPARSE_MODULAR,
            CompressionStrategy.HYBRID,
        ]
        
        test_tokens = list(range(50))  # 0 to 49
        print(f"Testing with {len(test_tokens)} tokens")
        
        for strategy in strategies:
            config = CompressionConfig(strategy=strategy, compression_ratio=0.3)
            compressor = RamanujanCompressor(config)
            
            # Compress
            compressed_data = compressor.compress(test_tokens)
            ratio = compressed_data['metadata']['compression_ratio']
            
            # Decompress
            decompressed = compressor.decompress(compressed_data)
            
            print(f"  {strategy.value:15}: {ratio:.3f} ratio, {len(decompressed)} tokens restored")
        
        print("✓ Core compression tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Core compression test failed: {e}")
        return False

def test_compression_config():
    """Test compression configuration."""
    print("\nTesting compression configuration...")
    
    try:
        from ramanujan_compression import CompressionConfig, CompressionStrategy
        
        # Test default config
        config1 = CompressionConfig()
        assert config1.strategy == CompressionStrategy.HYBRID
        assert config1.compression_ratio == 0.5
        
        # Test custom config
        config2 = CompressionConfig(
            strategy=CompressionStrategy.FOURIER_LIKE,
            compression_ratio=0.3,
            modular_base=11,
            sparse_threshold=0.05
        )
        assert config2.strategy == CompressionStrategy.FOURIER_LIKE
        assert config2.compression_ratio == 0.3
        assert config2.modular_base == 11
        
        print("✓ Configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_compression_stats():
    """Test compression statistics."""
    print("\nTesting compression statistics...")
    
    try:
        from ramanujan_compression import RamanujanCompressor
        
        compressor = RamanujanCompressor()
        tokens = list(range(100))
        
        compressed_data = compressor.compress(tokens)
        stats = compressor.get_compression_stats(tokens, compressed_data)
        
        assert 'original_length' in stats
        assert 'compressed_length' in stats
        assert 'compression_ratio' in stats
        assert 'space_saved' in stats
        assert 'bits_per_token' in stats
        
        assert stats['original_length'] == len(tokens)
        assert stats['compressed_length'] == len(compressed_data['compressed'])
        assert 0 <= stats['compression_ratio'] <= 1
        
        print(f"  Original: {stats['original_length']} tokens")
        print(f"  Compressed: {stats['compressed_length']} tokens")
        print(f"  Ratio: {stats['compression_ratio']:.3f}")
        print(f"  Space saved: {stats['space_saved']:.1%}")
        
        print("✓ Statistics tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Statistics test failed: {e}")
        return False

def test_utility_functions():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    try:
        from ramanujan_compression.utils import create_sample_tokens, validate_compression
        
        # Test sample token creation
        tokens = create_sample_tokens(50, 1000)
        assert len(tokens) == 50
        assert all(isinstance(t, int) for t in tokens)
        assert all(0 <= t < 1000 for t in tokens)
        
        # Test compression validation
        from ramanujan_compression import RamanujanCompressor
        compressor = RamanujanCompressor()
        
        compressed_data = compressor.compress(tokens)
        decompressed = compressor.decompress(compressed_data)
        
        is_valid = validate_compression(tokens, compressed_data, decompressed)
        assert is_valid
        
        print("✓ Utility function tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Utility function test failed: {e}")
        return False

def test_error_handling():
    """Test error handling."""
    print("\nTesting error handling...")
    
    try:
        from ramanujan_compression import RamanujanCompressor
        
        compressor = RamanujanCompressor()
        
        # Test empty input
        result = compressor.compress([])
        assert result['compressed'] == []
        assert result['metadata']['original_length'] == 0
        
        # Test single token
        result = compressor.compress([42])
        assert 'compressed' in result
        assert 'metadata' in result
        assert 'original_length' in result['metadata']
        assert result['metadata']['original_length'] == 1
        
        print("✓ Error handling tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Ramanujan Compression SDK - Basic Tests")
    print("=" * 50)
    
    tests = [
        test_core_compression,
        test_compression_config,
        test_compression_stats,
        test_utility_functions,
        test_error_handling,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The Ramanujan Compression SDK is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())