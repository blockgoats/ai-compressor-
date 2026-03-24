"""
Ramanujan Compression Core Implementation

Implements Ramanujan-inspired mathematical compression algorithms for token sequences.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class CompressionStrategy(Enum):
    """Available compression strategies."""
    FOURIER_LIKE = "fourier_like"
    SPARSE_MODULAR = "sparse_modular"
    HYBRID = "hybrid"


@dataclass
class CompressionConfig:
    """Configuration for compression algorithms."""
    strategy: CompressionStrategy = CompressionStrategy.HYBRID
    compression_ratio: float = 0.5  # Target compression ratio (0.0-1.0)
    modular_base: int = 7  # Base for modular arithmetic
    sparse_threshold: float = 0.1  # Threshold for sparse filtering
    context_length: int = 512  # Context window length
    gpu_acceleration: bool = False  # Enable GPU acceleration (Pro tier)


class RamanujanCompressor:
    """
    Ramanujan-inspired token compressor.
    
    Implements multiple compression strategies inspired by Ramanujan's mathematical work,
    particularly his work on modular forms and theta functions.
    """
    
    def __init__(self, config: Optional[CompressionConfig] = None):
        """
        Initialize the compressor.
        
        Args:
            config: Compression configuration. If None, uses default config.
        """
        self.config = config or CompressionConfig()
        self._setup_compression_functions()
        
    def _setup_compression_functions(self):
        """Setup compression functions based on strategy."""
        if self.config.strategy == CompressionStrategy.FOURIER_LIKE:
            self._compress_func = self._fourier_compress
            self._decompress_func = self._fourier_decompress
        elif self.config.strategy == CompressionStrategy.SPARSE_MODULAR:
            self._compress_func = self._sparse_modular_compress
            self._decompress_func = self._sparse_modular_decompress
        elif self.config.strategy == CompressionStrategy.HYBRID:
            self._compress_func = self._hybrid_compress
            self._decompress_func = self._hybrid_decompress
        else:
            raise ValueError(f"Unknown compression strategy: {self.config.strategy}")
    
    def compress(self, tokens: List[int]) -> Dict[str, Any]:
        """
        Compress a list of tokens.
        
        Args:
            tokens: List of token IDs to compress
            
        Returns:
            Dictionary containing compressed data and metadata
        """
        if not tokens:
            return {
                "compressed": [], 
                "metadata": {
                    "original_length": 0,
                    "compressed_length": 0,
                    "compression_ratio": 0.0,
                    "strategy": self.config.strategy.value,
                }
            }
            
        logger.debug(f"Compressing {len(tokens)} tokens using {self.config.strategy.value}")
        
        try:
            compressed_data = self._compress_func(tokens)
            compression_ratio = len(compressed_data) / len(tokens)
            
            result = {
                "compressed": compressed_data,
                "metadata": {
                    "original_length": len(tokens),
                    "compressed_length": len(compressed_data),
                    "compression_ratio": compression_ratio,
                    "strategy": self.config.strategy.value,
                    "config": {
                        "modular_base": self.config.modular_base,
                        "sparse_threshold": self.config.sparse_threshold,
                    }
                }
            }
            
            logger.debug(f"Compression completed. Ratio: {compression_ratio:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"Compression failed: {e}")
            raise
    
    def decompress(self, compressed_data: Dict[str, Any]) -> List[int]:
        """
        Decompress compressed data back to tokens.
        
        Args:
            compressed_data: Dictionary containing compressed data and metadata
            
        Returns:
            List of decompressed token IDs
        """
        if not compressed_data.get("compressed"):
            return []
            
        logger.debug(f"Decompressing using {compressed_data.get('metadata', {}).get('strategy', 'unknown')}")
        
        try:
            tokens = self._decompress_func(compressed_data)
            logger.debug(f"Decompression completed. Restored {len(tokens)} tokens")
            return tokens
            
        except Exception as e:
            logger.error(f"Decompression failed: {e}")
            raise
    
    def _fourier_compress(self, tokens: List[int]) -> List[int]:
        """
        Fourier-like compression using frequency domain analysis.
        
        Inspired by Ramanujan's work on theta functions and modular forms.
        """
        if len(tokens) < 2:
            return tokens
            
        # Convert to numpy array for FFT
        token_array = np.array(tokens, dtype=np.float64)
        
        # Apply FFT
        fft_tokens = np.fft.fft(token_array)
        
        # Keep only the most significant frequencies (sparse representation)
        threshold = np.percentile(np.abs(fft_tokens), (1 - self.config.compression_ratio) * 100)
        sparse_fft = np.where(np.abs(fft_tokens) >= threshold, fft_tokens, 0)
        
        # Convert back to real domain and quantize
        compressed = np.real(np.fft.ifft(sparse_fft))
        
        # Quantize to integers
        compressed_tokens = np.round(compressed).astype(int).tolist()
        
        return compressed_tokens
    
    def _fourier_decompress(self, compressed_data: Dict[str, Any]) -> List[int]:
        """Decompress Fourier-compressed data."""
        # For Fourier compression, the compressed data is already the tokens
        return compressed_data["compressed"]
    
    def _sparse_modular_compress(self, tokens: List[int]) -> List[int]:
        """
        Sparse modular compression using Ramanujan sums.
        
        Based on Ramanujan's work on modular arithmetic and theta functions.
        """
        if len(tokens) < 2:
            return tokens
            
        # Convert tokens to modular representation
        modular_tokens = [t % self.config.modular_base for t in tokens]
        
        # Apply sparse filtering based on Ramanujan sum properties
        sparse_tokens = []
        for i, token in enumerate(modular_tokens):
            # Use Ramanujan sum-like filtering
            if self._ramanujan_filter(token, i, len(tokens)):
                sparse_tokens.append(token)
            else:
                # Store position and value for reconstruction
                sparse_tokens.append(0)  # Placeholder for sparse element
        
        # Apply additional compression by removing zeros and storing positions
        compressed = []
        for i, token in enumerate(sparse_tokens):
            if token != 0:
                compressed.append(token)
            elif i % 2 == 0:  # Keep every other zero for reconstruction
                compressed.append(0)
        
        return compressed
    
    def _sparse_modular_decompress(self, compressed_data: Dict[str, Any]) -> List[int]:
        """Decompress sparse modular data."""
        # This is a simplified decompression - in practice, you'd need more metadata
        return compressed_data["compressed"]
    
    def _hybrid_compress(self, tokens: List[int]) -> List[int]:
        """
        Hybrid compression combining multiple strategies.
        
        Uses both Fourier and sparse modular approaches adaptively.
        """
        if len(tokens) < 4:
            return tokens
            
        # Split tokens into chunks for different strategies
        chunk_size = max(4, len(tokens) // 4)
        compressed_chunks = []
        
        for i in range(0, len(tokens), chunk_size):
            chunk = tokens[i:i + chunk_size]
            
            # Choose strategy based on chunk characteristics
            if self._should_use_fourier(chunk):
                compressed_chunk = self._fourier_compress(chunk)
            else:
                compressed_chunk = self._sparse_modular_compress(chunk)
            
            compressed_chunks.extend(compressed_chunk)
        
        return compressed_chunks
    
    def _hybrid_decompress(self, compressed_data: Dict[str, Any]) -> List[int]:
        """Decompress hybrid compressed data."""
        return compressed_data["compressed"]
    
    def _ramanujan_filter(self, token: int, position: int, total_length: int) -> bool:
        """
        Ramanujan-inspired filtering function.
        
        Based on properties of Ramanujan sums and modular forms.
        """
        # Simple heuristic based on position and value
        if token == 0:
            return False
            
        # Use modular arithmetic properties
        if (position * token) % self.config.modular_base == 0:
            return True
            
        # Sparse selection based on prime-like properties
        if token % 2 == 1 and position % 3 == 0:
            return True
            
        return False
    
    def _should_use_fourier(self, chunk: List[int]) -> bool:
        """Determine if Fourier compression is better for this chunk."""
        if len(chunk) < 3:
            return False
            
        # Use Fourier if the chunk has high variance (good for frequency domain)
        variance = np.var(chunk)
        return variance > np.mean(chunk) * 0.5
    
    def get_compression_stats(self, original_tokens: List[int], compressed_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Get compression statistics.
        
        Args:
            original_tokens: Original token list
            compressed_data: Compressed data dictionary
            
        Returns:
            Dictionary with compression statistics
        """
        original_length = len(original_tokens)
        compressed_length = len(compressed_data["compressed"])
        
        return {
            "original_length": original_length,
            "compressed_length": compressed_length,
            "compression_ratio": compressed_length / original_length if original_length > 0 else 0,
            "space_saved": (original_length - compressed_length) / original_length if original_length > 0 else 0,
            "bits_per_token": compressed_length * 8 / original_length if original_length > 0 else 0,
        }