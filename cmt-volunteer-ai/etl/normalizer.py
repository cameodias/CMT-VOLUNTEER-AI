from dateutil.parser import parse

def normalize_name(name):
    return " ".join(word.capitalize() for word in name.strip().split())

def normalize_date(date_str):
    return parse(date_str).strftime("%Y-%m-%d") if date_str else None
