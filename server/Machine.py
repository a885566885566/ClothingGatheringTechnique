import json
import time

class Machine:
    JSON_FILENAME = "machine_status.json"
    AUTO_SAVING_INTERVAL = 10 #sec
    def __init__(self, capacity):
        self.status = {}
        if not self.load():
            self.status = {
                "index"=0,
                "capacity"=capacity,
                "clothes"=[]}
        self.file_update_time = time.time()
        self.file_modified = False

    def load(self):
        try:
            with open(JSON_FILENAME, 'r') as f:
                old_status = json.load(f)
                self.status = old_status
                f.close()
                return True
         except FileNotFoundError:
             print("No history status file founded")
             return False
    
    def file_save_check(self):
        if file_modified and time.time() - self.last_update_time > AUTO_SAVING_INTERVAL:
            self.save()
            self.last_update_time = time.time()
            file_modified = False

    def save(self):
        with open(JSON_FILENAME, 'w') as f:
            json.dump(self.status, f)
            f.close()

    def close(self):
        self.save()
"
The detail working command of events, handling motor movements.
Param:
    lock: If set to True, indicating that this task is not interruptable.
"
class Task:
    ENDING_CHAR = ";"
    def __init__(self, lock=False):
        self.working_lock = lock
        self.mode = ""
        self.para = 0

    def encode(self):
        msg = self.mode + str(self.para) + ENDING_CHAR

