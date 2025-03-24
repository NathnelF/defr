from datetime import datetime

def valid_date(date):
    formats = ["%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y", "%m,%d,%Y", "%m %d %Y"]
    for format in formats:
        try:
            date = datetime.strptime(date, format)
            return True
        except ValueError:
            continue
    
    return False