import re

def make_replacement(pattern, command, cmd):
    has_pattern = pattern in cmd
    if has_pattern:
        idx_pattern = cmd.index(pattern)
        quotes = []
        pos = 0
        open = True
        while pos != -1 and pos < len(cmd):
            old_pos = pos
            pos = cmd.find("\"", pos)
            if open and pos != -1:
                open = False
            elif pos != -1:
                quotes.append((old_pos, pos))
            if pos != -1:
                pos += 1
        has_quote = False
        for range in quotes:
            if idx_pattern < range[1] and idx_pattern >= range[0]:
                has_quote = True
        has_variable = "${" in cmd
        comment_pos = cmd.rfind("#")
        if not has_quote and not has_variable:
            cmd = cmd.replace(pattern, command)
        else:
            pattern_pos_list = []
            variable_pos = []
            pos = 0
            while pos != -1:
                start = cmd.find("${", pos)
                if start >= 0:
                    end = start + len(re.match(r"\${\w+}", cmd[start:]).group())
                    variable_pos.append((start, end))
                    pos = end + 1
                else:
                    pos = start
            pos = 0
            while pos != -1:
                start = cmd.find("\"", pos)
                if start >= 0:
                    end = cmd.find("\"", start + 1)
                    variable_pos.append((start, end))
                    pos = end + 1
                else:
                    pos = start
            pos = 0
            while True:
                pos = cmd.find(pattern, pos)
                if pos == -1:
                    break
                is_inside_pair = False
                for pair in variable_pos:
                    if not is_inside_pair:
                        is_inside_pair = pos > pair[0] and pos < pair[1]
                    if comment_pos >= 0 and pos > comment_pos:
                        is_inside_pair = True
                if not is_inside_pair:
                    pattern_pos_list.append(pos)
                pos += 1
            for i in reversed(pattern_pos_list):
                cmd = cmd[:i] + command + cmd[i+1:]
    return cmd

class DiceAlias:
    def __init__(self, pattern, command, comment, is_replace, is_enable):
        self.m_pattern = pattern
        self.m_command = command
        self.m_comment = comment
        self.m_type = "REPLACE" if is_replace else "REGEXP"
        self.m_is_enable = is_enable

    def resolved(self, str):
        if not self.m_is_enable:
            return False
        if self.m_type == "REPLACE" and self.m_pattern in str:
            str = make_replacement(self.m_pattern, self.m_command, str)
            return True
        elif self.m_type == "REGEXP":
            exp = re.compile(self.m_pattern)
            str = exp.sub(self.m_command, str)
            return True
        return False

    def set_command(self, command):
        self.m_command = command

    def set_pattern(self, pattern):
        self.m_pattern = pattern

    def set_type(self, type):
        self.m_type = "REPLACE" if type == "REPLACE" else "REGEXP"

    def command(self):
        return self.m_command

    def pattern(self):
        return self.m_pattern

    def is_replace(self):
        return self.m_type == "REPLACE"

    def set_replace(self, b):
        self.m_type = "REPLACE" if b else "REGEXP"

    def is_enable(self):
        return self.m_is_enable

    def set_enable(self, b):
        self.m_is_enable = b

    def comment(self):
        return self.m_comment

    def set_comment(self, comment):
        self.m_comment = comment