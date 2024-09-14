# date.py

from datetime import datetime, timedelta

def get_date_str(delta: int = 0) -> str:
    today = datetime.today()
    date = today + timedelta(days=delta)
    return date.strftime('%Y-%m-%d')
