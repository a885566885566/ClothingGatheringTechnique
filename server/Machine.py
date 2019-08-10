import json
import time

class File_Saver:
    def __init__(self, filename, save_interval):
        self.interval = save_interval
        self.filename = filename
        self.file_update_time = time.time()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                old_status = json.load(f)
                f.close()
                return old_status
        except FileNotFoundError:
             print("No history status file founded")
             return False
    
    def file_save_check(self, file_modified):
        if file_modified and time.time() - self.last_update_time > AUTO_SAVING_INTERVAL:
            return True
        return False

    def save(self, json_obj):
        with open(self.filename, 'w') as f:
            json.dump(json_obj, f)
            self.last_update_time = time.time()
            f.close()

class Machine:
    JSON_FILENAME = "machine_status.json"
    AUTO_SAVING_INTERVAL = 10 #sec
    def __init__(self, capacity):
        self.saver = File_Saver(type(self).JSON_FILENAME, type(self).AUTO_SAVING_INTERVAL)
        self.status = self.saver.load()
        if self.status is not False:
            self.status = {
                    "index":0,
                    "capacity":capacity,
                    "clothes":[]}
        self.file_modified = False
    
    def update(self):
        if self.saver.file_save_check(self.file_modified):
            self.saver.save(self.status)
            self.file_modified = False

    def close(self):
        self.saver.save(self.status)
"""
The detail working command of events, handling motor movements.
Param:
    lock: If set to True, indicating that this task is not interruptable.
"""
class Task:
    ENDING_CHAR = ";"
    def __init__(self, m="A",p=0, lock=False):
        self.working_lock = lock
        self.mode = m
        self.para = p

    def encode(self):
        msg = self.mode + str(self.para) + ENDING_CHAR

