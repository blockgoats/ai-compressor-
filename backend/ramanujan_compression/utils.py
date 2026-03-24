"""
Utility functions for Ramanujan Compression SDK.
"""

import time
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Results from compression benchmarking."""
    compression_ratio: float
    compression_time: float
    decompression_time: float
    memory_usage: float
    quality_score: float


def benchmark_compression(
    compressor,
    test_tokens: List[List[int]],
    iterations: int = 3
) -> BenchmarkResult:
    """
    Benchmark compression performance.
    
    Args:
        compressor: RamanujanCompressor instance
        test_tokens: List of token sequences to test
        iterations: Number of iterations to average
        
    Returns:
        BenchmarkResult with performance metrics
    """
    logger.info(f"Benchmarking compression with {len(test_tokens)} test sequences")
    
    compression_times = []
    decompression_times = []
    compression_ratios = []
    quality_scores = []
    
    for iteration in range(iterations):
        total_compression_time = 0
        total_decompression_time = 0
        total_original_length = 0
        total_compressed_length = 0
        total_quality_score = 0
        
        for tokens in test_tokens:
            if not tokens:
                continue
                
            # Compression timing
            start_time = time.time()
            compressed_data = compressor.compress(tokens)
            compression_time = time.time() - start_time
            total_compression_time += compression_time
            
            # Decompression timing
            start_time = time.time()
            decompressed_tokens = compressor.decompress(compressed_data)
            decompression_time = time.time() - start_time
            total_decompression_time += decompression_time
            
            # Calculate metrics
            original_length = len(tokens)
            compressed_length = len(compressed_data["compressed"])
            total_original_length += original_length
            total_compressed_length += compressed_length
            
            # Quality score (simplified - in practice, use more sophisticated metrics)
            quality_score = _calculate_quality_score(tokens, decompressed_tokens)
            total_quality_score += quality_score
        
        # Store iteration results
        compression_times.append(total_compression_time)
        decompression_times.append(total_decompression_time)
        compression_ratios.append(total_compressed_length / total_original_length if total_original_length > 0 else 0)
        quality_scores.append(total_quality_score / len(test_tokens) if test_tokens else 0)
    
    # Calculate averages
    avg_compression_time = np.mean(compression_times)
    avg_decompression_time = np.mean(decompression_times)
    avg_compression_ratio = np.mean(compression_ratios)
    avg_quality_score = np.mean(quality_scores)
    
    # Estimate memory usage (simplified)
    memory_usage = _estimate_memory_usage(test_tokens, avg_compression_ratio)
    
    return BenchmarkResult(
        compression_ratio=avg_compression_ratio,
        compression_time=avg_compression_time,
        decompression_time=avg_decompression_time,
        memory_usage=memory_usage,
        quality_score=avg_quality_score
    )


def _calculate_quality_score(original: List[int], reconstructed: List[int]) -> float:
    """
    Calculate quality score for compression.
    
    Args:
        original: Original token sequence
        reconstructed: Reconstructed token sequence
        
    Returns:
        Quality score between 0 and 1 (1 = perfect reconstruction)
    """
    if not original and not reconstructed:
        return 1.0
    
    if not original or not reconstructed:
        return 0.0
    
    # Simple quality metric based on sequence similarity
    min_length = min(len(original), len(reconstructed))
    if min_length == 0:
        return 0.0
    
    # Calculate element-wise accuracy
    matches = sum(1 for i in range(min_length) if original[i] == reconstructed[i])
    accuracy = matches / min_length
    
    # Penalize length differences
    length_penalty = 1.0 - abs(len(original) - len(reconstructed)) / max(len(original), len(reconstructed))
    
    return accuracy * length_penalty


def _estimate_memory_usage(tokens: List[List[int]], compression_ratio: float) -> float:
    """
    Estimate memory usage in MB.
    
    Args:
        tokens: Test token sequences
        compression_ratio: Average compression ratio
        
    Returns:
        Estimated memory usage in MB
    """
    total_tokens = sum(len(seq) for seq in tokens)
    # Estimate 4 bytes per token (int32)
    original_memory = total_tokens * 4 / (1024 * 1024)  # Convert to MB
    compressed_memory = original_memory * compression_ratio
    return compressed_memory


def save_compression_config(config, filepath: str):
    """
    Save compression configuration to file.
    
    Args:
        config: CompressionConfig instance
        filepath: Path to save configuration
    """
    config_dict = {
        "strategy": config.strategy.value,
        "compression_ratio": config.compression_ratio,
        "modular_base": config.modular_base,
        "sparse_threshold": config.sparse_threshold,
        "context_length": config.context_length,
        "gpu_acceleration": config.gpu_acceleration,
    }
    
    with open(filepath, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    logger.info(f"Configuration saved to {filepath}")


def load_compression_config(filepath: str) -> 'CompressionConfig':
    """
    Load compression configuration from file.
    
    Args:
        filepath: Path to configuration file
        
    Returns:
        CompressionConfig instance
    """
    with open(filepath, 'r') as f:
        config_dict = json.load(f)
    
    # Convert strategy string back to enum
    config_dict["strategy"] = CompressionStrategy(config_dict["strategy"])
    
    return CompressionConfig(**config_dict)


def create_sample_tokens(length: int = 100, vocab_size: int = 1000) -> List[int]:
    """
    Create sample token sequence for testing.
    
    Args:
        length: Length of token sequence
        vocab_size: Vocabulary size
        
    Returns:
        List of random token IDs
    """
    return np.random.randint(0, vocab_size, size=length).tolist()


def validate_compression(original: List[int], compressed_data: Dict[str, Any], decompressed: List[int]) -> bool:
    """
    Validate compression/decompression round-trip.
    
    Args:
        original: Original token sequence
        compressed_data: Compressed data
        decompressed: Decompressed token sequence
        
    Returns:
        True if validation passes
    """
    # Check basic properties
    if not isinstance(compressed_data, dict):
        logger.error("Compressed data should be a dictionary")
        return False
    
    if "compressed" not in compressed_data:
        logger.error("Compressed data missing 'compressed' field")
        return False
    
    if "metadata" not in compressed_data:
        logger.error("Compressed data missing 'metadata' field")
        return False
    
    # Check metadata
    metadata = compressed_data["metadata"]
    required_fields = ["original_length", "compressed_length", "strategy"]
    for field in required_fields:
        if field not in metadata:
            logger.error(f"Metadata missing required field: {field}")
            return False
    
    # Check lengths
    if metadata["original_length"] != len(original):
        logger.error("Original length mismatch")
        return False
    
    if metadata["compressed_length"] != len(compressed_data["compressed"]):
        logger.error("Compressed length mismatch")
        return False
    
    # Check decompression quality (simplified)
    if len(decompressed) != len(original):
        logger.warning(f"Length mismatch: original={len(original)}, decompressed={len(decompressed)}")
    
    logger.info("Compression validation passed")
    return True


def setup_logging(level: str = "INFO"):
    """
    Setup logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set specific loggers
    logger.setLevel(getattr(logging, level.upper()))
    
    logger.info(f"Logging configured at {level} level")