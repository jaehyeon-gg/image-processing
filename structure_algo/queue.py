class Queue :
    def __init__(self):
        self.data =[]

    def _enqueue(self,element):
        self.data.append(element)
    
    def _dequeue(self):
        self.data.