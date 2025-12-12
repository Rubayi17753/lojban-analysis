class LockedVal:

    def __init__(self, lock=0):
        self._val = None
        self.lock = 0
        
    def getx(self):
        return self._val

    def setx(self, value):
        if not self.lock:
            self._val = value

    def delx(self):
        del self._val

    docx = '''
    LockedVal has attributes .val .lock ._val
    if .lock is set to True, .val does not change when assigned.
    ._val plays a role in internal mechanics and should not be accessed from outside.
    '''

    val = property(getx, setx, delx, docx)