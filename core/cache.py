# File: core/cache.py
"""
Caching layer for UFAC Engine.

Implements in-memory caching with TTL (Time-To-Live) for:
- Identical assessment requests
- RAG retrieval results
- LLM responses

Reduces redundant LLM calls and improves response times.
"""

import os
import hashlib
import json
import logging
import time
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheEntry:
    """Represents a single cache entry with TTL."""
    
    def __init__(self, value: Any, ttl_seconds: int = 3600):
        """
        Initialize cache entry.
        
        Args:
            value: The cached value
            ttl_seconds: Time-to-live in seconds (default: 1 hour)
        """
        self.value = value
        self.created_at = time.time()
        self.ttl_seconds = ttl_seconds
        self.access_count = 0
        self.last_accessed = self.created_at
    
    def is_expired(self) -> bool:
        """Check if cache entry has expired."""
        return time.time() - self.created_at > self.ttl_seconds
    
    def access(self) -> Any:
        """Access the cache entry and update stats."""
        self.access_count += 1
        self.last_accessed = time.time()
        return self.value
    
    def age_seconds(self) -> float:
        """Get age of cache entry in seconds."""
        return time.time() - self.created_at


class Cache:
    """In-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 3600):
        """
        Initialize cache.
        
        Args:
            default_ttl: Default TTL in seconds (default: 1 hour)
        """
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "total_requests": 0,
        }
    
    def generate_key(self, data: Dict[str, Any]) -> str:
        """Generate cache key from data dictionary."""
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(sorted_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        self._stats["total_requests"] += 1
        
        if key not in self._cache:
            logger.debug(f"Cache miss: {key}")
            self._stats["misses"] += 1
            return None
        
        entry = self._cache[key]
        
        if entry.is_expired():
            logger.debug(f"Cache expired: {key}")
            del self._cache[key]
            self._stats["misses"] += 1
            self._stats["evictions"] += 1
            return None
        
        logger.debug(f"Cache hit: {key} (age: {entry.age_seconds():.1f}s, accesses: {entry.access_count})")
        self._stats["hits"] += 1
        return entry.access()
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: TTL in seconds (uses default if not specified)
        """
        ttl = ttl_seconds or self._default_ttl
        self._cache[key] = CacheEntry(value, ttl)
        logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted: {key}")
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"Cache cleared: {count} entries removed")
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.
        
        Returns:
            Number of entries removed
        """
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        if expired_keys:
            logger.debug(f"Cache cleanup: {len(expired_keys)} expired entries removed")
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        self.cleanup_expired()
        
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = (self._stats["hits"] / total * 100) if total > 0 else 0
        
        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": f"{hit_rate:.1f}%",
            "evictions": self._stats["evictions"],
            "total_requests": self._stats["total_requests"],
            "cached_entries": len(self._cache),
            "memory_usage": self._get_memory_usage(),
        }
    
    def _get_memory_usage(self) -> str:
        """Estimate memory usage of cache."""
        import sys
        total_size = sum(sys.getsizeof(entry.value) for entry in self._cache.values())
        
        if total_size < 1024:
            return f"{total_size} B"
        elif total_size < 1024 * 1024:
            return f"{total_size / 1024:.1f} KB"
        else:
            return f"{total_size / (1024 * 1024):.1f} MB"
    
    def __len__(self) -> int:
        """Get number of cached entries."""
        return len(self._cache)
    
    def __repr__(self) -> str:
        """String representation of cache."""
        return f"Cache(entries={len(self._cache)}, hits={self._stats['hits']}, misses={self._stats['misses']})"


# Global cache instances with configurable TTL
_assessment_cache = Cache(default_ttl=int(os.getenv("CACHE_TTL_ASSESSMENT", "3600")))  # 1 hour for assessments
_rag_cache = Cache(default_ttl=int(os.getenv("CACHE_TTL_RAG", "7200")))  # 2 hours for RAG results
_llm_cache = Cache(default_ttl=int(os.getenv("CACHE_TTL_LLM", "3600")))  # 1 hour for LLM responses


def get_assessment_cache() -> Cache:
    """Get the global assessment cache."""
    return _assessment_cache


def get_rag_cache() -> Cache:
    """Get the global RAG cache."""
    return _rag_cache


def get_llm_cache() -> Cache:
    """Get the global LLM cache."""
    return _llm_cache


def clear_all_caches() -> None:
    """Clear all cache instances."""
    logger.info("Clearing all caches...")
    _assessment_cache.clear()
    _rag_cache.clear()
    _llm_cache.clear()
    logger.info("All caches cleared")


def get_all_cache_stats() -> Dict[str, Any]:
    """Get statistics for all caches."""
    return {
        "assessment_cache": _assessment_cache.get_stats(),
        "rag_cache": _rag_cache.get_stats(),
        "llm_cache": _llm_cache.get_stats(),
    }
