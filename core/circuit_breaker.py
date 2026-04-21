import time
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing — reject all calls
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        name: str = "default"
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.name = name
        self._failure_count = 0
        self._last_failure_time: float = 0
        self._state = CircuitState.CLOSED
    
    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time > self.recovery_timeout:
                logger.info(f"Circuit {self.name}: OPEN → HALF_OPEN")
                self._state = CircuitState.HALF_OPEN
        return self._state
    
    def call_succeeded(self):
        self._failure_count = 0
        if self._state == CircuitState.HALF_OPEN:
            logger.info(f"Circuit {self.name}: HALF_OPEN → CLOSED")
        self._state = CircuitState.CLOSED
    
    def call_failed(self):
        self._failure_count += 1
        self._last_failure_time = time.time()
        if self._failure_count >= self.failure_threshold:
            logger.error(
                f"Circuit {self.name}: CLOSED → OPEN "
                f"(after {self._failure_count} failures)"
            )
            self._state = CircuitState.OPEN
    
    def is_open(self) -> bool:
        return self.state == CircuitState.OPEN
    
    def get_status(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self._failure_count,
            "last_failure": self._last_failure_time,
        }


# Global circuit breaker for Groq API
groq_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60,
    name="groq_api"
)
