#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Database management module for SQLite operations.

This module provides a unified interface for database operations
including connection management, query execution, and transaction handling.

Attributes:
    DEFAULT_DB_PATH: Default path to the SQLite database file.
"""

import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging
import configparser

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = "guide_system.db"


class DatabaseManager:
    """Database manager for SQLite operations.
    
    This class provides methods for executing queries, managing
    connections, and handling transactions.
    
    Attributes:
        db_path: Path to the SQLite database file.
        connection: SQLite connection object.
    """
    
    def __init__(self, config_path: str = "config.ini") -> None:
        """Initialize the DatabaseManager with configuration.
        
        Args:
            config_path: Path to the configuration file.
        """
        self.db_path = self._get_db_path(config_path)
        self.connection: Optional[sqlite3.Connection] = None
        
        # Ensure database directory exists
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("DatabaseManager initialized with path: %s", self.db_path)
    
    def _get_db_path(self, config_path: str) -> str:
        """Get database path from configuration file.
        
        Args:
            config_path: Path to the configuration file.
        
        Returns:
            Database path string.
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.warning(
                "Config file not found: %s, using default path",
                config_path
            )
            return DEFAULT_DB_PATH
        
        config = configparser.ConfigParser()
        config.read(str(config_file), encoding="utf-8")
        
        db_path = config.get(
            "Database", "db_path", fallback=DEFAULT_DB_PATH
        )
        
        # 相对路径相对于配置文件所在目录解析
        db_file = Path(db_path)
        if not db_file.is_absolute():
            db_file = config_file.parent / db_path
        
        return str(db_file)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get or create a database connection.
        
        Returns:
            SQLite connection object.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False  # 允许跨线程（Flask 多线程安全）
            )
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
            logger.debug("Database connection established")
        
        return self.connection
    
    def execute_query(
        self, 
        query: str, 
        params: Tuple = ()
    ) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dicts.
        
        Args:
            query: SQL query string.
            params: Query parameters tuple.
        
        Returns:
            List of dictionaries representing rows.
        """
        try:
            conn = self.get_connection()
            cursor = conn.execute(query, params)
            
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            
            logger.debug(
                "Query executed successfully, returned %d rows",
                len(result)
            )
            
            return result
            
        except sqlite3.Error as e:
            logger.error("Query execution failed: %s", str(e))
            logger.error("Query: %s", query)
            return []
    
    def execute_update(
        self, 
        query: str, 
        params: Tuple = ()
    ) -> int:
        """Execute an INSERT/UPDATE/DELETE query.
        
        Args:
            query: SQL query string.
            params: Query parameters tuple.
        
        Returns:
            Number of affected rows.
        """
        try:
            conn = self.get_connection()
            cursor = conn.execute(query, params)
            conn.commit()
            
            affected_rows = cursor.rowcount
            
            logger.debug(
                "Update executed successfully, affected %d rows",
                affected_rows
            )
            
            return affected_rows
            
        except sqlite3.Error as e:
            logger.error("Update execution failed: %s", str(e))
            logger.error("Query: %s", query)
            if self.connection:
                self.connection.rollback()
            return 0
    
    def execute_insert(
        self, 
        query: str, 
        params: Tuple = ()
    ) -> Optional[int]:
        """Execute an INSERT query and return the last row ID.
        
        Args:
            query: SQL INSERT query string.
            params: Query parameters tuple.
        
        Returns:
            Last inserted row ID, or None if failed.
        """
        try:
            conn = self.get_connection()
            cursor = conn.execute(query, params)
            conn.commit()
            
            last_id = cursor.lastrowid
            
            logger.debug(
                "Insert executed successfully, last ID: %d",
                last_id
            )
            
            return last_id
            
        except sqlite3.Error as e:
            logger.error("Insert execution failed: %s", str(e))
            logger.error("Query: %s", query)
            if self.connection:
                self.connection.rollback()
            return None
    
    def execute_many(
        self, 
        query: str, 
        params_list: List[Tuple]
    ) -> int:
        """Execute a query with multiple parameter sets.
        
        Args:
            query: SQL query string.
            params_list: List of parameter tuples.
        
        Returns:
            Number of affected rows.
        """
        try:
            conn = self.get_connection()
            cursor = conn.executemany(query, params_list)
            conn.commit()
            
            affected_rows = cursor.rowcount
            
            logger.debug(
                "Batch execution completed, affected %d rows",
                affected_rows
            )
            
            return affected_rows
            
        except sqlite3.Error as e:
            logger.error("Batch execution failed: %s", str(e))
            logger.error("Query: %s", query)
            if self.connection:
                self.connection.rollback()
            return 0
    
    def begin_transaction(self) -> bool:
        """Begin a database transaction.
        
        Returns:
            True if transaction started successfully.
        """
        try:
            conn = self.get_connection()
            conn.execute("BEGIN TRANSACTION")
            logger.debug("Transaction started")
            return True
        except sqlite3.Error as e:
            logger.error("Failed to begin transaction: %s", str(e))
            return False
    
    def commit_transaction(self) -> bool:
        """Commit the current transaction.
        
        Returns:
            True if commit successful.
        """
        try:
            if self.connection:
                self.connection.commit()
                logger.debug("Transaction committed")
            return True
        except sqlite3.Error as e:
            logger.error("Failed to commit transaction: %s", str(e))
            return False
    
    def rollback_transaction(self) -> bool:
        """Rollback the current transaction.
        
        Returns:
            True if rollback successful.
        """
        try:
            if self.connection:
                self.connection.rollback()
                logger.debug("Transaction rolled back")
            return True
        except sqlite3.Error as e:
            logger.error("Failed to rollback transaction: %s", str(e))
            return False
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.debug("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
