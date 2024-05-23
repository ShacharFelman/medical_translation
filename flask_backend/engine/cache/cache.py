from datetime import datetime, timedelta
from typing import Optional

class Cache:
    def __init__(self, timeout_minutes):
        self.data = {}
        self._timeout_minutes = timeout_minutes 

    def add(self,key,data:dict,timeout_minutes:Optional[int]):
        expiration_time = datetime.now() + timedelta(minutes=self._timeout_minutes if self._timeout_minutes else timeout_minutes )
        self.data[key] = {
            'data': data,
            'expiration_time': expiration_time
        }

    def get(self,key):
        if key in self.data:
            return self.data[key]['data']

    def remove(self, key):
        if key in self.data:
            del self.data[key]

    def remove_expired_entries(self):
        current_time = datetime.now()
        expired_keys = [key for key, value in self.data.items() if value['expiration_time'] < current_time]
        for key in expired_keys:
            del self.data[key]    
        return self