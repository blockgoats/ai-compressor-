"""
Ramanujan Tokenizer - HuggingFace Integration

Implements a HuggingFace-compatible tokenizer with Ramanujan compression capabilities.
"""

import logging
from typing import List, Dict, Any, Optional, Union, Tuple
import torch
from transformers import PreTrainedTokenizerFast
from transformers.tokenization_utils_base import BatchEncoding
from transformers.utils import PaddingStrategy

from ramanujan_compression import RamanujanCompressor, CompressionConfig
from .config import RamanujanTokenizerConfig

logger = logging.getLogger(__name__)


class RamanujanTokenizerFast(PreTrainedTokenizerFast):
    """
    HuggingFace-compatible tokenizer with Ramanujan compression.
    
    This tokenizer wraps a base HuggingFace tokenizer and adds compression capabilities
    inspired by Ramanujan's mathematical work.
    """
    
    def __init__(
        self,
        base_tokenizer: Optional[PreTrainedTokenizerFast] = None,
        config: Optional[RamanujanTokenizerConfig] = None,
        **kwargs
    ):
        """
        Initialize Ramanujan tokenizer.
        
        Args:
            base_tokenizer: Base HuggingFace tokenizer to wrap
            config: Ramanujan tokenizer configuration
            **kwargs: Additional arguments passed to base tokenizer
        """
        self.config = config or RamanujanTokenizerConfig()
        
        # Initialize base tokenizer if not provided
        if base_tokenizer is None:
            from transformers import AutoTokenizer
            base_tokenizer = AutoTokenizer.from_pretrained(
                self.config.base_tokenizer_name,
                **(self.config.base_tokenizer_config or {})
            )
        
        # Initialize base tokenizer
        super().__init__(
            tokenizer_object=base_tokenizer,
            **kwargs
        )
        
        # Initialize compression
        self._compressor = None
        if self.config.enable_compression:
            self._compressor = RamanujanCompressor(self.config.compression_config)
        
        # Store original methods for fallback
        self._original_encode = super().encode
        self._original_decode = super().decode
        self._original_batch_encode_plus = super().batch_encode_plus
        
        logger.info(f"Ramanujan tokenizer initialized with compression: {self.config.enable_compression}")
    
    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: str,
        config: Optional[RamanujanTokenizerConfig] = None,
        **kwargs
    ):
        """
        Load tokenizer from pretrained model.
        
        Args:
            pretrained_model_name_or_path: Path to pretrained model
            config: Optional configuration override
            **kwargs: Additional arguments
        """
        # Load base tokenizer
        from transformers import AutoTokenizer
        base_tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path,
            **kwargs
        )
        
        # Load Ramanujan config if not provided
        if config is None:
            config = RamanujanTokenizerConfig.from_pretrained(pretrained_model_name_or_path)
        
        return cls(base_tokenizer=base_tokenizer, config=config)
    
    def encode(
        self,
        text: Union[str, List[str]],
        text_pair: Optional[Union[str, List[str]]] = None,
        add_special_tokens: bool = True,
        padding: Union[bool, str, PaddingStrategy] = False,
        truncation: Union[bool, str, PaddingStrategy] = False,
        max_length: Optional[int] = None,
        stride: int = 0,
        return_tensors: Optional[Union[str, bool]] = None,
        **kwargs
    ) -> Union[List[int], torch.Tensor]:
        """
        Encode text with optional compression.
        
        Args:
            text: Text to encode
            text_pair: Optional second text for pair encoding
            add_special_tokens: Whether to add special tokens
            padding: Padding strategy
            truncation: Truncation strategy
            max_length: Maximum sequence length
            stride: Stride for overflow handling
            return_tensors: Return format
            **kwargs: Additional arguments
            
        Returns:
            Encoded tokens (with compression if enabled)
        """
        # Use base tokenizer for encoding
        tokens = self._original_encode(
            text=text,
            text_pair=text_pair,
            add_special_tokens=add_special_tokens,
            padding=padding,
            truncation=truncation,
            max_length=max_length or self.config.max_length,
            stride=stride,
            return_tensors=return_tensors,
            **kwargs
        )
        
        # Apply compression if enabled
        if self.config.enable_compression and self._compressor is not None:
            if isinstance(tokens, torch.Tensor):
                # Convert tensor to list for compression
                tokens_list = tokens.tolist()
                if isinstance(tokens_list[0], list):
                    # Batch encoding
                    compressed_tokens = []
                    for token_seq in tokens_list:
                        compressed_data = self._compressor.compress(token_seq)
                        compressed_tokens.append(compressed_data["compressed"])
                    tokens = torch.tensor(compressed_tokens)
                else:
                    # Single sequence
                    compressed_data = self._compressor.compress(tokens_list)
                    tokens = torch.tensor(compressed_data["compressed"])
            else:
                # List encoding
                if isinstance(tokens[0], list):
                    # Batch encoding
                    compressed_tokens = []
                    for token_seq in tokens:
                        compressed_data = self._compressor.compress(token_seq)
                        compressed_tokens.append(compressed_data["compressed"])
                    tokens = compressed_tokens
                else:
                    # Single sequence
                    compressed_data = self._compressor.compress(tokens)
                    tokens = compressed_data["compressed"]
        
        return tokens
    
    def decode(
        self,
        token_ids: Union[int, List[int], torch.Tensor],
        skip_special_tokens: bool = False,
        clean_up_tokenization_spaces: bool = True,
        **kwargs
    ) -> str:
        """
        Decode tokens with optional decompression.
        
        Args:
            token_ids: Token IDs to decode
            skip_special_tokens: Whether to skip special tokens
            clean_up_tokenization_spaces: Whether to clean up spaces
            **kwargs: Additional arguments
            
        Returns:
            Decoded text
        """
        # Handle decompression if enabled
        if self.config.enable_compression and self._compressor is not None:
            if isinstance(token_ids, torch.Tensor):
                token_ids = token_ids.tolist()
            
            if isinstance(token_ids, list) and len(token_ids) > 0:
                if isinstance(token_ids[0], list):
                    # Batch decoding
                    decompressed_tokens = []
                    for token_seq in token_ids:
                        # Create compressed data structure for decompression
                        compressed_data = {
                            "compressed": token_seq,
                            "metadata": {
                                "strategy": self.config.compression_strategy,
                                "original_length": len(token_seq),
                                "compressed_length": len(token_seq),
                            }
                        }
                        decompressed_seq = self._compressor.decompress(compressed_data)
                        decompressed_tokens.append(decompressed_seq)
                    token_ids = decompressed_tokens
                else:
                    # Single sequence
                    compressed_data = {
                        "compressed": token_ids,
                        "metadata": {
                            "strategy": self.config.compression_strategy,
                            "original_length": len(token_ids),
                            "compressed_length": len(token_ids),
                        }
                    }
                    token_ids = self._compressor.decompress(compressed_data)
        
        # Use base tokenizer for decoding
        return self._original_decode(
            token_ids=token_ids,
            skip_special_tokens=skip_special_tokens,
            clean_up_tokenization_spaces=clean_up_tokenization_spaces,
            **kwargs
        )
    
    def batch_encode_plus(
        self,
        batch_text_or_text_pairs: Union[List[str], List[Tuple[str, str]]],
        add_special_tokens: bool = True,
        padding: Union[bool, str, PaddingStrategy] = False,
        truncation: Union[bool, str, PaddingStrategy] = False,
        max_length: Optional[int] = None,
        stride: int = 0,
        is_split_into_words: bool = False,
        pad_to_multiple_of: Optional[int] = None,
        return_tensors: Optional[Union[str, bool]] = None,
        return_token_type_ids: Optional[bool] = None,
        return_attention_mask: Optional[bool] = None,
        return_overflowing_tokens: bool = False,
        return_special_tokens_mask: bool = False,
        return_offsets_mapping: bool = False,
        return_length: bool = False,
        verbose: bool = True,
        **kwargs
    ) -> BatchEncoding:
        """
        Batch encode with optional compression.
        
        Args:
            batch_text_or_text_pairs: Batch of texts or text pairs
            add_special_tokens: Whether to add special tokens
            padding: Padding strategy
            truncation: Truncation strategy
            max_length: Maximum sequence length
            stride: Stride for overflow handling
            is_split_into_words: Whether input is pre-tokenized
            pad_to_multiple_of: Pad to multiple of this number
            return_tensors: Return format
            return_token_type_ids: Whether to return token type IDs
            return_attention_mask: Whether to return attention mask
            return_overflowing_tokens: Whether to return overflowing tokens
            return_special_tokens_mask: Whether to return special tokens mask
            return_offsets_mapping: Whether to return offsets mapping
            return_length: Whether to return lengths
            verbose: Whether to be verbose
            **kwargs: Additional arguments
            
        Returns:
            BatchEncoding with compressed tokens
        """
        # Use base tokenizer for batch encoding
        batch_encoding = self._original_batch_encode_plus(
            batch_text_or_text_pairs=batch_text_or_text_pairs,
            add_special_tokens=add_special_tokens,
            padding=padding,
            truncation=truncation,
            max_length=max_length or self.config.max_length,
            stride=stride,
            is_split_into_words=is_split_into_words,
            pad_to_multiple_of=pad_to_multiple_of,
            return_tensors=return_tensors,
            return_token_type_ids=return_token_type_ids,
            return_attention_mask=return_attention_mask,
            return_overflowing_tokens=return_overflowing_tokens,
            return_special_tokens_mask=return_special_tokens_mask,
            return_offsets_mapping=return_offsets_mapping,
            return_length=return_length,
            verbose=verbose,
            **kwargs
        )
        
        # Apply compression if enabled
        if self.config.enable_compression and self._compressor is not None:
            input_ids = batch_encoding["input_ids"]
            
            if isinstance(input_ids, torch.Tensor):
                # Convert tensor to list for compression
                input_ids_list = input_ids.tolist()
                compressed_ids = []
                for token_seq in input_ids_list:
                    compressed_data = self._compressor.compress(token_seq)
                    compressed_ids.append(compressed_data["compressed"])
                
                # Convert back to tensor if needed
                if return_tensors == "pt":
                    compressed_ids = torch.tensor(compressed_ids)
                
                batch_encoding["input_ids"] = compressed_ids
            else:
                # List format
                compressed_ids = []
                for token_seq in input_ids:
                    compressed_data = self._compressor.compress(token_seq)
                    compressed_ids.append(compressed_data["compressed"])
                batch_encoding["input_ids"] = compressed_ids
        
        return batch_encoding
    
    def save_pretrained(self, save_directory: str, **kwargs):
        """
        Save tokenizer to directory.
        
        Args:
            save_directory: Directory to save to
            **kwargs: Additional arguments
        """
        # Save base tokenizer
        super().save_pretrained(save_directory, **kwargs)
        
        # Save Ramanujan config
        self.config.save_pretrained(save_directory)
        
        logger.info(f"Ramanujan tokenizer saved to {save_directory}")
    
    def get_compression_stats(self) -> Optional[Dict[str, Any]]:
        """
        Get compression statistics if available.
        
        Returns:
            Dictionary with compression statistics or None
        """
        if not self.config.enable_compression or self._compressor is None:
            return None
        
        return {
            "strategy": self.config.compression_strategy,
            "compression_ratio": self.config.compression_ratio,
            "modular_base": self.config.modular_base,
            "sparse_threshold": self.config.sparse_threshold,
            "context_length": self.config.context_length,
            "gpu_acceleration": self.config.gpu_acceleration,
        }
    
    def enable_compression(self, enable: bool = True):
        """
        Enable or disable compression.
        
        Args:
            enable: Whether to enable compression
        """
        self.config.enable_compression = enable
        
        if enable and self._compressor is None:
            self._compressor = RamanujanCompressor(self.config.compression_config)
        elif not enable:
            self._compressor = None
        
        logger.info(f"Compression {'enabled' if enable else 'disabled'}")
    
    def set_compression_config(self, config: CompressionConfig):
        """
        Update compression configuration.
        
        Args:
            config: New compression configuration
        """
        self.config.compression_config = config
        
        if self._compressor is not None:
            self._compressor.config = config
        
        logger.info("Compression configuration updated")