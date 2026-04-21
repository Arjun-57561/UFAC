# File: core/database.py
"""
Database layer for UFAC Engine.
Stores assessment history with full results and metadata.
"""

import os
import uuid
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, select, desc

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./ufac_engine.db"
)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


class AssessmentRecord(Base):
    """Assessment record model."""
    __tablename__ = "assessments"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Input data
    occupation = Column(String, nullable=True)
    state = Column(String, nullable=True, index=True)
    district = Column(String, nullable=True)
    input_fields_count = Column(Integer, default=0)
    
    # Results
    answer = Column(Text)
    confidence = Column(Integer, index=True)
    risk_level = Column(String, index=True)
    known_facts = Column(JSON)
    assumptions = Column(JSON)
    unknowns = Column(JSON)
    next_steps = Column(JSON)
    
    # Consensus scores
    fact_consensus = Column(Float)
    assumption_consensus = Column(Float)
    unknown_consensus = Column(Float)
    confidence_consensus = Column(Float)
    decision_consensus = Column(Float)
    
    # Metadata
    response_time_ms = Column(Integer, nullable=True)
    was_cached = Column(Integer, default=0)  # 0/1 boolean


async def init_db():
    """Initialize database tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise


async def save_assessment(
    user_data: dict,
    result: "UFACResponse",
    response_time_ms: int = 0,
    was_cached: bool = False
) -> str:
    """
    Save assessment to database.
    
    Args:
        user_data: Input data from user
        result: UFACResponse object
        response_time_ms: Response time in milliseconds
        was_cached: Whether result was from cache
        
    Returns:
        Assessment ID
    """
    try:
        async with AsyncSessionLocal() as session:
            record = AssessmentRecord(
                occupation=user_data.get("occupation"),
                state=user_data.get("state"),
                district=user_data.get("district"),
                input_fields_count=len(user_data),
                answer=result.answer,
                confidence=result.confidence,
                risk_level=result.risk_level,
                known_facts=result.known_facts,
                assumptions=result.assumptions,
                unknowns=result.unknowns,
                next_steps=result.next_steps,
                fact_consensus=result.fact_consensus,
                assumption_consensus=result.assumption_consensus,
                unknown_consensus=result.unknown_consensus,
                confidence_consensus=result.confidence_consensus,
                decision_consensus=result.decision_consensus,
                response_time_ms=response_time_ms,
                was_cached=int(was_cached),
            )
            session.add(record)
            await session.commit()
            logger.debug(f"Saved assessment {record.id} to database")
            return record.id
    except Exception as e:
        logger.error(f"Failed to save assessment: {e}", exc_info=True)
        # Don't raise - saving to DB is non-critical
        return ""


async def get_assessment_history(limit: int = 20, offset: int = 0) -> list:
    """
    Get recent assessment history.
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
        
    Returns:
        List of assessment records
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(AssessmentRecord)
                .order_by(desc(AssessmentRecord.created_at))
                .limit(min(limit, 100))
                .offset(offset)
            )
            records = result.scalars().all()
            return [
                {
                    "id": r.id,
                    "created_at": r.created_at.isoformat(),
                    "occupation": r.occupation,
                    "state": r.state,
                    "district": r.district,
                    "answer": r.answer,
                    "confidence": r.confidence,
                    "risk_level": r.risk_level,
                    "response_time_ms": r.response_time_ms,
                    "was_cached": bool(r.was_cached),
                }
                for r in records
            ]
    except Exception as e:
        logger.error(f"Failed to get assessment history: {e}", exc_info=True)
        return []


async def get_assessment_by_id(assessment_id: str) -> Optional[dict]:
    """
    Get full assessment details by ID.
    
    Args:
        assessment_id: Assessment ID
        
    Returns:
        Assessment record or None
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.get(AssessmentRecord, assessment_id)
            if not result:
                return None
            
            return {
                "id": result.id,
                "created_at": result.created_at.isoformat(),
                "occupation": result.occupation,
                "state": result.state,
                "district": result.district,
                "input_fields_count": result.input_fields_count,
                "answer": result.answer,
                "confidence": result.confidence,
                "risk_level": result.risk_level,
                "known_facts": result.known_facts,
                "assumptions": result.assumptions,
                "unknowns": result.unknowns,
                "next_steps": result.next_steps,
                "fact_consensus": result.fact_consensus,
                "assumption_consensus": result.assumption_consensus,
                "unknown_consensus": result.unknown_consensus,
                "confidence_consensus": result.confidence_consensus,
                "decision_consensus": result.decision_consensus,
                "response_time_ms": result.response_time_ms,
                "was_cached": bool(result.was_cached),
            }
    except Exception as e:
        logger.error(f"Failed to get assessment {assessment_id}: {e}", exc_info=True)
        return None
