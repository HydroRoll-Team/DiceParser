import uuid
from oneroll.include.diceparser.diceparserhelper import Dice

class ExecutionNode:
    def __init__(self):
        self.m_previousNode = None
        self.m_result = None
        self.m_nextNode = None
        self.m_errors = {}
        self.m_id = str(uuid.uuid4())

    def run(self, previous=None):
        pass

    def get_result(self):
        return self.m_result

    def set_next_node(self, node):
        self.m_nextNode = node

    def get_next_node(self):
        return self.m_nextNode

    def get_previous_node(self):
        return self.m_previousNode

    def set_previous_node(self, node):
        self.m_previousNode = node

    def to_string(self, with_label):
        pass

    def get_priority(self):
        pass

    def get_execution_error_map(self):
        if self.m_nextNode:
            keys = self.m_nextNode.get_execution_error_map().keys()
            for key in keys:
                self.m_errors[key] = self.m_nextNode.get_execution_error_map().get(key)
        return self.m_errors

    def generate_dot_tree(self, s):
        str_ = self.to_string(True)
        if str_ in s:
            return
        s += self.to_string(True)
        s += ";\n"

        if self.m_nextNode:
            s += self.to_string(False)
            s += " -> "
            s += self.m_nextNode.to_string(False)
            s += "[label=\"next\"];\n"
            self.m_nextNode.generate_dot_tree(s)
        else:
            s += self.to_string(False)
            s += " -> nullptr;\n"

        if self.m_result:
            s += self.to_string(False)
            s += " ->"
            s += self.m_result.to_string(False)
            s += " [label=\"Result\", style=\"dashed\"];\n"
            if not self.m_nextNode:
                self.m_result.generate_dot_tree(s)

    def get_help(self):
        return ""

    def get_copy(self):
        pass

    def get_scalar_result(self):
        if self.m_result is None:
            return 0
        return int(self.m_result.get_result(Dice.RESULT_TYPE.SCALAR))