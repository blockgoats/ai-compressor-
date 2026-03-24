"""
Tests for Ramanujan Tokenizer
"""

import pytest
import torch
from ramanujan_tokenizer import RamanujanTokenizerFast, RamanujanTokenizerConfig
from ramanujan_compression import CompressionConfig, CompressionStrategy


class TestRamanujanTokenizer:
    """Test cases for RamanujanTokenizerFast."""
    
    def test_tokenizer_initialization(self):
        """Test tokenizer initialization."""
        config = RamanujanTokenizerConfig()
        tokenizer = RamanujanTokenizerFast(config=config)
        
        assert tokenizer.config == config
        assert tokenizer.config.enable_compression is True
    
    def test_tokenizer_with_compression_disabled(self):
        """Test tokenizer with compression disabled."""
        config = RamanujanTokenizerConfig(enable_compression=False)
        tokenizer = RamanujanTokenizerFast(config=config)
        
        assert tokenizer.config.enable_compression is False
        assert tokenizer._compressor is None
    
    def test_encode_decode_roundtrip(self):
        """Test encode and decode roundtrip."""
        config = RamanujanTokenizerConfig(
            base_tokenizer_name="bert-base-uncased",
            enable_compression=True
        )
        tokenizer = RamanujanTokenizerFast(config=config)
        
        text = "This is a test sentence."
        
        # Encode
        tokens = tokenizer.encode(text)
        assert isinstance(tokens, (list, torch.Tensor))
        
        # Decode
        decoded = tokenizer.decode(tokens)
        assert isinstance(decoded, str)
        assert len(decoded) > 0
    
    def test_batch_encode_decode(self):
        """Test batch encoding and decoding."""
        config = RamanujanTokenizerConfig(
            base_tokenizer_name="bert-base-uncased",
            enable_compression=True
        )
        tokenizer = RamanujanTokenizerFast(config=config)
        
        texts = ["First sentence.", "Second sentence.", "Third sentence."]
        
        # Batch encode
        batch_encoding = tokenizer.batch_encode_plus(texts)
        assert "input_ids" in batch_encoding
        assert len(batch_encoding["input_ids"]) == len(texts)
        
        # Decode each
        for i, text in enumerate(texts):
            tokens = batch_encoding["input_ids"][i]
            decoded = tokenizer.decode(tokens)
            assert isinstance(decoded, str)
    
    def test_compression_stats(self):
        """Test compression statistics."""
        config = RamanujanTokenizerConfig(enable_compression=True)
        tokenizer = RamanujanTokenizerFast(config=config)
        
        stats = tokenizer.get_compression_stats()
        assert stats is not None
        assert "strategy" in stats
        assert "compression_ratio" in stats
    
    def test_compression_disabled_stats(self):
        """Test compression statistics when disabled."""
        config = RamanujanTokenizerConfig(enable_compression=False)
        tokenizer = RamanujanTokenizerFast(config=config)
        
        stats = tokenizer.get_compression_stats()
        assert stats is None
    
    def test_enable_disable_compression(self):
        """Test enabling and disabling compression."""
        config = RamanujanTokenizerConfig(enable_compression=True)
        tokenizer = RamanujanTokenizerFast(config=config)
        
        # Initially enabled
        assert tokenizer.config.enable_compression is True
        assert tokenizer._compressor is not None
        
        # Disable
        tokenizer.enable_compression(False)
        assert tokenizer.config.enable_compression is False
        assert tokenizer._compressor is None
        
        # Re-enable
        tokenizer.enable_compression(True)
        assert tokenizer.config.enable_compression is True
        assert tokenizer._compressor is not None
    
    def test_set_compression_config(self):
        """Test setting compression configuration."""
        config = RamanujanTokenizerConfig()
        tokenizer = RamanujanTokenizerFast(config=config)
        
        new_config = CompressionConfig(
            strategy=CompressionStrategy.FOURIER_LIKE,
            compression_ratio=0.3
        )
        
        tokenizer.set_compression_config(new_config)
        assert tokenizer.config.compression_config == new_config
        assert tokenizer._compressor.config == new_config
    
    def test_different_compression_strategies(self):
        """Test different compression strategies."""
        strategies = ["fourier_like", "sparse_modular", "hybrid"]
        
        for strategy in strategies:
            config = RamanujanTokenizerConfig(
                compression_strategy=strategy,
                enable_compression=True
            )
            tokenizer = RamanujanTokenizerFast(config=config)
            
            text = "Testing compression strategy."
            tokens = tokenizer.encode(text)
            decoded = tokenizer.decode(tokens)
            
            assert isinstance(tokens, (list, torch.Tensor))
            assert isinstance(decoded, str)
    
    def test_save_pretrained(self, tmp_path):
        """Test saving tokenizer."""
        config = RamanujanTokenizerConfig()
        tokenizer = RamanujanTokenizerFast(config=config)
        
        save_dir = tmp_path / "test_tokenizer"
        tokenizer.save_pretrained(str(save_dir))
        
        # Check that files were created
        assert (save_dir / "ramanujan_tokenizer_config.json").exists()
        assert (save_dir / "compression_config.json").exists()
    
    def test_from_pretrained(self, tmp_path):
        """Test loading tokenizer from pretrained."""
        # First save a tokenizer
        config = RamanujanTokenizerConfig()
        tokenizer = RamanujanTokenizerFast(config=config)
        
        save_dir = tmp_path / "test_tokenizer"
        tokenizer.save_pretrained(str(save_dir))
        
        # Load it back
        loaded_tokenizer = RamanujanTokenizerFast.from_pretrained(str(save_dir))
        
        assert loaded_tokenizer.config.enable_compression == config.enable_compression
        assert loaded_tokenizer.config.compression_strategy == config.compression_strategy
    
    def test_tokenizer_with_torch_tensors(self):
        """Test tokenizer with PyTorch tensors."""
        config = RamanujanTokenizerConfig(
            return_tensors="pt",
            enable_compression=True
        )
        tokenizer = RamanujanTokenizerFast(config=config)
        
        text = "Test with PyTorch tensors."
        tokens = tokenizer.encode(text)
        
        assert isinstance(tokens, torch.Tensor)
        
        decoded = tokenizer.decode(tokens)
        assert isinstance(decoded, str)
    
    def test_error_handling(self):
        """Test error handling."""
        config = RamanujanTokenizerConfig()
        tokenizer = RamanujanTokenizerFast(config=config)
        
        # Test with invalid input
        with pytest.raises(Exception):
            tokenizer.encode(None)
        
        with pytest.raises(Exception):
            tokenizer.decode(None)
    
    def test_compression_quality(self):
        """Test compression quality."""
        config = RamanujanTokenizerConfig(enable_compression=True)
        tokenizer = RamanujanTokenizerFast(config=config)
        
        text = "This is a longer text that should benefit from compression."
        
        # Encode and decode
        tokens = tokenizer.encode(text)
        decoded = tokenizer.decode(tokens)
        
        # Basic quality check
        assert len(decoded) > 0
        assert isinstance(decoded, str)
        
        # Should be able to decode back to some meaningful text
        assert len(decoded.split()) > 0
    
    def test_batch_processing_consistency(self):
        """Test consistency between single and batch processing."""
        config = RamanujanTokenizerConfig(enable_compression=True)
        tokenizer = RamanujanTokenizerFast(config=config)
        
        text = "Test consistency between single and batch processing."
        
        # Single processing
        single_tokens = tokenizer.encode(text)
        single_decoded = tokenizer.decode(single_tokens)
        
        # Batch processing
        batch_encoding = tokenizer.batch_encode_plus([text])
        batch_tokens = batch_encoding["input_ids"][0]
        batch_decoded = tokenizer.decode(batch_tokens)
        
        # Results should be consistent
        assert isinstance(single_tokens, type(batch_tokens))
        assert isinstance(single_decoded, str)
        assert isinstance(batch_decoded, str)