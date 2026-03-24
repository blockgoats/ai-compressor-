"""
Ramanujan Compression SDK - Core Compression Module

This module provides Ramanujan-inspired compression algorithms for token sequences.
"""

from .compressor import RamanujanCompressor, CompressionStrategy, CompressionConfig
from .utils import benchmark_compression

__version__ = "0.1.0"
__all__ = [
    "RamanujanCompressor",
    "CompressionStrategy", 
    "CompressionConfig",
    "benchmark_compression",
]