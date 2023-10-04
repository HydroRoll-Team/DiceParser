from .explodedicenode import ExecutionNode
from ..result.stringresult import StringResult

class HelpNode(ExecutionNode):
    def __init__(self):
        super().__init__()
        self.m_path = "https://invent.kde.org/rolisteam/rolisteam-diceparser/-/blob/master/HelpMe.md"
        self.m_result = StringResult()

    def run(self, previous):
        self.m_previousNode = previous
        txtResult = self.m_result
        txtResult.setHighLight(False)

        if (previous is None) and (txtResult is not None):
            txtResult.addText("Rolisteam Dice Parser:\n" +
                              "\n" +
                              "Example (with ! as prefix):\n" +
                              "!2d6\n" +
                              "!1d20\n" +
                              "!6d10e10k3 (L5R)\n" +
                              "\n" +
                              "Full documentation at: %s" % self.m_path)
            self.m_result.setPrevious(None)
        elif previous is not None:
            txtResult.addText(previous.getHelp())
            self.m_result.setPrevious(previous.getResult())
        txtResult.finished()

        if self.m_nextNode is not None:
            self.m_nextNode.run(self)

    def toString(self, wl):
        if wl:
            return "{} [label=\"{} : {}\"]".format(self.m_id, self.m_path, "Rolisteam Dice Parser:\nFull documentation at")
        else:
            return self.m_id

    def getPriority(self):
        return 0

    def setHelpPath(self, path):
        self.m_path = path

    def getCopy(self):
        node = HelpNode()
        if self.m_nextNode is not None:
            node.setNextNode(self.m_nextNode.getCopy())
        return node
