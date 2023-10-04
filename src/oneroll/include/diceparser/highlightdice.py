from typing import List, Dict

class HighLightDice:
    def __init__(self, result: List[int], isHighlighted: bool, color: str, displayed: bool, faces: int, uuid: str):
        self.result = result
        self.isHighlighted = isHighlighted
        self.color = color
        self.displayed = displayed
        self.faces = faces
        self.uuid = uuid

class ExportedDiceResult:
    def __init__(self):
        self.data: Dict[int, List[List[HighLightDice]]] = {}

    def addResult(self, key: int, result: List[HighLightDice]):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(result)
