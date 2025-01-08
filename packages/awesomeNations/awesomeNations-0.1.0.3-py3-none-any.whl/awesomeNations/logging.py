from icecream import ic
from datetime import datetime

def configure(logging: bool = False):
    if logging:
        ic.enable()
    else:
        ic.disable()

    today = datetime.today()
    date = today.strftime('%H:%M:%S')
    ic.configureOutput(prefix=f'{date} --> ', includeContext=True)

def log(log):
    ic(log)