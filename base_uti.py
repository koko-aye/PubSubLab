import threading
from datetime import datetime
from zoneinfo import ZoneInfo

def start_subscription_thread(fun, params, stop_event):
    t = threading.Thread(
            target=fun,
            args=(params,),
            daemon=True
        )
    t.start()
    print(f"{fun.__name__} thread started. Params: {params}")
    stop_event.set()
    t.join()
    print(f"{fun.__name__} stopped.")

def get_json_value(payload, key, default=None):
    if payload is None:
        return None
    elif isinstance(payload, dict):
        return payload.get(key, default) 
    else:
        return payload
    
from datetime import datetime
from zoneinfo import ZoneInfo

def get_singapore_datetime():
    return datetime.now(ZoneInfo("Asia/Singapore"))