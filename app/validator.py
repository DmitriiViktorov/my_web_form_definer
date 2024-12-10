import re
from datetime import datetime

def validate_date(date: str):
    formats = ["%d.%m.%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            datetime.strptime(date, fmt)
            return True
        except ValueError:
            continue
    return False



def validate_field(field_value):
    if validate_date(field_value):
        return "date"
    elif re.match(r"^[\\+ ]7 \d{3} \d{3} \d{2} \d{2}$", field_value):
        return "phone"
    elif re.match(r"^[^@]+@[^@]+\.[^@]+$", field_value):
        return "email"
    else:
        return "text"