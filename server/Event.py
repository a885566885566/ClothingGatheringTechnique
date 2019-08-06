"Number larger has higher priority"
PRIORITY_CLOTH_SORTING = 1
PRIORITY_CLOTH_GATHERING = 2
PRIORITY_CLOTH_DRYING = 3

class Machine:
    def __init__(self, capacity):
        self.index = 0
        self.MAX_CAPACITY = capacity
        self.clothes = []
        self.
"
The detail working command of events, handling motor movements.
Param:
    lock: If set to True, indicating that this task is not interruptable.
"
class Task:
    def __init__(self, lock=False):
        self.working_lock = lock

"
The parent class of Events
"
class Event:
    def __init__(self, p):
        self.prioity = p
        self.tasksQueue = []

class ClothSortingEvent(Event):
    def __init__(self):
        super().__init__(PRIORITY_CLOTH_SORTING)

class ClothDryingEvent(Event):
    def __init__(self):
        super().__init__(PRIORITY_CLOTH_DRYING)

class ClothGatheringEvent(Event):
    def __init__(self):
        super().__init__(PRIORITY_CLOTH_GATHERING)

"
Dealing with event flow, that is, event inserting, deleting and running.
"
class EventHandler:
    def __init__(self, machine):
        self.eventQueue = []
        self.taskQueue = []
        self.maching = machine
    
    "
    Add event according to the event's priority, and if the running event interrupting
    is needed, it will store the old event automatically, and reschedule it.
    "
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
            self.taskQueue.append(self.eventQueue[0].getTasks())

        else:
            self.eventQueue.insert(i, new_event)
        
        # The old event need to be stored(If it exists), this must run at the end,
        # otherwise, it might cause recursive logic error
        if old_Event:
            self.addEvent(old_event)

    "
    Delete the running event. If the running event have some locked task that can not 
    be interrupted, it will keep them untill interruption can be performed. Finally, 
    push new event in the eventQueue.
    It will return the old event if it exist.
    "
    def deleteRunningEvent(self):
        if len(self.eventQueue) <= 0:
            return None
        # Check if the running task is interruptable
        task_i = 0
        while task_i < len(self.taskQueue) and self.taskQueue[task_i].working_lock:
            task_i += 1
        
        # Delete all task that are interruptable
        del self.taskQueue[task_i:-1]

        # Delete the event in the queue
        print(str(len(self.eventQueue)) + "events in queue.")
        old_event = self.eventQueue[0]
        del self.eventQueue[0]
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

    def printState(self):
        print(str(len(self.eventQueue)) + "events in queue.")
        print(str(len(self.taskQueue)) + "tasks in queue.")
        print("==================================")
        pass
