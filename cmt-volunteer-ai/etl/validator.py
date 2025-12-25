from dateutil.parser import parse

def is_valid_date(date_str):
    try:
        parse(date_str)
        return True
    except:
        return False

def validate_row(row):
    if not row.get("Name") or not row.get("City"):
        return False, "Missing Name or City"
    if row.get("Join_Date") and not is_valid_date(row["Join_Date"]):
        return False, "Invalid Join_Date"
    return True, None
def validate_row(row):
    # Minimal validation based on actual CSV
    if not row.get("members"):
        return False, "Missing member name"
    return True, None
