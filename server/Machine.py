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
        if file_modified and time.time() - self.file_update_time > self.interval:
            return True
        return False

    def save(self, json_obj):
        with open(self.filename, 'w') as f:
            json.dump(json_obj, f)
            self.last_update_time = time.time()
            f.close()

CLOTH_EMPTY = 0
CLOTH_WET = 1
CLOTH_DRY = 2
class Machine:
    JSON_FILENAME = "machine_status.json"
    AUTO_SAVING_INTERVAL = 10 #sec
    def __init__(self, capacity):
        self.saver = File_Saver(type(self).JSON_FILENAME, type(self).AUTO_SAVING_INTERVAL)
        status_json = self.saver.load()
        if status_json is not False:
            self.status = {
                    "index": status_json["index"],
                    "clothes": status_json["clothes"]}
        else:
            self.status = {
                    "index":0,
                    "clothes":[{
                        "key":  0,
                        "status":CLOTH_EMPTY,
                        "time": i,
                        "batch":int(i/10)} for i in range(capacity)]}
        self.file_modified = False

    def get_status(self, key):
        batches = []
        key_status = []
        for cloth in self.status["clothes"]:
            if cloth["key"] == key:
                batches.append(cloth)
        if len(batches) == 0:
            return False
        batches.sort(key=lambda d:d["batch"])

        start = 0
        end = 0
        while end < len(batches):
            while end < len(batches) and batches[end]["batch"] == batches[start]["batch"]:
                end += 1
            num_dry = 0
            for cloth in batches[start:end]:
                if cloth["status"] == CLOTH_DRY:
                    num_dry += 1
            earlist_cloth = min(batches[start:end], key=lambda d:d["time"])
            new_status = {
                "batch":batches[start]["batch"],
                "status":num_dry/(end-start),
                "time":earlist_cloth["time"],
                "num":end-start
            }
            key_status.append(new_status)
            start = end
        return key_status
    
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

if __name__ == "__main__":
    machine = Machine(40)
    machine.get_status(0)
