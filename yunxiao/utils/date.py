from datetime import datetime

def format_timestamp(ts: int) -> str:
    # Convert from microseconds to seconds by dividing by 1,000,000
    dt = datetime.fromtimestamp(ts / 1_000_000)
    return dt.strftime('%Y-%m-%d')
