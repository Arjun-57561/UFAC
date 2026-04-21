# File: core/constants.py
"""
Constants for UFAC Engine.
Centralized configuration values to avoid magic numbers.
"""

# Eligibility thresholds
AGGREGATION_THRESHOLD_FACTS = 0.6       # Higher — facts need more agreement
AGGREGATION_THRESHOLD_ASSUMPTIONS = 0.4
AGGREGATION_THRESHOLD_UNKNOWNS = 0.4
AGGREGATION_THRESHOLD_STEPS = 0.4

# Confidence thresholds
CONFIDENCE_HIGH = 80
CONFIDENCE_MEDIUM = 65
CONFIDENCE_LOW = 40

# Risk levels
RISK_HIGH_THRESHOLD = 40
RISK_MEDIUM_THRESHOLD = 70

# LLM council
DEFAULT_COUNCIL_RUNS = 3
MAX_LLM_TEMPERATURE = 1.0
LLM_TIMEOUT_DEFAULT = 15.0
MAX_OUTPUT_TOKENS = 500

# Input validation
MAX_STRING_LENGTH = 200
MAX_INCOME_VALUE = 100_000_000.0
