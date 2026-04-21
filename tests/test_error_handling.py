# File: tests/test_error_handling.py
"""Tests for error handling."""

import pytest
from core.llm_utils import LLMError, LLMInitializationError, LLMCallError
from data.rag_pipeline import RAGError, RAGInitializationError
from core.ufac_engine import UFACError


class TestExceptionHierarchy:
    """Test exception hierarchy."""
    
    def test_llm_error_inheritance(self):
        """Test LLM error inheritance."""
        error = LLMError("test")
        assert isinstance(error, Exception)
    
    def test_llm_initialization_error_inheritance(self):
        """Test LLM initialization error inheritance."""
        error = LLMInitializationError("test")
        assert isinstance(error, LLMError)
        assert isinstance(error, Exception)
    
    def test_llm_call_error_inheritance(self):
        """Test LLM call error inheritance."""
        error = LLMCallError("test")
        assert isinstance(error, LLMError)
        assert isinstance(error, Exception)
    
    def test_rag_error_inheritance(self):
        """Test RAG error inheritance."""
        error = RAGError("test")
        assert isinstance(error, Exception)
    
    def test_rag_initialization_error_inheritance(self):
        """Test RAG initialization error inheritance."""
        error = RAGInitializationError("test")
        assert isinstance(error, RAGError)
        assert isinstance(error, Exception)
    
    def test_ufac_error_inheritance(self):
        """Test UFAC error inheritance."""
        error = UFACError("test")
        assert isinstance(error, Exception)


class TestExceptionMessages:
    """Test exception messages."""
    
    def test_llm_error_message(self):
        """Test LLM error message."""
        error = LLMError("test message")
        assert str(error) == "test message"
    
    def test_llm_initialization_error_message(self):
        """Test LLM initialization error message."""
        error = LLMInitializationError("init failed")
        assert "init failed" in str(error)
    
    def test_ufac_error_message(self):
        """Test UFAC error message."""
        error = UFACError("assessment failed")
        assert "assessment failed" in str(error)
