"""
Tests for Ramanujan Compressor
"""

import pytest
import numpy as np
from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy


class TestRamanujanCompressor:
    """Test cases for RamanujanCompressor."""
    
    def test_compressor_initialization(self):
        """Test compressor initialization."""
        config = CompressionConfig()
        compressor = RamanujanCompressor(config)
        assert compressor.config == config
    
    def test_compressor_default_config(self):
        """Test compressor with default config."""
        compressor = RamanujanCompressor()
        assert compressor.config is not None
        assert compressor.config.strategy == CompressionStrategy.HYBRID
    
    def test_compress_empty_tokens(self):
        """Test compression of empty token list."""
        compressor = RamanujanCompressor()
        result = compressor.compress([])
        
        assert result["compressed"] == []
        assert result["metadata"]["original_length"] == 0
        assert result["metadata"]["compressed_length"] == 0
    
    def test_compress_single_token(self):
        """Test compression of single token."""
        compressor = RamanujanCompressor()
        tokens = [42]
        result = compressor.compress(tokens)
        
        assert "compressed" in result
        assert "metadata" in result
        assert result["metadata"]["original_length"] == 1
    
    def test_compress_decompress_roundtrip(self):
        """Test compression and decompression roundtrip."""
        compressor = RamanujanCompressor()
        original_tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Compress
        compressed_data = compressor.compress(original_tokens)
        assert "compressed" in compressed_data
        assert "metadata" in compressed_data
        
        # Decompress
        decompressed_tokens = compressor.decompress(compressed_data)
        assert isinstance(decompressed_tokens, list)
        assert len(decompressed_tokens) > 0
    
    def test_different_strategies(self):
        """Test different compression strategies."""
        strategies = [
            CompressionStrategy.FOURIER_LIKE,
            CompressionStrategy.SPARSE_MODULAR,
            CompressionStrategy.HYBRID,
        ]
        
        tokens = list(range(100))
        
        for strategy in strategies:
            config = CompressionConfig(strategy=strategy)
            compressor = RamanujanCompressor(config)
            
            result = compressor.compress(tokens)
            assert "compressed" in result
            assert result["metadata"]["strategy"] == strategy.value
    
    def test_compression_stats(self):
        """Test compression statistics."""
        compressor = RamanujanCompressor()
        tokens = list(range(50))
        
        compressed_data = compressor.compress(tokens)
        stats = compressor.get_compression_stats(tokens, compressed_data)
        
        assert "original_length" in stats
        assert "compressed_length" in stats
        assert "compression_ratio" in stats
        assert "space_saved" in stats
        assert "bits_per_token" in stats
        
        assert stats["original_length"] == len(tokens)
        assert stats["compressed_length"] == len(compressed_data["compressed"])
        assert 0 <= stats["compression_ratio"] <= 1
    
    def test_large_token_sequence(self):
        """Test compression of large token sequence."""
        compressor = RamanujanCompressor()
        tokens = list(range(1000))
        
        result = compressor.compress(tokens)
        assert "compressed" in result
        assert result["metadata"]["original_length"] == 1000
        
        # Should achieve some compression
        compression_ratio = result["metadata"]["compression_ratio"]
        assert compression_ratio < 1.0  # Some compression should occur
    
    def test_compression_config_validation(self):
        """Test compression configuration validation."""
        # Test valid config
        config = CompressionConfig(
            strategy=CompressionStrategy.HYBRID,
            compression_ratio=0.3,
            modular_base=11,
            sparse_threshold=0.05,
        )
        compressor = RamanujanCompressor(config)
        assert compressor.config.compression_ratio == 0.3
        assert compressor.config.modular_base == 11
    
    def test_ramanujan_filter(self):
        """Test Ramanujan filtering function."""
        compressor = RamanujanCompressor()
        
        # Test with different inputs
        assert compressor._ramanujan_filter(1, 0, 10) is not None
        assert compressor._ramanujan_filter(0, 5, 10) is False
        assert isinstance(compressor._ramanujan_filter(7, 3, 10), bool)
    
    def test_should_use_fourier(self):
        """Test Fourier strategy selection."""
        compressor = RamanujanCompressor()
        
        # High variance chunk should use Fourier
        high_variance = [1, 100, 2, 99, 3, 98]
        assert compressor._should_use_fourier(high_variance) is True
        
        # Low variance chunk should not use Fourier
        low_variance = [5, 6, 5, 7, 6, 5]
        assert compressor._should_use_fourier(low_variance) is False
    
    def test_error_handling(self):
        """Test error handling in compression."""
        compressor = RamanujanCompressor()
        
        # Test with invalid input
        with pytest.raises(Exception):
            compressor.compress(None)
        
        # Test with non-list input
        with pytest.raises(Exception):
            compressor.compress("not a list")
    
    def test_compression_quality(self):
        """Test compression quality metrics."""
        compressor = RamanujanCompressor()
        tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        compressed_data = compressor.compress(tokens)
        decompressed_tokens = compressor.decompress(compressed_data)
        
        # Basic quality check - should have some similarity
        assert len(decompressed_tokens) > 0
        assert isinstance(decompressed_tokens, list)
    
    def test_memory_efficiency(self):
        """Test memory efficiency of compression."""
        compressor = RamanujanCompressor()
        
        # Test with progressively larger sequences
        for size in [10, 100, 1000]:
            tokens = list(range(size))
            result = compressor.compress(tokens)
            
            # Should achieve some compression
            compression_ratio = result["metadata"]["compression_ratio"]
            assert compression_ratio < 1.0
            
            # Should not exceed original size
            assert len(result["compressed"]) <= len(tokens)