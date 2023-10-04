import uuid

class Result:
    def __init__(self):
        self.m_resultTypes = 0
        self.m_id = str(uuid.uuid4())
        self.m_previous = None

    def getPrevious(self):
        return self.m_previous

    def setPrevious(self, p):
        assert p != self
        self.m_previous = p

    def isStringResult(self):
        return False

    def clear(self):
        pass

    def hasResultOfType(self, type):
        return bool(self.m_resultTypes & type)

    def generateDotTree(self, s):
        str_ = self.toString(True)
        if str_ in s:
            return
        s += str_
        s += ";\n"

        if self.m_previous:
            s += self.toString(False)
            s += " -> "
            s += self.m_previous.toString(False)
            s += "[label=\"previousResult\"]\n"
            self.m_previous.generateDotTree(s)
        else:
            s += self.toString(False)
            s += " -> "
            s += "nullptr"
            s += " [label=\"previousResult\", shape=\"box\"];\n"

    def getId(self):
        return self.m_id

    def getStringResult(self):
        return ""

    def getResult(self, type):
        pass

    def toString(self, wl):
        pass

    def getCopy(self):
        pass