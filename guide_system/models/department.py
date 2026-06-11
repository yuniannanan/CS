#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Department data model for Intelligent Medical Guide System.

This module defines the Department class for representing and
manipulating department data.

Attributes:
    MIN_FLOOR: Minimum valid floor number.
    MAX_FLOOR: Maximum valid floor number.
"""

from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

MIN_FLOOR = 1
MAX_FLOOR = 50


class Department:
    """Data model class for hospital departments.
    
    This class represents a hospital department with its attributes
    and provides methods for data access and manipulation.
    
    Attributes:
        dept_id: Unique identifier for the department.
        dept_name: Name of the department.
        function_desc: Description of department function.
        floor: Floor number where department is located.
        location_desc: Detailed location description.
    """
    
    def __init__(
        self, 
        dept_id: Optional[int] = None,
        dept_name: str = "",
        function_desc: str = "",
        floor: int = 1,
        location_desc: str = ""
    ) -> None:
        """Initialize a Department instance.
        
        Args:
            dept_id: Unique identifier.
            dept_name: Name of the department.
            function_desc: Function description.
            floor: Floor number.
            location_desc: Location description.
        """
        self.dept_id = dept_id
        self.dept_name = dept_name
        self.function_desc = function_desc
        self.floor = max(MIN_FLOOR, min(floor, MAX_FLOOR))
        self.location_desc = location_desc
        
        logger.debug("Department created: %s", self.dept_name)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Department":
        """Create Department instance from dictionary.
        
        Args:
            data: Dictionary with department data.
        
        Returns:
            Department instance.
        """
        return cls(
            dept_id=data.get('dept_id'),
            dept_name=data.get('dept_name', ''),
            function_desc=data.get('function_desc', ''),
            floor=data.get('floor', 1),
            location_desc=data.get('location_desc', ''),
        )
    
    def to_dict(self) -> Dict:
        """Convert Department instance to dictionary.
        
        Returns:
            Dictionary representation of the department.
        """
        return {
            'dept_id': self.dept_id,
            'dept_name': self.dept_name,
            'function_desc': self.function_desc,
            'floor': self.floor,
            'location_desc': self.location_desc,
        }
    
    def validate(self) -> tuple[bool, str]:
        """Validate department data.
        
        Returns:
            Tuple of (is_valid, error_message).
        """
        if not self.dept_name:
            return False, "科室名称不能为空"
        
        if len(self.dept_name) > 50:
            return False, "科室名称不能超过50个字符"
        
        if self.floor < MIN_FLOOR or self.floor > MAX_FLOOR:
            return False, f"楼层必须在{MIN_FLOOR}-{MAX_FLOOR}之间"
        
        return True, ""
    
    def get_full_location(self) -> str:
        """Get full location string.
        
        Returns:
            Full location description with floor info.
        """
        return f"{self.floor}楼 - {self.location_desc}"
    
    def __repr__(self) -> str:
        """String representation of Department."""
        return (
            f"Department(id={self.dept_id}, "
            f"name='{self.dept_name}', "
            f"floor={self.floor})"
        )
