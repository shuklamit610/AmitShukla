# ----------------------------------------------------------
# Array
# ----------------------------------------------------------
class Array:

    def __init__(self):
        self.data = []

    def insert(self, value):
        self.data.append(value)

    def delete(self, value):
        self.data.remove(value)

    def access(self, index):
        return self.data[index]


# ----------------------------------------------------------
# Stack
# ----------------------------------------------------------
class Stack:

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) == 0:
            return None
        return self.items.pop()

    def peek(self):
        if len(self.items) == 0:
            return None
        return self.items[-1]


# ----------------------------------------------------------
# Queue
# ----------------------------------------------------------
class Queue:

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if len(self.items) == 0:
            return None
        return self.items.pop(0)

    def front(self):
        if len(self.items) == 0:
            return None
        return self.items[0]


# ----------------------------------------------------------
# Linked List Node
# ----------------------------------------------------------
class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


# ----------------------------------------------------------
# Singly Linked List
# ----------------------------------------------------------
class LinkedList:

    def __init__(self):
        self.head = None

    def insert(self, data):

        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node

    def delete(self, value):

        current = self.head
        previous = None

        while current:

            if current.data == value:

                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                return

            previous = current
            current = current.next

    def traverse(self):

        current = self.head

        while current:
            print(current.data)
            current = current.next


# ----------------------------------------------------------
# Demonstration
# ----------------------------------------------------------
array = Array()

array.insert(10)
array.insert(20)
array.insert(30)

print(array.access(1))

stack = Stack()

stack.push(100)
stack.push(200)

print(stack.pop())

queue = Queue()

queue.enqueue(1)
queue.enqueue(2)

print(queue.dequeue())

linked = LinkedList()

linked.insert(5)
linked.insert(15)
linked.insert(25)

linked.delete(15)

linked.traverse()