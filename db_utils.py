# db_utils.py
# MySQL CRUD layer mirroring excel_utils.py signatures
import json
import os
from datetime import datetime
from typing import List, Any, Tuple

import mysql.connector
from mysql.connector import errorcode

from constants import COLUMNS

# Default DB config (XAMPP defaults)
DEFAULT_DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "Hakdog123!",
    "database": "dietary_mgmt",
}


class DatabaseError(Exception):
    pass


def _load_db_config() -> dict:
    # Start with default config
    cfg = dict(DEFAULT_DB_CONFIG)
    
    # Try project-level settings.json
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(base_dir, 'settings.json')
        
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Check for db_config in settings
                if isinstance(data, dict) and 'db_config' in data and isinstance(data['db_config'], dict):
                    cfg.update(data['db_config'])
                # For backward compatibility with old settings format
                elif isinstance(data, dict) and 'db' in data and isinstance(data['db'], dict):
                    cfg.update(data['db'])
    except Exception as e:
        print(f"Warning: Could not load settings from settings.json: {e}")
    
    # Environment overrides
    cfg['host'] = os.environ.get('DMS_DB_HOST', cfg['host'])
    cfg['port'] = int(os.environ.get('DMS_DB_PORT', cfg['port']))
    cfg['user'] = os.environ.get('DMS_DB_USER', cfg['user'])
    cfg['password'] = os.environ.get('DMS_DB_PASSWORD', cfg['password'])
    cfg['database'] = os.environ.get('DMS_DB_NAME', cfg['database'])
    
    return cfg


def _get_connection(database_required=True):
    cfg = _load_db_config()
    try:
        conn = mysql.connector.connect(
            host=cfg['host'],
            port=cfg['port'],
            user=cfg['user'],
            password=cfg['password'],
            database=(cfg['database'] if database_required else None),
            autocommit=False,
            use_pure=True,
        )
        return conn
    except mysql.connector.Error as err:
        raise DatabaseError(str(err))


def init_db():
    """Check connectivity and ensure `patients` table exists.
    Assumes you've run schema_dietary_mgmt.sql. If not, attempts to create the table.
    """
    cfg = _load_db_config()
    # Ensure database exists
    try:
        conn = _get_connection(database_required=False)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{cfg['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise DatabaseError(f"Failed to ensure database: {e}")

    # Ensure table exists
    create_sql = (
        """
        CREATE TABLE IF NOT EXISTS `patients` (
          `Patient ID` INT NOT NULL AUTO_INCREMENT,
          `Patient Name` VARCHAR(255) NOT NULL,
          `Sex` ENUM('Male','Female') NULL,
          `Age` INT NULL,
          `Age Group` VARCHAR(64) NULL,
          `Ward Admission Date` DATE NULL,
          `Date of Visit` DATE NULL,
          `Diagnosis` VARCHAR(512) NULL,
          `With Nutrition Support` ENUM('Yes','No') NULL,
          `Ward` VARCHAR(64) NULL,
          `Subspecialty` VARCHAR(64) NULL,
          `Height` DECIMAL(5,2) NULL,
          `Weight` DECIMAL(5,2) NULL,
          `Type Of Visit` VARCHAR(64) NULL,
          `Purpose of Visit` VARCHAR(64) NULL,
          `WFL Z-Score` VARCHAR(32) NULL,
          `BMI Percentile` VARCHAR(32) NULL,
          `Nutritional Status` VARCHAR(32) NULL,
          `Bowel Movement` VARCHAR(64) NULL,
          `Emesis` VARCHAR(32) NULL,
          `Abdominal Distention` VARCHAR(32) NULL,
          `Biochemical Parameters` VARCHAR(128) NULL,
          `RND Dietary Management` VARCHAR(128) NULL,
          `Diet Prescriptions(Current)` VARCHAR(512) NULL,
          `With Documents` ENUM('Yes','No') NULL,
          `Given NCP` ENUM('Yes','No') NULL,
          `Encoded By` VARCHAR(64) NULL,
          `Encoded Date` DATE NULL,
          `Last Updated` DATETIME NULL,
          PRIMARY KEY (`Patient ID`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
    )
    try:
        conn = _get_connection(database_required=True)
        cur = conn.cursor()
        cur.execute(create_sql)
        conn.commit()
    except Exception as e:
        raise DatabaseError(f"Failed to ensure table: {e}")
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


def _normalize_date(value: Any):
    # Accept 'YYYY-MM-DD' strings or empty -> None
    if not value or str(value).strip() == '':
        return None
    s = str(value)
    # If includes time, take only date
    if 'T' in s or ' ' in s:
        s = s.split('T')[0].split(' ')[0]
    return s


def load_patients() -> List[Tuple[Any, ...]]:
    cols = ', '.join([f"`{c}`" for c in COLUMNS])
    sql = f"SELECT {cols} FROM `patients` ORDER BY `Patient ID` ASC"
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        # Convert dates to string format YYYY-MM-DD to match Excel UI expectation
        out = []
        for row in rows:
            row = list(row)
            for idx, col in enumerate(COLUMNS):
                if col in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
                    v = row[idx]
                    if v is None:
                        row[idx] = ''
                    else:
                        row[idx] = v.strftime('%Y-%m-%d')
                elif col == 'Last Updated':
                    v = row[idx]
                    if v is None:
                        row[idx] = ''
                    else:
                        # Keep the same format the UI uses
                        row[idx] = v.strftime('%Y-%m-%d %H:%M:%S')
            out.append(tuple(row))
        return out
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def add_patient(item: List[Any]):
    # item matches COLUMNS order
    # Convert date strings to DATE, Last Updated to DATETIME
    values = []
    for idx, col in enumerate(COLUMNS):
        v = item[idx] if idx < len(item) else None
        if col in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
            v = _normalize_date(v)
        elif col == 'Last Updated':
            if not v:
                v = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values.append(v)

    cols_sql = ', '.join([f"`{c}`" for c in COLUMNS])
    placeholders = ', '.join(['%s'] * len(COLUMNS))
    sql = f"INSERT INTO `patients` ({cols_sql}) VALUES ({placeholders})"

    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, tuple(values))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise DatabaseError(str(err))
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def update_patient(item_id: Any, updated_item: List[Any]):
    set_parts = []
    params = []
    for idx, col in enumerate(COLUMNS):
        # Always set based on updated_item order
        set_parts.append(f"`{col}` = %s")
        v = updated_item[idx] if idx < len(updated_item) else None
        if col in ['Ward Admission Date', 'Date of Visit', 'Encoded Date']:
            v = _normalize_date(v)
        params.append(v)
    params.append(item_id)

    sql = f"UPDATE `patients` SET {', '.join(set_parts)} WHERE `Patient ID` = %s"

    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise DatabaseError(str(err))
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def delete_patient(item_id: Any):
    sql = "DELETE FROM `patients` WHERE `Patient ID` = %s"
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, (item_id,))
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        raise DatabaseError(str(err))
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()
