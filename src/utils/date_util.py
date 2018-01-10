from datetime import datetime

def to_date(provider):
    return datetime.strptime(provider, '%Y-%m-%dT%H:%M:%S+01:00').date()