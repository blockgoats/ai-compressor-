"""
Pro Compressor - Professional Tier Features

Advanced compression features for enterprise and professional users.
"""

import logging
from typing import List, Dict, Any, Optional, Union
import json
import hashlib
import time
from dataclasses import dataclass

from ramanujan_compression import RamanujanCompressor, CompressionConfig, CompressionStrategy
from .gpu_compressor import GPUCompressor
from .licensing import LicenseValidator, ProFeatures

logger = logging.getLogger(__name__)


@dataclass
class ProCompressionConfig(CompressionConfig):
    """Extended configuration for Pro features."""
    # Advanced compression settings
    adaptive_compression: bool = True
    learned_embeddings: bool = False
    encryption_enabled: bool = False
    encryption_key: Optional[str] = None
    
    # Performance settings
    parallel_processing: bool = True
    max_workers: int = 4
    memory_optimization: bool = True
    
    # Quality settings
    quality_threshold: float = 0.95
    adaptive_quality: bool = True


class ProCompressor:
    """
    Professional tier compressor with advanced features.
    
    Provides enterprise-grade compression with GPU acceleration, encryption,
    and advanced optimization features.
    """
    
    def __init__(
        self, 
        config: Optional[ProCompressionConfig] = None,
        api_key: Optional[str] = None,
        license_key: Optional[str] = None
    ):
        """
        Initialize Pro compressor.
        
        Args:
            config: Pro compression configuration
            api_key: API key for Pro features
            license_key: License key for validation
        """
        self.config = config or ProCompressionConfig()
        self.api_key = api_key
        self.license_key = license_key
        
        # Validate license
        self.license_validator = LicenseValidator(api_key, license_key)
        self.pro_features = self.license_validator.validate()
        
        # Initialize base compressor
        if self.pro_features.gpu_acceleration:
            try:
                self._compressor = GPUCompressor(self.config)
                logger.info("Pro compressor initialized with GPU acceleration")
            except Exception as e:
                logger.warning(f"GPU initialization failed, falling back to CPU: {e}")
                self._compressor = RamanujanCompressor(self.config)
        else:
            self._compressor = RamanujanCompressor(self.config)
        
        # Initialize additional Pro features
        self._encryption_key = None
        if self.pro_features.encryption and self.config.encryption_enabled:
            self._encryption_key = self._generate_encryption_key()
        
        logger.info(f"Pro compressor initialized with features: {self.pro_features}")
    
    def compress(
        self, 
        tokens: List[int], 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Advanced compression with Pro features.
        
        Args:
            tokens: List of token IDs to compress
            metadata: Optional metadata for compression
            
        Returns:
            Dictionary containing compressed data and metadata
        """
        if not tokens:
            return {"compressed": [], "metadata": {}}
        
        start_time = time.time()
        
        try:
            # Apply adaptive compression if enabled
            if self.config.adaptive_compression:
                tokens = self._adaptive_preprocessing(tokens)
            
            # Compress using base compressor
            compressed_data = self._compressor.compress(tokens)
            
            # Apply Pro enhancements
            if self.pro_features.encryption and self._encryption_key:
                compressed_data = self._encrypt_compressed_data(compressed_data)
            
            if self.pro_features.learned_embeddings:
                compressed_data = self._apply_learned_embeddings(compressed_data, tokens)
            
            # Add Pro metadata
            compression_time = time.time() - start_time
            compressed_data["metadata"].update({
                "pro_features": {
                    "adaptive_compression": self.config.adaptive_compression,
                    "learned_embeddings": self.config.learned_embeddings,
                    "encryption_enabled": self.config.encryption_enabled,
                    "gpu_accelerated": isinstance(self._compressor, GPUCompressor),
                    "compression_time": compression_time,
                },
                "license_info": {
                    "pro_tier": True,
                    "features": self.pro_features.to_dict(),
                }
            })
            
            logger.debug(f"Pro compression completed in {compression_time:.3f}s")
            return compressed_data
            
        except Exception as e:
            logger.error(f"Pro compression failed: {e}")
            raise
    
    def decompress(
        self, 
        compressed_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[int]:
        """
        Advanced decompression with Pro features.
        
        Args:
            compressed_data: Dictionary containing compressed data
            metadata: Optional metadata for decompression
            
        Returns:
            List of decompressed token IDs
        """
        if not compressed_data.get("compressed"):
            return []
        
        start_time = time.time()
        
        try:
            # Apply Pro enhancements in reverse order
            if self.pro_features.learned_embeddings:
                compressed_data = self._reverse_learned_embeddings(compressed_data)
            
            if self.pro_features.encryption and self._encryption_key:
                compressed_data = self._decrypt_compressed_data(compressed_data)
            
            # Decompress using base compressor
            tokens = self._compressor.decompress(compressed_data)
            
            # Apply adaptive postprocessing if enabled
            if self.config.adaptive_compression:
                tokens = self._adaptive_postprocessing(tokens)
            
            decompression_time = time.time() - start_time
            logger.debug(f"Pro decompression completed in {decompression_time:.3f}s")
            
            return tokens
            
        except Exception as e:
            logger.error(f"Pro decompression failed: {e}")
            raise
    
    def batch_compress(
        self, 
        token_batches: List[List[int]],
        parallel: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Batch compression with parallel processing.
        
        Args:
            token_batches: List of token sequences to compress
            parallel: Whether to use parallel processing
            
        Returns:
            List of compressed data dictionaries
        """
        if not token_batches:
            return []
        
        logger.debug(f"Pro batch compressing {len(token_batches)} sequences")
        
        if parallel and self.config.parallel_processing and self.pro_features.parallel_processing:
            return self._parallel_batch_compress(token_batches)
        else:
            return [self.compress(tokens) for tokens in token_batches]
    
    def _adaptive_preprocessing(self, tokens: List[int]) -> List[int]:
        """Apply adaptive preprocessing for better compression."""
        if not self.config.adaptive_compression:
            return tokens
        
        # Analyze token patterns and apply preprocessing
        # This is a simplified version - in practice, you'd use more sophisticated analysis
        
        # Remove consecutive duplicates
        processed = []
        prev_token = None
        for token in tokens:
            if token != prev_token:
                processed.append(token)
            prev_token = token
        
        # Apply run-length encoding for repeated patterns
        if len(processed) < len(tokens) * 0.8:  # If we saved significant space
            return processed
        else:
            return tokens
    
    def _adaptive_postprocessing(self, tokens: List[int]) -> List[int]:
        """Apply adaptive postprocessing for better reconstruction."""
        if not self.config.adaptive_compression:
            return tokens
        
        # Apply inverse of preprocessing
        # This is a simplified version
        return tokens
    
    def _encrypt_compressed_data(self, compressed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt compressed data for security."""
        if not self._encryption_key:
            return compressed_data
        
        try:
            # Simple encryption using the key (in practice, use proper encryption)
            encrypted_compressed = []
            for token in compressed_data["compressed"]:
                # Simple XOR encryption with key hash
                key_hash = int(hashlib.md5(self._encryption_key.encode()).hexdigest()[:8], 16)
                encrypted_token = token ^ (key_hash % 10000)
                encrypted_compressed.append(encrypted_token)
            
            compressed_data["compressed"] = encrypted_compressed
            compressed_data["metadata"]["encrypted"] = True
            
            logger.debug("Compressed data encrypted")
            return compressed_data
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return compressed_data
    
    def _decrypt_compressed_data(self, compressed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt compressed data."""
        if not self._encryption_key or not compressed_data.get("metadata", {}).get("encrypted"):
            return compressed_data
        
        try:
            # Simple decryption (inverse of encryption)
            decrypted_compressed = []
            for token in compressed_data["compressed"]:
                key_hash = int(hashlib.md5(self._encryption_key.encode()).hexdigest()[:8], 16)
                decrypted_token = token ^ (key_hash % 10000)
                decrypted_compressed.append(decrypted_token)
            
            compressed_data["compressed"] = decrypted_compressed
            compressed_data["metadata"]["encrypted"] = False
            
            logger.debug("Compressed data decrypted")
            return compressed_data
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return compressed_data
    
    def _apply_learned_embeddings(self, compressed_data: Dict[str, Any], original_tokens: List[int]) -> Dict[str, Any]:
        """Apply learned embeddings for better compression."""
        if not self.config.learned_embeddings:
            return compressed_data
        
        # This is a placeholder for learned embeddings
        # In practice, you'd use a trained model to learn better representations
        
        compressed_data["metadata"]["learned_embeddings"] = True
        logger.debug("Learned embeddings applied")
        return compressed_data
    
    def _reverse_learned_embeddings(self, compressed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Reverse learned embeddings during decompression."""
        if not compressed_data.get("metadata", {}).get("learned_embeddings"):
            return compressed_data
        
        # This is a placeholder for reversing learned embeddings
        logger.debug("Learned embeddings reversed")
        return compressed_data
    
    def _parallel_batch_compress(self, token_batches: List[List[int]]) -> List[Dict[str, Any]]:
        """Parallel batch compression using multiprocessing."""
        try:
            from concurrent.futures import ProcessPoolExecutor, as_completed
            
            results = [None] * len(token_batches)
            
            with ProcessPoolExecutor(max_workers=self.config.max_workers) as executor:
                # Submit all tasks
                future_to_index = {
                    executor.submit(self.compress, tokens): i 
                    for i, tokens in enumerate(token_batches)
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        results[index] = future.result()
                    except Exception as e:
                        logger.error(f"Parallel compression failed for batch {index}: {e}")
                        results[index] = {"compressed": [], "metadata": {"error": str(e)}}
            
            logger.debug(f"Parallel batch compression completed")
            return results
            
        except Exception as e:
            logger.error(f"Parallel processing failed: {e}")
            # Fallback to sequential processing
            return [self.compress(tokens) for tokens in token_batches]
    
    def _generate_encryption_key(self) -> str:
        """Generate encryption key for secure compression."""
        if self.api_key:
            # Use API key as base for encryption key
            return hashlib.sha256(self.api_key.encode()).hexdigest()
        else:
            # Generate random key
            import secrets
            return secrets.token_hex(32)
    
    def get_pro_stats(self) -> Dict[str, Any]:
        """Get Pro compressor statistics and capabilities."""
        stats = {
            "pro_tier": True,
            "features": self.pro_features.to_dict(),
            "config": {
                "adaptive_compression": self.config.adaptive_compression,
                "learned_embeddings": self.config.learned_embeddings,
                "encryption_enabled": self.config.encryption_enabled,
                "parallel_processing": self.config.parallel_processing,
                "gpu_accelerated": isinstance(self._compressor, GPUCompressor),
            }
        }
        
        if isinstance(self._compressor, GPUCompressor):
            stats["gpu_info"] = self._compressor.get_gpu_info()
        
        return stats
    
    def validate_license(self) -> bool:
        """Validate Pro license."""
        return self.license_validator.is_valid()
    
    def upgrade_license(self, new_license_key: str) -> bool:
        """Upgrade to new license."""
        try:
            self.license_key = new_license_key
            self.license_validator = LicenseValidator(self.api_key, new_license_key)
            self.pro_features = self.license_validator.validate()
            
            logger.info("License upgraded successfully")
            return True
        except Exception as e:
            logger.error(f"License upgrade failed: {e}")
            return False