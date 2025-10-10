# backup_utils.py
from __future__ import annotations
from datetime import datetime
import os
from typing import Optional

from constants import COLUMNS
import exporter
import db_utils


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def _escape_sql_value(v):
    if v is None or v == "":
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    # escape single quotes
    s = s.replace("'", "''")
    return f"'{s}'"


def backup_to_sql(output_path: str) -> str:
    """Create a portable SQL file containing schema + data for `patients`.

    Returns the written path.
    """
    conn = db_utils._get_connection()  # use internal connector for consistency
    try:
        cur = conn.cursor()
        # Determine current DB and table schema
        cur.execute("SELECT DATABASE()")
        db_name = cur.fetchone()[0]

        cur.execute("SHOW CREATE TABLE `patients`")
        _tbl, create_sql = cur.fetchone()

        # Fetch data
        cols_quoted = ", ".join([f"`{c}`" for c in COLUMNS])
        cur.execute(f"SELECT {cols_quoted} FROM `patients` ORDER BY `Patient ID` ASC")
        rows = cur.fetchall()

        # Write dump
        with open(output_path, "w", encoding="utf-8") as f:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write("-- Dietary Management System backup\n")
            f.write(f"-- Generated: {ts}\n\n")
            f.write("SET NAMES utf8mb4;\n")
            f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")
            if db_name:
                f.write(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n")
                f.write(f"USE `{db_name}`;\n\n")
            f.write("-- Table schema\n")
            f.write(f"{create_sql};\n\n")

            f.write("-- Data\n")
            if rows:
                # Insert in batches to keep lines reasonable
                batch_size = 500
                for i in range(0, len(rows), batch_size):
                    batch = rows[i:i+batch_size]
                    values_sql_parts = []
                    for row in batch:
                        vals = []
                        for idx, col in enumerate(COLUMNS):
                            v = row[idx] if idx < len(row) else None
                            # Dates and datetimes should be stringified in ISO
                            if v is not None:
                                if hasattr(v, 'strftime'):
                                    # Date/datetime
                                    fmt = '%Y-%m-%d %H:%M:%S' if getattr(v, 'hour', None) is not None else '%Y-%m-%d'
                                    v = v.strftime(fmt)
                            vals.append(_escape_sql_value(v))
                        values_sql_parts.append("(" + ", ".join(vals) + ")")
                    insert_sql = f"INSERT INTO `patients` ({cols_quoted}) VALUES \n  " + ",\n  ".join(values_sql_parts) + ";\n"
                    f.write(insert_sql)
            f.write("\nSET FOREIGN_KEY_CHECKS=1;\n")
        return output_path
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def backup_to_excel(output_path: str) -> str:
    """Create an Excel export using existing exporter."""
    exporter.export_db_to_excel(output_path)
    return output_path


def backup_all(backup_dir: str, with_excel: bool = True) -> dict:
    """Create timestamped backups in a folder. Returns dict with written paths."""
    _ensure_dir(backup_dir)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {}
    sql_path = os.path.join(backup_dir, f"patients_{ts}.sql")
    results['sql'] = backup_to_sql(sql_path)
    if with_excel:
        xlsx_path = os.path.join(backup_dir, f"patients_{ts}.xlsx")
        results['excel'] = backup_to_excel(xlsx_path)
    return results
