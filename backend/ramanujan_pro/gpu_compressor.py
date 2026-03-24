"""
GPU-Accelerated Compression for Ramanujan Pro

Provides CUDA-accelerated compression algorithms for high-performance applications.
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np

try:
    import torch
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False
    torch = None
    cp = None

from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy

logger = logging.getLogger(__name__)


class GPUCompressor(RamanujanCompressor):
    """
    GPU-accelerated Ramanujan compressor.
    
    Provides CUDA-accelerated compression algorithms for high-performance applications.
    Requires CUDA-compatible GPU and cupy library.
    """
    
    def __init__(self, config: Optional[CompressionConfig] = None, device: str = "cuda"):
        """
        Initialize GPU compressor.
        
        Args:
            config: Compression configuration
            device: CUDA device to use ("cuda" or "cuda:0", "cuda:1", etc.)
        """
        if not GPU_AVAILABLE:
            raise ImportError("GPU acceleration requires torch and cupy. Install with: pip install torch cupy-cuda11x")
        
        super().__init__(config)
        self.device = device
        self._check_gpu_availability()
        
        logger.info(f"GPU compressor initialized on device: {device}")
    
    def _check_gpu_availability(self):
        """Check if GPU is available and accessible."""
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available on this system")
        
        if not cp.cuda.is_available():
            raise RuntimeError("CuPy CUDA is not available")
        
        # Test GPU memory
        try:
            test_tensor = torch.randn(1000, 1000).to(self.device)
            del test_tensor
        except Exception as e:
            raise RuntimeError(f"GPU device {self.device} is not accessible: {e}")
    
    def compress(self, tokens: List[int]) -> Dict[str, Any]:
        """
        GPU-accelerated compression.
        
        Args:
            tokens: List of token IDs to compress
            
        Returns:
            Dictionary containing compressed data and metadata
        """
        if not tokens:
            return {"compressed": [], "metadata": {}}
        
        logger.debug(f"GPU compressing {len(tokens)} tokens using {self.config.strategy.value}")
        
        try:
            # Convert to GPU tensors
            token_tensor = torch.tensor(tokens, dtype=torch.float32, device=self.device)
            
            # Apply GPU-accelerated compression
            compressed_tensor = self._gpu_compress_tensor(token_tensor)
            
            # Convert back to CPU
            compressed_tokens = compressed_tensor.cpu().numpy().astype(int).tolist()
            
            compression_ratio = len(compressed_tokens) / len(tokens)
            
            result = {
                "compressed": compressed_tokens,
                "metadata": {
                    "original_length": len(tokens),
                    "compressed_length": len(compressed_tokens),
                    "compression_ratio": compression_ratio,
                    "strategy": self.config.strategy.value,
                    "gpu_accelerated": True,
                    "device": self.device,
                    "config": {
                        "modular_base": self.config.modular_base,
                        "sparse_threshold": self.config.sparse_threshold,
                    }
                }
            }
            
            logger.debug(f"GPU compression completed. Ratio: {compression_ratio:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"GPU compression failed: {e}")
            # Fallback to CPU compression
            logger.warning("Falling back to CPU compression")
            return super().compress(tokens)
    
    def decompress(self, compressed_data: Dict[str, Any]) -> List[int]:
        """
        GPU-accelerated decompression.
        
        Args:
            compressed_data: Dictionary containing compressed data and metadata
            
        Returns:
            List of decompressed token IDs
        """
        if not compressed_data.get("compressed"):
            return []
        
        logger.debug(f"GPU decompressing using {compressed_data.get('metadata', {}).get('strategy', 'unknown')}")
        
        try:
            # Convert to GPU tensor
            compressed_tensor = torch.tensor(
                compressed_data["compressed"], 
                dtype=torch.float32, 
                device=self.device
            )
            
            # Apply GPU-accelerated decompression
            decompressed_tensor = self._gpu_decompress_tensor(compressed_tensor, compressed_data)
            
            # Convert back to CPU
            tokens = decompressed_tensor.cpu().numpy().astype(int).tolist()
            
            logger.debug(f"GPU decompression completed. Restored {len(tokens)} tokens")
            return tokens
            
        except Exception as e:
            logger.error(f"GPU decompression failed: {e}")
            # Fallback to CPU decompression
            logger.warning("Falling back to CPU decompression")
            return super().decompress(compressed_data)
    
    def _gpu_compress_tensor(self, token_tensor: torch.Tensor) -> torch.Tensor:
        """
        GPU-accelerated tensor compression.
        
        Args:
            token_tensor: Input token tensor on GPU
            
        Returns:
            Compressed tensor on GPU
        """
        if self.config.strategy == CompressionStrategy.FOURIER_LIKE:
            return self._gpu_fourier_compress(token_tensor)
        elif self.config.strategy == CompressionStrategy.SPARSE_MODULAR:
            return self._gpu_sparse_modular_compress(token_tensor)
        elif self.config.strategy == CompressionStrategy.HYBRID:
            return self._gpu_hybrid_compress(token_tensor)
        else:
            raise ValueError(f"Unknown compression strategy: {self.config.strategy}")
    
    def _gpu_decompress_tensor(self, compressed_tensor: torch.Tensor, metadata: Dict[str, Any]) -> torch.Tensor:
        """
        GPU-accelerated tensor decompression.
        
        Args:
            compressed_tensor: Compressed tensor on GPU
            metadata: Compression metadata
            
        Returns:
            Decompressed tensor on GPU
        """
        strategy = metadata.get("metadata", {}).get("strategy", self.config.strategy.value)
        
        if strategy == CompressionStrategy.FOURIER_LIKE.value:
            return self._gpu_fourier_decompress(compressed_tensor)
        elif strategy == CompressionStrategy.SPARSE_MODULAR.value:
            return self._gpu_sparse_modular_decompress(compressed_tensor)
        elif strategy == CompressionStrategy.HYBRID.value:
            return self._gpu_hybrid_decompress(compressed_tensor)
        else:
            # Fallback to returning as-is
            return compressed_tensor
    
    def _gpu_fourier_compress(self, token_tensor: torch.Tensor) -> torch.Tensor:
        """GPU-accelerated Fourier compression."""
        # Apply FFT on GPU
        fft_tokens = torch.fft.fft(token_tensor)
        
        # Keep only significant frequencies
        threshold = torch.quantile(torch.abs(fft_tokens), 1 - self.config.compression_ratio)
        sparse_fft = torch.where(torch.abs(fft_tokens) >= threshold, fft_tokens, 0)
        
        # Convert back to real domain
        compressed = torch.real(torch.fft.ifft(sparse_fft))
        
        return compressed
    
    def _gpu_fourier_decompress(self, compressed_tensor: torch.Tensor) -> torch.Tensor:
        """GPU-accelerated Fourier decompression."""
        # For Fourier compression, the compressed data is already the tokens
        return compressed_tensor
    
    def _gpu_sparse_modular_compress(self, token_tensor: torch.Tensor) -> torch.Tensor:
        """GPU-accelerated sparse modular compression."""
        # Apply modular arithmetic on GPU
        modular_tokens = token_tensor % self.config.modular_base
        
        # Apply sparse filtering using GPU operations
        positions = torch.arange(len(modular_tokens), device=self.device)
        sparse_mask = self._gpu_ramanujan_filter(modular_tokens, positions)
        
        # Apply sparse filtering
        compressed = torch.where(sparse_mask, modular_tokens, 0)
        
        return compressed
    
    def _gpu_sparse_modular_decompress(self, compressed_tensor: torch.Tensor) -> torch.Tensor:
        """GPU-accelerated sparse modular decompression."""
        # This is a simplified decompression - in practice, you'd need more metadata
        return compressed_tensor
    
    def _gpu_hybrid_compress(self, token_tensor: torch.Tensor) -> torch.Tensor:
        """GPU-accelerated hybrid compression."""
        # Split into chunks for different strategies
        chunk_size = max(4, len(token_tensor) // 4)
        compressed_chunks = []
        
        for i in range(0, len(token_tensor), chunk_size):
            chunk = token_tensor[i:i + chunk_size]
            
            # Choose strategy based on chunk characteristics
            if self._gpu_should_use_fourier(chunk):
                compressed_chunk = self._gpu_fourier_compress(chunk)
            else:
                compressed_chunk = self._gpu_sparse_modular_compress(chunk)
            
            compressed_chunks.append(compressed_chunk)
        
        return torch.cat(compressed_chunks)
    
    def _gpu_hybrid_decompress(self, compressed_tensor: torch.Tensor) -> torch.Tensor:
        """GPU-accelerated hybrid decompression."""
        return compressed_tensor
    
    def _gpu_ramanujan_filter(self, tokens: torch.Tensor, positions: torch.Tensor) -> torch.Tensor:
        """GPU-accelerated Ramanujan filtering."""
        # Use GPU operations for filtering
        non_zero_mask = tokens != 0
        modular_mask = (positions * tokens) % self.config.modular_base == 0
        sparse_mask = (tokens % 2 == 1) & (positions % 3 == 0)
        
        return non_zero_mask & (modular_mask | sparse_mask)
    
    def _gpu_should_use_fourier(self, chunk: torch.Tensor) -> bool:
        """Determine if Fourier compression is better for this chunk (GPU version)."""
        if len(chunk) < 3:
            return False
        
        variance = torch.var(chunk)
        mean_val = torch.mean(chunk)
        return variance > mean_val * 0.5
    
    def batch_compress(self, token_batches: List[List[int]]) -> List[Dict[str, Any]]:
        """
        Batch compression using GPU acceleration.
        
        Args:
            token_batches: List of token sequences to compress
            
        Returns:
            List of compressed data dictionaries
        """
        if not token_batches:
            return []
        
        logger.debug(f"GPU batch compressing {len(token_batches)} sequences")
        
        try:
            # Convert all batches to GPU tensors
            batch_tensors = []
            for tokens in token_batches:
                if tokens:
                    batch_tensors.append(torch.tensor(tokens, dtype=torch.float32, device=self.device))
                else:
                    batch_tensors.append(torch.tensor([], dtype=torch.float32, device=self.device))
            
            # Process in parallel (simplified - in practice, use proper batching)
            results = []
            for i, (tokens, tensor) in enumerate(zip(token_batches, batch_tensors)):
                if len(tokens) == 0:
                    results.append({"compressed": [], "metadata": {}})
                    continue
                
                compressed_tensor = self._gpu_compress_tensor(tensor)
                compressed_tokens = compressed_tensor.cpu().numpy().astype(int).tolist()
                
                compression_ratio = len(compressed_tokens) / len(tokens)
                
                results.append({
                    "compressed": compressed_tokens,
                    "metadata": {
                        "original_length": len(tokens),
                        "compressed_length": len(compressed_tokens),
                        "compression_ratio": compression_ratio,
                        "strategy": self.config.strategy.value,
                        "gpu_accelerated": True,
                        "device": self.device,
                    }
                })
            
            logger.debug(f"GPU batch compression completed")
            return results
            
        except Exception as e:
            logger.error(f"GPU batch compression failed: {e}")
            # Fallback to CPU batch compression
            logger.warning("Falling back to CPU batch compression")
            return [self.compress(tokens) for tokens in token_batches]
    
    def get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information and capabilities."""
        if not GPU_AVAILABLE:
            return {"available": False}
        
        try:
            device = torch.device(self.device)
            gpu_name = torch.cuda.get_device_name(device)
            gpu_memory = torch.cuda.get_device_properties(device).total_memory
            gpu_memory_allocated = torch.cuda.memory_allocated(device)
            gpu_memory_cached = torch.cuda.memory_reserved(device)
            
            return {
                "available": True,
                "device": str(device),
                "name": gpu_name,
                "total_memory": gpu_memory,
                "memory_allocated": gpu_memory_allocated,
                "memory_cached": gpu_memory_cached,
                "memory_free": gpu_memory - gpu_memory_allocated,
                "cuda_version": torch.version.cuda,
                "cupy_available": cp is not None,
            }
        except Exception as e:
            return {
                "available": True,
                "error": str(e),
            }