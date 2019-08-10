import time
import Machine

"""Number larger has higher priority"""
PRIORITY_CLOTH_SORTING = 1
PRIORITY_CLOTH_GATHERING = 2
PRIORITY_CLOTH_DRYING = 3
"""
The parent class of Events
"""
class Event:

    def __init__(self, p):
        self.priority = p
        self.taskQueue = []

    def getTasks(self):
        for i in range(2*self.priority) :
            self.taskQueue.append({"mode":"A", "para":i, "lock":i<3})
        return self.taskQueue

    def print(self):
        print("Priority=" + str(self.priority) + ", Tasks=", end="")
        for t in self.taskQueue:
            if t["lock"]:
                print("*", end="")
            print(t["mode"]+str(t["para"])+", ", end="")
        print("")

class ClothSortingEvent(Event):
    def __init__(self):
        super().__init__(PRIORITY_CLOTH_SORTING)

class ClothDryingEvent(Event):
    def __init__(self):
        super().__init__(PRIORITY_CLOTH_DRYING)

class ClothGatheringEvent(Event):
    def __init__(self):
        super().__init__(PRIORITY_CLOTH_GATHERING)

"""
Dealing with event flow, that is, event inserting, deleting and running.
"""
class EventHandler:
    JSON_FILENAME = "event_status.json"
    AUTO_SAVING_INTERVAL = 10 #sec
    def __init__(self, machine):
        self.saver = Machine.File_Saver(type(self).JSON_FILENAME, type(self).AUTO_SAVING_INTERVAL)

        # Load events infomations from past data
        events_json = self.saver.load() 
        if events_json is not False:
            self.eventQueue = events_json['eventQueue']
            self.taskQueue = events_json['taskQueue']
        else:
            self.eventQueue = []
            self.taskQueue = []
        self.machine = machine

    """
    Add event according to the event's priority, and if the running event interrupting
    is needed, it will store the old event automatically, and reschedule it.
    """
    def addEvent(self, new_event):
        i = 0
        # If there are two event reach, the new one's priority is lower. So it will be sorted to backend.
        while i < len(self.eventQueue) and self.eventQueue[i].priority >= new_event.priority:
            i += 1
        
        old_event = None
        # If the new event trying to interrupt the running event, insert the task into proper location
        if i == 0:
            old_event = self.deleteRunningEvent()
            self.eventQueue.insert(i, new_event)
            for t in self.eventQueue[0].getTasks():
                self.taskQueue.append(t)

        else:
            self.eventQueue.insert(i, new_event)
        
        # The old event need to be stored(If it exists), this must run at the end,
        # otherwise, it might cause recursive logic error
        if old_event:
            self.addEvent(old_event)

        self.file_modified = True

    """
    Delete the running event. If the running event have some locked task that can not 
    be interrupted, it will keep them untill interruption can be performed. Finally, 
    push new event in the eventQueue.
    It will return the old event if it exist.
    """
    def deleteRunningEvent(self):
        if len(self.eventQueue) <= 0:
            return None
        # Check if the running task is interruptable
        task_i = 0
        print(self.taskQueue)
        while task_i < len(self.taskQueue) and self.taskQueue[task_i]["lock"]:
            task_i += 1
        
        # Delete all task that are interruptable
        del self.taskQueue[task_i:-1]

        # Delete the event in the queue
        print(str(len(self.eventQueue)) + "events in queue.")
        old_event = self.eventQueue[0]
        del self.eventQueue[0]
        self.file_modified = True
        return old_event

    def update(self):
        # Run task
        if len(self.taskQueue) > 0:
            pass
        # There is no task remain to do, load new tasks.
        elif len(self.eventQeueu) > 0:
            # Load new event task
            self.taskQueue.append(self.eventQueue[0].getTasks())
        # Idle
        else:
            pass

        # Auto saving
        if self.saver.file_save_check(self.file_modified):
            self.saver.save(self._create_json_obj())
            self.file_modified = False

    def print(self):
        print("Event==================================")
        print(str(len(self.eventQueue)) + "events in queue.")
        print(str(len(self.taskQueue)) + "tasks in queue.")
        for e in self.eventQueue:
            e.print()
    
    def _create_json_obj(self):
        events_json = {
                "eventQueue": self.eventQueue,
                "taskQueue":self.taskQueue
                }
        return events_json

    def close(self):
        self.saver.save(self._create_json_obj())

if __name__ == '__main__':
    machine = Machine.Machine(40)
    event_handler = EventHandler(machine)
    event_handler.addEvent(Event(PRIORITY_CLOTH_SORTING))
    event_handler.addEvent(Event(PRIORITY_CLOTH_DRYING))
    event_handler.addEvent(Event(PRIORITY_CLOTH_DRYING))
    event_handler.addEvent(Event(PRIORITY_CLOTH_GATHERING))
    event_handler.addEvent(Event(PRIORITY_CLOTH_GATHERING))
    event_handler.print()
