"""
Ramanujan Tokenizer - HuggingFace Integration

Provides HuggingFace-compatible tokenizer with Ramanujan compression capabilities.
"""

from .tokenization_ramanujan import RamanujanTokenizerFast
from .config import RamanujanTokenizerConfig

__version__ = "0.1.0"
__all__ = [
    "RamanujanTokenizerFast",
    "RamanujanTokenizerConfig",
]