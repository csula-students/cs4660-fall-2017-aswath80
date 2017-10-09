"""
Custom stack implementation
"""

class Stack(object):
    """
    Custom stack implementation
    """
    def __init__(self):
        self.stack = []

    def push(self, node):
        """
        Stack.push
        """
        self.stack.insert(0, node)

    def pop(self):
        """
        Stack.pop
        """
        if not self.empty():
            return self.stack.pop(0)
        else:
            raise ValueError("Empty Stack")

    def peek(self):
        """
        Stack.peek
        """
        if not self.empty():
            return self.stack[-1]
        else:
            raise ValueError("Empty Stack")

    def size(self):
        """
        Stack.size
        """
        return len(self.stack)

    def empty(self):
        """
        Stack.empty
        """
        return self.size() == 0
                                     