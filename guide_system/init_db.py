#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Database initialization script for Intelligent Medical Guide System.

This script creates the SQLite database and populates it with initial data
for symptoms, departments, rules, and floor information.

Attributes:
    DATABASE_PATH: Path to the SQLite database file.
"""

import sqlite3
import json
import os
from pathlib import Path

# Default database path
DATABASE_PATH = "guide_system.db"

# Sample data for initialization
SAMPLE_SYMPTOMS = [
    (1, "头痛", "neurological", "头疼,头部疼痛,脑部不适", 1.0),
    (2, "发热", "systemic", "发烧,体温升高,高热", 1.2),
    (3, "咳嗽", "respiratory", "咳,咳嗽不止,干咳", 1.0),
    (4, "咽痛", "respiratory", "喉咙痛,咽喉疼痛,嗓子疼", 0.9),
    (5, "胸闷", "cardiovascular", "胸部闷痛,胸口不适,呼吸困难", 1.3),
    (6, "腹痛", "gastrointestinal", "肚子疼,腹部疼痛,肠胃不适", 1.0),
    (7, "恶心", "gastrointestinal", "想吐,反胃,呕吐感", 0.8),
    (8, "腹泻", "gastrointestinal", "拉肚子,腹痛腹泻,稀便", 1.0),
    (9, "关节疼痛", "musculoskeletal", "关节疼,关节肿痛,关节炎", 1.0),
    (10, "皮疹", "dermatological", "皮肤红疹,皮肤瘙痒,皮炎", 0.9),
    (11, "头晕", "neurological", "眩晕,头昏,平衡失调", 1.1),
    (12, "心悸", "cardiovascular", "心跳加快,心慌,心律不齐", 1.2),
    (13, "乏力", "systemic", "疲劳,疲倦,无力", 0.7),
    (14, "食欲不振", "gastrointestinal", "厌食,胃口差,消化不良", 0.8),
    (15, "体重下降", "systemic", "消瘦,体重减轻,莫名消瘦", 1.1),
]

SAMPLE_DEPARTMENTS = [
    (1, "神经内科", "诊治神经系统疾病", 3, "3楼东侧走廊,神经内科门诊区"),
    (2, "呼吸内科", "诊治呼吸系统疾病", 4, "4楼南侧,呼吸内科诊区"),
    (3, "消化内科", "诊治消化系统疾病", 4, "4楼北侧,消化内科诊区"),
    (4, "心血管内科", "诊治心血管疾病", 3, "3楼西侧,心血管内科诊区"),
    (5, "骨科", "诊治骨骼肌肉系统疾病", 2, "2楼东侧,骨科诊区"),
    (6, "皮肤科", "诊治皮肤疾病", 5, "5楼南侧,皮肤科诊区"),
    (7, "普通内科", "综合内科常见病诊治", 1, "1楼东侧,综合门诊区"),
    (8, "急诊科", "急危重症救治", 1, "1楼北侧,急诊中心"),
]

SAMPLE_RULES = [
    (1, 1, 1, 1.5, "IF 头痛 THEN 神经内科"),
    (2, 11, 1, 1.2, "IF 头晕 THEN 神经内科"),
    (3, 3, 2, 1.4, "IF 咳嗽 THEN 呼吸内科"),
    (4, 4, 2, 1.3, "IF 咽痛 THEN 呼吸内科"),
    (5, 6, 3, 1.4, "IF 腹痛 THEN 消化内科"),
    (6, 7, 3, 1.2, "IF 恶心 THEN 消化内科"),
    (7, 8, 3, 1.3, "IF 腹泻 THEN 消化内科"),
    (8, 14, 3, 0.9, "IF 食欲不振 THEN 消化内科"),
    (9, 5, 4, 1.5, "IF 胸闷 THEN 心血管内科"),
    (10, 12, 4, 1.4, "IF 心悸 THEN 心血管内科"),
    (11, 9, 5, 1.5, "IF 关节疼痛 THEN 骨科"),
    (12, 10, 6, 1.5, "IF 皮疹 THEN 皮肤科"),
    (13, 2, 7, 1.0, "IF 发热 THEN 普通内科"),
    (14, 13, 7, 0.8, "IF 乏力 THEN 普通内科"),
    (15, 15, 7, 1.1, "IF 体重下降 THEN 普通内科"),
    (16, 1, 8, 0.8, "IF 剧烈头痛伴呕吐 THEN 急诊科"),
    (17, 5, 8, 1.0, "IF 胸闷伴大汗 THEN 急诊科"),
    (18, 2, 8, 0.9, "IF 高热不退 THEN 急诊科"),
]

SAMPLE_FLOORS = [
    (1, 1, "导诊台,挂号处,收费处,药房,急诊中心", "电梯1(主电梯),电梯2(扶梯),楼梯A(主楼梯),楼梯B(消防楼梯)", "从正门进入后直行50米到达导诊台"),
    (2, 2, "骨科诊区,外科诊区,检验科,超声科", "电梯1(主电梯),楼梯A(主楼梯)", "从1楼乘坐电梯1到2楼,向东步行100米"),
    (3, 3, "神经内科诊区,心血管内科诊区,脑电图室,心电图室", "电梯1(主电梯),楼梯A(主楼梯)", "从1楼乘坐电梯1到3楼,根据指示牌选择东西方向"),
    (4, 4, "呼吸内科诊区,消化内科诊区,内镜中心", "电梯1(主电梯),电梯2(扶梯)", "从1楼乘坐电梯1到4楼,南侧为呼吸内科,北侧为消化内科"),
    (5, 5, "皮肤科诊区,中医科诊区,康复医学科", "电梯1(主电梯),楼梯A(主楼梯)", "从1楼乘坐电梯1到5楼,向南步行50米"),
]


def create_database(db_path: str = DATABASE_PATH) -> None:
    """Create the SQLite database with all required tables.
    
    Args:
        db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create symptoms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptoms (
            symptom_id INTEGER PRIMARY KEY,
            symptom_name VARCHAR(50) NOT NULL,
            category VARCHAR(30) NOT NULL,
            synonyms VARCHAR(200),
            base_weight FLOAT DEFAULT 1.0
        )
    """)
    
    # Create departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            dept_id INTEGER PRIMARY KEY,
            dept_name VARCHAR(50) NOT NULL,
            function_desc VARCHAR(200),
            floor INTEGER NOT NULL,
            location_desc VARCHAR(200) NOT NULL
        )
    """)
    
    # Create rules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            rule_id INTEGER PRIMARY KEY,
            symptom_id INTEGER,
            dept_id INTEGER,
            rule_weight FLOAT DEFAULT 1.0,
            conditions VARCHAR(500),
            FOREIGN KEY (symptom_id) REFERENCES symptoms(symptom_id),
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        )
    """)
    
    # Create records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            input_text VARCHAR(500) NOT NULL,
            matched_symptoms VARCHAR(200),
            recommended_dept INTEGER,
            confidence FLOAT,
            viewed_route BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (recommended_dept) REFERENCES departments(dept_id)
        )
    """)
    
    # Create floors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS floors (
            floor_id INTEGER PRIMARY KEY,
            floor_number INTEGER NOT NULL,
            core_areas VARCHAR(200),
            elevator_stairs VARCHAR(200),
            guide_text VARCHAR(500)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database created successfully: {db_path}")


def populate_sample_data(db_path: str = DATABASE_PATH) -> None:
    """Populate the database with sample data.
    
    Args:
        db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM rules")
    cursor.execute("DELETE FROM records")
    cursor.execute("DELETE FROM symptoms")
    cursor.execute("DELETE FROM departments")
    cursor.execute("DELETE FROM floors")
    
    # Insert sample symptoms
    cursor.executemany(
        "INSERT INTO symptoms VALUES (?, ?, ?, ?, ?)",
        SAMPLE_SYMPTOMS
    )
    
    # Insert sample departments
    cursor.executemany(
        "INSERT INTO departments VALUES (?, ?, ?, ?, ?)",
        SAMPLE_DEPARTMENTS)
    
    # Insert sample rules
    cursor.executemany(
        "INSERT INTO rules VALUES (?, ?, ?, ?, ?)",
        SAMPLE_RULES
    )
    
    # Insert sample floors
    cursor.executemany(
        "INSERT INTO floors VALUES (?, ?, ?, ?, ?)",
        SAMPLE_FLOORS
    )
    
    conn.commit()
    conn.close()
    print("Sample data populated successfully")


def export_to_json(db_path: str = DATABASE_PATH) -> None:
    """Export database data to JSON files for backup and offline use.
    
    Args:
        db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create data directory if not exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Export symptoms
    cursor.execute("SELECT * FROM symptoms")
    symptoms = [dict(row) for row in cursor.fetchall()]
    with open(data_dir / "symptoms.json", "w", encoding="utf-8") as f:
        json.dump(symptoms, f, ensure_ascii=False, indent=2)
    
    # Export departments
    cursor.execute("SELECT * FROM departments")
    departments = [dict(row) for row in cursor.fetchall()]
    with open(data_dir / "departments.json", "w", encoding="utf-8") as f:
        json.dump(departments, f, ensure_ascii=False, indent=2)
    
    # Export rules
    cursor.execute("SELECT * FROM rules")
    rules = [dict(row) for row in cursor.fetchall()]
    with open(data_dir / "rules.json", "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)
    
    conn.close()
    print("Data exported to JSON files successfully")


def main() -> None:
    """Main function to initialize the database."""
    # Remove existing database if exists
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f"Removed existing database: {DATABASE_PATH}")
    
    # Create database and tables
    create_database()
    
    # Populate with sample data
    populate_sample_data()
    
    # Export to JSON files
    export_to_json()
    
    print("Database initialization completed successfully!")


if __name__ == "__main__":
    main()
