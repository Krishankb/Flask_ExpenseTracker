import threading


class UserGroup:

    def set_members(self, members):
        self.lock.acquire()
        self.members = members
        self.lock.release()

    def add_expense(self, expense):
        self.lock.acquire()
        self.expenses.append(expense)
        self.lock.release()

    def __init__(self, name, members=None):
        self.name = name
        self.members = members
        self.expenses = []
        self.lock = threading.Lock()
