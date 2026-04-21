# File: core/metrics.py
"""Metrics collection for UFAC Engine."""

import logging
import time
from typing import Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class Metrics:
    """Metrics collection and tracking."""
    
    def __init__(self):
        """Initialize metrics."""
        self._metrics = {
            "requests": {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "cached": 0,
            },
            "latency": {
                "total_time": 0.0,
                "min_time": float('inf'),
                "max_time": 0.0,
                "avg_time": 0.0,
            },
            "agents": {
                "fact": {"runs": 0, "failures": 0},
                "assumption": {"runs": 0, "failures": 0},
                "unknown": {"runs": 0, "failures": 0},
                "confidence": {"runs": 0, "failures": 0},
                "decision": {"runs": 0, "failures": 0},
            },
            "errors": {
                "llm_errors": 0,
                "rag_errors": 0,
                "ufac_errors": 0,
                "other_errors": 0,
            },
            "cache": {
                "hits": 0,
                "misses": 0,
            },
            "started_at": datetime.now().isoformat(),
        }
    
    def record_request(self, success: bool, latency: float, cached: bool = False) -> None:
        """Record request metrics."""
        self._metrics["requests"]["total"] += 1
        if success:
            self._metrics["requests"]["successful"] += 1
        else:
            self._metrics["requests"]["failed"] += 1
        
        if cached:
            self._metrics["requests"]["cached"] += 1
        
        # Update latency metrics
        self._metrics["latency"]["total_time"] += latency
        self._metrics["latency"]["min_time"] = min(self._metrics["latency"]["min_time"], latency)
        self._metrics["latency"]["max_time"] = max(self._metrics["latency"]["max_time"], latency)
        
        if self._metrics["requests"]["total"] > 0:
            self._metrics["latency"]["avg_time"] = (
                self._metrics["latency"]["total_time"] / self._metrics["requests"]["total"]
            )
    
    def record_agent_run(self, agent_name: str, success: bool = True) -> None:
        """Record agent run."""
        if agent_name in self._metrics["agents"]:
            self._metrics["agents"][agent_name]["runs"] += 1
            if not success:
                self._metrics["agents"][agent_name]["failures"] += 1
    
    def record_error(self, error_type: str) -> None:
        """Record error."""
        if error_type in self._metrics["errors"]:
            self._metrics["errors"][error_type] += 1
    
    def record_cache_hit(self) -> None:
        """Record cache hit."""
        self._metrics["cache"]["hits"] += 1
    
    def record_cache_miss(self) -> None:
        """Record cache miss."""
        self._metrics["cache"]["misses"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        total_cache = self._metrics["cache"]["hits"] + self._metrics["cache"]["misses"]
        cache_hit_rate = (
            (self._metrics["cache"]["hits"] / total_cache * 100) if total_cache > 0 else 0
        )
        
        success_rate = (
            (self._metrics["requests"]["successful"] / self._metrics["requests"]["total"] * 100)
            if self._metrics["requests"]["total"] > 0 else 0
        )
        
        return {
            "requests": self._metrics["requests"],
            "latency": {
                **self._metrics["latency"],
                "min_time": (
                    self._metrics["latency"]["min_time"]
                    if self._metrics["latency"]["min_time"] != float('inf') else 0
                ),
            },
            "agents": self._metrics["agents"],
            "errors": self._metrics["errors"],
            "cache": {
                **self._metrics["cache"],
                "hit_rate": f"{cache_hit_rate:.1f}%",
            },
            "success_rate": f"{success_rate:.1f}%",
            "started_at": self._metrics["started_at"],
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.__init__()


# Global metrics instance
_metrics = Metrics()


def get_metrics() -> Metrics:
    """Get global metrics instance."""
    return _metrics


def record_request(success: bool, latency: float, cached: bool = False) -> None:
    """Record request metrics."""
    _metrics.record_request(success, latency, cached)


def record_agent_run(agent_name: str, success: bool = True) -> None:
    """Record agent run."""
    _metrics.record_agent_run(agent_name, success)


def record_error(error_type: str) -> None:
    """Record error."""
    _metrics.record_error(error_type)


def record_cache_hit() -> None:
    """Record cache hit."""
    _metrics.record_cache_hit()


def record_cache_miss() -> None:
    """Record cache miss."""
    _metrics.record_cache_miss()


def get_all_metrics() -> Dict[str, Any]:
    """Get all metrics."""
    return _metrics.get_metrics()


def reset_metrics() -> None:
    """Reset all metrics."""
    _metrics.reset()
