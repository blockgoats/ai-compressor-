"""
Licensing System for Ramanujan Pro

Handles license validation and feature access control for Pro tier features.
"""

import logging
import hashlib
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class ProFeatures:
    """Pro tier features and capabilities."""
    gpu_acceleration: bool = False
    encryption: bool = False
    parallel_processing: bool = False
    learned_embeddings: bool = False
    extended_context: bool = False
    priority_support: bool = False
    api_access: bool = False
    custom_models: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "gpu_acceleration": self.gpu_acceleration,
            "encryption": self.encryption,
            "parallel_processing": self.parallel_processing,
            "learned_embeddings": self.learned_embeddings,
            "extended_context": self.extended_context,
            "priority_support": self.priority_support,
            "api_access": self.api_access,
            "custom_models": self.custom_models,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProFeatures':
        """Create from dictionary."""
        return cls(**data)


class LicenseValidator:
    """
    License validation system for Pro tier features.
    
    Handles license key validation, feature access control, and usage tracking.
    """
    
    def __init__(self, api_key: Optional[str] = None, license_key: Optional[str] = None):
        """
        Initialize license validator.
        
        Args:
            api_key: API key for online validation
            license_key: License key for offline validation
        """
        self.api_key = api_key
        self.license_key = license_key
        self._cached_features = None
        self._cache_expiry = None
        
        # License tiers and their features
        self._license_tiers = {
            "free": ProFeatures(),
            "basic": ProFeatures(
                parallel_processing=True,
                extended_context=True,
            ),
            "pro": ProFeatures(
                gpu_acceleration=True,
                encryption=True,
                parallel_processing=True,
                learned_embeddings=True,
                extended_context=True,
                priority_support=True,
            ),
            "enterprise": ProFeatures(
                gpu_acceleration=True,
                encryption=True,
                parallel_processing=True,
                learned_embeddings=True,
                extended_context=True,
                priority_support=True,
                api_access=True,
                custom_models=True,
            ),
        }
    
    def validate(self) -> ProFeatures:
        """
        Validate license and return available features.
        
        Returns:
            ProFeatures object with available capabilities
        """
        # Check cache first
        if self._cached_features and self._cache_expiry and time.time() < self._cache_expiry:
            return self._cached_features
        
        try:
            # Try online validation first
            if self.api_key:
                features = self._validate_online()
            elif self.license_key:
                features = self._validate_offline()
            else:
                features = self._license_tiers["free"]
            
            # Cache results for 1 hour
            self._cached_features = features
            self._cache_expiry = time.time() + 3600
            
            logger.info(f"License validated. Features: {features.to_dict()}")
            return features
            
        except Exception as e:
            logger.error(f"License validation failed: {e}")
            # Return free tier on validation failure
            return self._license_tiers["free"]
    
    def _validate_online(self) -> ProFeatures:
        """Validate license online using API key."""
        if not self.api_key:
            return self._license_tiers["free"]
        
        try:
            # In practice, this would make an API call to validate the key
            # For now, we'll simulate based on key format
            
            if self.api_key.startswith("sk_live_"):
                # Live API key - check with Stripe or similar
                return self._validate_stripe_key()
            elif self.api_key.startswith("sk_test_"):
                # Test API key
                return self._license_tiers["pro"]
            else:
                # Invalid key format
                return self._license_tiers["free"]
                
        except Exception as e:
            logger.error(f"Online validation failed: {e}")
            return self._license_tiers["free"]
    
    def _validate_offline(self) -> ProFeatures:
        """Validate license offline using license key."""
        if not self.license_key:
            return self._license_tiers["free"]
        
        try:
            # Decode license key (simplified)
            license_data = self._decode_license_key(self.license_key)
            
            if not license_data:
                return self._license_tiers["free"]
            
            # Check expiration
            if license_data.get("expires_at"):
                expires_at = datetime.fromisoformat(license_data["expires_at"])
                if datetime.now() > expires_at:
                    logger.warning("License has expired")
                    return self._license_tiers["free"]
            
            # Get tier and return features
            tier = license_data.get("tier", "free")
            return self._license_tiers.get(tier, self._license_tiers["free"])
            
        except Exception as e:
            logger.error(f"Offline validation failed: {e}")
            return self._license_tiers["free"]
    
    def _validate_stripe_key(self) -> ProFeatures:
        """Validate Stripe API key (simplified simulation)."""
        # In practice, this would make a real API call to Stripe
        # For now, we'll simulate based on key characteristics
        
        try:
            # Simulate API call delay
            time.sleep(0.1)
            
            # Check if key is valid (simplified)
            if len(self.api_key) > 20 and self.api_key.startswith("sk_live_"):
                # Simulate successful validation
                return self._license_tiers["pro"]
            else:
                return self._license_tiers["free"]
                
        except Exception as e:
            logger.error(f"Stripe validation failed: {e}")
            return self._license_tiers["free"]
    
    def _decode_license_key(self, license_key: str) -> Optional[Dict[str, Any]]:
        """Decode license key to extract information."""
        try:
            # Simple base64-like decoding (in practice, use proper encryption)
            import base64
            
            # Remove any prefixes
            key = license_key.replace("ramanujan_", "").replace("pro_", "")
            
            # Decode base64
            decoded = base64.b64decode(key + "==")  # Add padding
            data = json.loads(decoded.decode('utf-8'))
            
            # Verify signature (simplified)
            if self._verify_license_signature(data):
                return data
            else:
                return None
                
        except Exception as e:
            logger.error(f"License key decoding failed: {e}")
            return None
    
    def _verify_license_signature(self, data: Dict[str, Any]) -> bool:
        """Verify license signature (simplified)."""
        try:
            # In practice, use proper cryptographic signature verification
            signature = data.get("signature", "")
            data_without_sig = {k: v for k, v in data.items() if k != "signature"}
            
            # Simple hash verification (in practice, use proper HMAC)
            expected_sig = hashlib.sha256(
                json.dumps(data_without_sig, sort_keys=True).encode()
            ).hexdigest()[:16]
            
            return signature == expected_sig
            
        except Exception as e:
            logger.error(f"Signature verification failed: {e}")
            return False
    
    def is_valid(self) -> bool:
        """Check if current license is valid."""
        features = self.validate()
        return features != self._license_tiers["free"]
    
    def get_license_info(self) -> Dict[str, Any]:
        """Get detailed license information."""
        features = self.validate()
        
        info = {
            "valid": self.is_valid(),
            "features": features.to_dict(),
            "tier": self._get_tier_from_features(features),
            "api_key_provided": self.api_key is not None,
            "license_key_provided": self.license_key is not None,
        }
        
        if self.license_key:
            try:
                license_data = self._decode_license_key(self.license_key)
                if license_data:
                    info.update({
                        "issued_at": license_data.get("issued_at"),
                        "expires_at": license_data.get("expires_at"),
                        "customer": license_data.get("customer"),
                    })
            except Exception as e:
                logger.error(f"Failed to get license info: {e}")
        
        return info
    
    def _get_tier_from_features(self, features: ProFeatures) -> str:
        """Determine tier from features."""
        for tier, tier_features in self._license_tiers.items():
            if features.to_dict() == tier_features.to_dict():
                return tier
        return "unknown"
    
    def generate_license_key(
        self, 
        tier: str, 
        customer: str, 
        expires_days: int = 365,
        private_key: Optional[str] = None
    ) -> str:
        """
        Generate a new license key (for testing/development).
        
        Args:
            tier: License tier (free, basic, pro, enterprise)
            customer: Customer identifier
            expires_days: Days until expiration
            private_key: Private key for signing (optional)
            
        Returns:
            Generated license key
        """
        try:
            expires_at = datetime.now() + timedelta(days=expires_days)
            
            license_data = {
                "tier": tier,
                "customer": customer,
                "issued_at": datetime.now().isoformat(),
                "expires_at": expires_at.isoformat(),
                "version": "1.0",
            }
            
            # Generate signature
            data_without_sig = license_data.copy()
            signature = hashlib.sha256(
                json.dumps(data_without_sig, sort_keys=True).encode()
            ).hexdigest()[:16]
            license_data["signature"] = signature
            
            # Encode as base64
            import base64
            encoded = base64.b64encode(
                json.dumps(license_data).encode('utf-8')
            ).decode('utf-8')
            
            return f"ramanujan_{tier}_{encoded}"
            
        except Exception as e:
            logger.error(f"License key generation failed: {e}")
            raise
    
    def check_usage_limits(self, operation: str) -> bool:
        """Check if operation is within usage limits."""
        # This is a placeholder for usage tracking
        # In practice, you'd track usage against license limits
        
        if not self.is_valid():
            return False
        
        # For now, allow all operations for valid licenses
        return True
    
    def track_usage(self, operation: str, details: Optional[Dict[str, Any]] = None):
        """Track usage for billing and monitoring."""
        # This is a placeholder for usage tracking
        # In practice, you'd send usage data to your billing system
        
        if not self.is_valid():
            return
        
        logger.debug(f"Usage tracked: {operation} - {details}")
    
    def refresh_license(self) -> bool:
        """Refresh license from server."""
        try:
            # Clear cache
            self._cached_features = None
            self._cache_expiry = None
            
            # Re-validate
            features = self.validate()
            
            logger.info("License refreshed successfully")
            return True
            
        except Exception as e:
            logger.error(f"License refresh failed: {e}")
            return False