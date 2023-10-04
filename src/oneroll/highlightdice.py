class HighLightDice:
    def __init__(self, result, isHighlighted, color, displayed, faces, uuid):
        self.m_result = result
        self.m_hasHighlight = isHighlighted
        self.m_color = color
        self.m_displayed = displayed
        self.m_faces = faces
        self.m_uuid = uuid

    def result(self):
        return self.m_result

    def setResult(self, result):
        self.m_result = result

    def isHighlighted(self):
        return self.m_hasHighlight

    def setHighlight(self, hasHighlight):
        self.m_hasHighlight = hasHighlight

    def color(self):
        return self.m_color

    def setColor(self, color):
        self.m_color = color

    def displayed(self):
        return self.m_displayed

    def setDisplayed(self, displayed):
        self.m_displayed = displayed

    def faces(self):
        return self.m_faces

    def setFaces(self, faces):
        self.m_faces = faces

    def getResultString(self):
        if len(self.m_result) == 1:
            return str(self.m_result[0])
        else:
            result_str = ', '.join(str(value) for value in self.m_result)
            total_score = sum(self.m_result)
            return f"{result_str} [{total_score}]"

    def uuid(self):
        return self.m_uuid

    def setUuid(self, uuid):
        self.m_uuid = uuid


class ListDiceResult(list):
    pass


class ExportedDiceResult(dict):
    pass
