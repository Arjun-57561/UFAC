# File: tests/test_cache.py
"""Tests for caching layer."""

import pytest
import time
from core.cache import Cache, CacheEntry, get_assessment_cache, clear_all_caches


class TestCacheEntry:
    """Test CacheEntry class."""
    
    def test_cache_entry_creation(self):
        """Test cache entry creation."""
        entry = CacheEntry("test_value", ttl_seconds=60)
        assert entry.value == "test_value"
        assert entry.ttl_seconds == 60
        assert entry.access_count == 0
    
    def test_cache_entry_expiration(self):
        """Test cache entry expiration."""
        entry = CacheEntry("test_value", ttl_seconds=1)
        assert not entry.is_expired()
        time.sleep(1.1)
        assert entry.is_expired()
    
    def test_cache_entry_access(self):
        """Test cache entry access tracking."""
        entry = CacheEntry("test_value")
        value = entry.access()
        assert value == "test_value"
        assert entry.access_count == 1


class TestCache:
    """Test Cache class."""
    
    def test_cache_set_and_get(self):
        """Test cache set and get."""
        cache = Cache()
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_cache_miss(self):
        """Test cache miss."""
        cache = Cache()
        assert cache.get("nonexistent") is None
    
    def test_cache_expiration(self):
        """Test cache expiration."""
        cache = Cache(default_ttl=1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        time.sleep(1.1)
        assert cache.get("key1") is None
    
    def test_cache_delete(self):
        """Test cache delete."""
        cache = Cache()
        cache.set("key1", "value1")
        assert cache.delete("key1")
        assert cache.get("key1") is None
    
    def test_cache_clear(self):
        """Test cache clear."""
        cache = Cache()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert len(cache) == 0
    
    def test_cache_stats(self):
        """Test cache statistics."""
        cache = Cache()
        cache.set("key1", "value1")
        cache.get("key1")  # hit
        cache.get("key2")  # miss
        stats = cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert "hit_rate" in stats
    
    def test_cache_key_generation(self):
        """Test cache key generation."""
        cache = Cache()
        data1 = {"a": 1, "b": 2}
        data2 = {"b": 2, "a": 1}
        key1 = cache._generate_key(data1)
        key2 = cache._generate_key(data2)
        assert key1 == key2  # Same key for same data
    
    def test_cache_cleanup_expired(self):
        """Test cleanup of expired entries."""
        cache = Cache(default_ttl=1)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        time.sleep(1.1)
        removed = cache.cleanup_expired()
        assert removed == 2
        assert len(cache) == 0


class TestGlobalCaches:
    """Test global cache instances."""
    
    def test_get_assessment_cache(self):
        """Test getting assessment cache."""
        cache = get_assessment_cache()
        assert cache is not None
        assert isinstance(cache, Cache)
    
    def test_clear_all_caches(self):
        """Test clearing all caches."""
        cache = get_assessment_cache()
        cache.set("key1", "value1")
        clear_all_caches()
        assert cache.get("key1") is None
