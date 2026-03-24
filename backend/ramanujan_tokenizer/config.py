"""
Configuration classes for Ramanujan Tokenizer.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from transformers import PreTrainedTokenizerFast
from ramanujan_compression import CompressionConfig, CompressionStrategy


@dataclass
class RamanujanTokenizerConfig:
    """
    Configuration for Ramanujan Tokenizer.
    
    Extends HuggingFace tokenizer configuration with compression settings.
    """
    # Base tokenizer configuration
    base_tokenizer_name: str = "bert-base-uncased"
    base_tokenizer_config: Optional[Dict[str, Any]] = None
    
    # Compression configuration
    compression_config: Optional[CompressionConfig] = None
    enable_compression: bool = True
    compression_strategy: str = "hybrid"
    compression_ratio: float = 0.5
    modular_base: int = 7
    sparse_threshold: float = 0.1
    
    # Advanced settings
    context_length: int = 512
    gpu_acceleration: bool = False
    pro_features: bool = False
    
    # Tokenizer-specific settings
    max_length: int = 512
    padding: str = "max_length"
    truncation: bool = True
    return_tensors: str = "pt"
    
    def __post_init__(self):
        """Initialize compression config if not provided."""
        if self.compression_config is None:
            self.compression_config = CompressionConfig(
                strategy=CompressionStrategy(self.compression_strategy),
                compression_ratio=self.compression_ratio,
                modular_base=self.modular_base,
                sparse_threshold=self.sparse_threshold,
                context_length=self.context_length,
                gpu_acceleration=self.gpu_acceleration,
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "base_tokenizer_name": self.base_tokenizer_name,
            "base_tokenizer_config": self.base_tokenizer_config,
            "enable_compression": self.enable_compression,
            "compression_strategy": self.compression_strategy,
            "compression_ratio": self.compression_ratio,
            "modular_base": self.modular_base,
            "sparse_threshold": self.sparse_threshold,
            "context_length": self.context_length,
            "gpu_acceleration": self.gpu_acceleration,
            "pro_features": self.pro_features,
            "max_length": self.max_length,
            "padding": self.padding,
            "truncation": self.truncation,
            "return_tensors": self.return_tensors,
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'RamanujanTokenizerConfig':
        """Create config from dictionary."""
        # Extract compression config if present
        compression_config = None
        if "compression_config" in config_dict:
            compression_config = CompressionConfig(**config_dict["compression_config"])
        
        # Remove compression_config from main dict
        config_dict = {k: v for k, v in config_dict.items() if k != "compression_config"}
        
        return cls(compression_config=compression_config, **config_dict)
    
    def save_pretrained(self, save_directory: str):
        """Save configuration to directory."""
        import json
        import os
        
        os.makedirs(save_directory, exist_ok=True)
        
        # Save main config
        config_path = os.path.join(save_directory, "ramanujan_tokenizer_config.json")
        with open(config_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        # Save compression config separately
        if self.compression_config:
            compression_path = os.path.join(save_directory, "compression_config.json")
            with open(compression_path, 'w') as f:
                json.dump({
                    "strategy": self.compression_config.strategy.value,
                    "compression_ratio": self.compression_config.compression_ratio,
                    "modular_base": self.compression_config.modular_base,
                    "sparse_threshold": self.compression_config.sparse_threshold,
                    "context_length": self.compression_config.context_length,
                    "gpu_acceleration": self.compression_config.gpu_acceleration,
                }, f, indent=2)
    
    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path: str) -> 'RamanujanTokenizerConfig':
        """Load configuration from pretrained model directory."""
        import json
        import os
        
        config_path = os.path.join(pretrained_model_name_or_path, "ramanujan_tokenizer_config.json")
        
        if not os.path.exists(config_path):
            # Return default config if not found
            return cls()
        
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        
        # Load compression config if available
        compression_path = os.path.join(pretrained_model_name_or_path, "compression_config.json")
        if os.path.exists(compression_path):
            with open(compression_path, 'r') as f:
                compression_dict = json.load(f)
                compression_dict["strategy"] = CompressionStrategy(compression_dict["strategy"])
                config_dict["compression_config"] = CompressionConfig(**compression_dict)
        
        return cls.from_dict(config_dict)