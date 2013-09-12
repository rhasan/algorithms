from heapq import *
import itertools

class CustomPriorityQueue:

    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        #self.counter = itertools.count()     # unique sequence count
        self.N = 0


    def add(self,entry):
        'Add a new entry or update the priority of an existing task'
        (pr,val) = entry
        if val in self.entry_finder:
            remove(val)
        entry_list = [pr,val]
        self.entry_finder[val] = entry_list
        heappush(self.pq, entry_list)

        self.N += 1

    def remove(self,task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
        self.N -= 1

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, task = heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                self.N -= 1
                return (priority, task)
        raise KeyError('pop from an empty priority queue')
    
    def empty(self):
        return self.N == 0

    def replace(self,find,replace):
        
        self.remove(find)
        self.add(replace)
        


def main():
    pq = CustomPriorityQueue()

    data = [(10,"ten"), (3,"three"), (5,"five"), (7,"seven"), (9, "nine"), (2,"two")]

    for item in data:
        print item
        pq.add(item)

    pq.replace("ten",(1,"one"))
    #print pq.counter
    sorted_list = []

    while pq.empty()==False:
        sorted_list.append(pq.pop())
    print sorted_list

if __name__ == "__main__":
    main()
