#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Triage record data model for Intelligent Medical Guide System.

This module defines the TriageRecord class for representing and
storing triage consultation records.

Attributes:
    MAX_INPUT_LENGTH: Maximum length for input text.
"""

from typing import Optional, Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

MAX_INPUT_LENGTH = 500


class TriageRecord:
    """Data model class for triage records.
    
    This class represents a triage consultation record with its
    attributes and provides methods for data access and manipulation.
    
    Attributes:
        record_id: Unique identifier for the record.
        create_time: Timestamp when record was created.
        input_text: Original user input text.
        matched_symptoms: Comma-separated matched symptom names.
        recommended_dept: Recommended department ID.
        confidence: Confidence score of the recommendation.
        viewed_route: Whether user viewed navigation route.
    """
    
    def __init__(
        self, 
        record_id: Optional[int] = None,
        create_time: Optional[datetime] = None,
        input_text: str = "",
        matched_symptoms: str = "",
        recommended_dept: Optional[int] = None,
        confidence: float = 0.0,
        viewed_route: bool = False
    ) -> None:
        """Initialize a TriageRecord instance.
        
        Args:
            record_id: Unique identifier.
            create_time: Creation timestamp.
            input_text: User input text.
            matched_symptoms: Matched symptoms string.
            recommended_dept: Department ID.
            confidence: Confidence score.
            viewed_route: Whether route was viewed.
        """
        self.record_id = record_id
        self.create_time = create_time or datetime.now()
        self.input_text = input_text[:MAX_INPUT_LENGTH]
        self.matched_symptoms = matched_symptoms
        self.recommended_dept = recommended_dept
        self.confidence = max(0.0, min(confidence, 1.0))
        self.viewed_route = viewed_route
        
        logger.debug("TriageRecord created at %s", self.create_time)
    
    @property
    def symptom_list(self) -> List[str]:
        """Get list of matched symptoms.
        
        Returns:
            List of symptom name strings.
        """
        if not self.matched_symptoms:
            return []
        return [
            s.strip() for s in self.matched_symptoms.split(',') 
            if s.strip()
        ]
    
    @symptom_list.setter
    def symptom_list(self, symptoms: List[str]) -> None:
        """Set matched symptoms from list.
        
        Args:
            symptoms: List of symptom name strings.
        """
        self.matched_symptoms = ','.join(symptoms)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "TriageRecord":
        """Create TriageRecord instance from dictionary.
        
        Args:
            data: Dictionary with record data.
        
        Returns:
            TriageRecord instance.
        """
        # Parse create_time
        create_time = None
        if 'create_time' in data and data['create_time']:
            try:
                create_time = datetime.fromisoformat(
                    str(data['create_time']).replace('Z', '+00:00')
                )
            except ValueError:
                create_time = datetime.now()
        
        return cls(
            record_id=data.get('record_id'),
            create_time=create_time,
            input_text=data.get('input_text', ''),
            matched_symptoms=data.get('matched_symptoms', ''),
            recommended_dept=data.get('recommended_dept'),
            confidence=data.get('confidence', 0.0),
            viewed_route=bool(data.get('viewed_route', False)),
        )
    
    def to_dict(self) -> Dict:
        """Convert TriageRecord instance to dictionary.
        
        Returns:
            Dictionary representation of the record.
        """
        return {
            'record_id': self.record_id,
            'create_time': self.create_time.isoformat(),
            'input_text': self.input_text,
            'matched_symptoms': self.matched_symptoms,
            'recommended_dept': self.recommended_dept,
            'confidence': self.confidence,
            'viewed_route': self.viewed_route,
        }
    
    def validate(self) -> tuple[bool, str]:
        """Validate record data.
        
        Returns:
            Tuple of (is_valid, error_message).
        """
        if not self.input_text:
            return False, "输入文本不能为空"
        
        if len(self.input_text) > MAX_INPUT_LENGTH:
            return False, f"输入文本不能超过{MAX_INPUT_LENGTH}个字符"
        
        if self.confidence < 0 or self.confidence > 1:
            return False, "置信度必须在0-1之间"
        
        return True, ""
    
    def __repr__(self) -> str:
        """String representation of TriageRecord."""
        return (
            f"TriageRecord(id={self.record_id}, "
            f"time={self.create_time}, "
            f"confidence={self.confidence:.2f})"
        )
