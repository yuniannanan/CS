#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Symptom data model for Intelligent Medical Guide System.

This module defines the Symptom class for representing and
manipulating symptom data.

Attributes:
    CATEGORIES: Valid symptom categories.
"""

from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)

CATEGORIES = [
    "neurological", "respiratory", "gastrointestinal",
    "cardiovascular", "musculoskeletal", "dermatological",
    "systemic", "other"
]


class Symptom:
    """Data model class for medical symptoms.
    
    This class represents a medical symptom with its attributes
    and provides methods for data access and manipulation.
    
    Attributes:
        symptom_id: Unique identifier for the symptom.
        symptom_name: Name of the symptom.
        category: Category of the symptom.
        synonyms: Comma-separated synonym strings.
        base_weight: Base weight for reasoning calculations.
    """
    
    def __init__(
        self, 
        symptom_id: Optional[int] = None,
        symptom_name: str = "",
        category: str = "other",
        synonyms: str = "",
        base_weight: float = 1.0
    ) -> None:
        """Initialize a Symptom instance.
        
        Args:
            symptom_id: Unique identifier.
            symptom_name: Name of the symptom.
            category: Category of the symptom.
            synonyms: Comma-separated synonyms.
            base_weight: Base weight for reasoning.
        """
        self.symptom_id = symptom_id
        self.symptom_name = symptom_name
        self.category = category if category in CATEGORIES else "other"
        self.synonyms = synonyms
        self.base_weight = max(0.1, base_weight)
        
        logger.debug("Symptom created: %s", self.symptom_name)
    
    @property
    def synonym_list(self) -> List[str]:
        """Get list of synonyms.
        
        Returns:
            List of synonym strings.
        """
        if not self.synonyms:
            return []
        return [s.strip() for s in self.synonyms.split(',') if s.strip()]
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Symptom":
        """Create Symptom instance from dictionary.
        
        Args:
            data: Dictionary with symptom data.
        
        Returns:
            Symptom instance.
        """
        return cls(
            symptom_id=data.get('symptom_id'),
            symptom_name=data.get('symptom_name', ''),
            category=data.get('category', 'other'),
            synonyms=data.get('synonyms', ''),
            base_weight=data.get('base_weight', 1.0),
        )
    
    def to_dict(self) -> Dict:
        """Convert Symptom instance to dictionary.
        
        Returns:
            Dictionary representation of the symptom.
        """
        return {
            'symptom_id': self.symptom_id,
            'symptom_name': self.symptom_name,
            'category': self.category,
            'synonyms': self.synonyms,
            'base_weight': self.base_weight,
        }
    
    def validate(self) -> tuple[bool, str]:
        """Validate symptom data.
        
        Returns:
            Tuple of (is_valid, error_message).
        """
        if not self.symptom_name:
            return False, "症状名称不能为空"
        
        if len(self.symptom_name) > 50:
            return False, "症状名称不能超过50个字符"
        
        if self.category not in CATEGORIES:
            return False, f"无效的症状分类: {self.category}"
        
        if self.base_weight < 0:
            return False, "基础权重不能为负数"
        
        return True, ""
    
    def __repr__(self) -> str:
        """String representation of Symptom."""
        return (
            f"Symptom(id={self.symptom_id}, "
            f"name='{self.symptom_name}', "
            f"category='{self.category}')"
        )
