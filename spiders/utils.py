# encoding=utf-8
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
def get_update_time():
    update_date = datetime.now()
    return update_date.strftime(DATE_FORMAT)