# helpers.py
from datetime import datetime

def format_date(year, month, day):
    if year and month and day:
        return f"{year}-{month}-{day}"
    return ''

def parse_date(date_str):
    try:
        y, m, d = date_str.split('-')
        return y, m, d
    except Exception:
        return '', '', ''
