class DieGroup(list):
    def __init__(self):
        self.excepted_value = 0

    def get_sum(self):
        return sum(self)

    def remove_value(self, i):
        for x in i:
            self.remove(x)

    def get_lost(self):
        return self.get_sum() - self.excepted_value


class GroupNode(ExecutionNode):
    def __init__(self, complex_output=False):
        super().__init__()
        self.scalar_result = ScalarResult()
        self.string_result = StringResult()
        self.group_value = 0
        self.groups_list = []
        self.complex_output = complex_output

    def run(self, previous):
        if self.complex_output:
            self.result = self.string_result
        else:
            self.result = self.scalar_result

        self.previous_node = previous
        if previous is not None:
            self.result.set_previous(previous.get_result())
            tmp_result = previous.get_result()
            if isinstance(tmp_result, DiceResult):
                result_list = tmp_result.get_result_list()
                all_result = DieGroup()
                for die in result_list:
                    all_result.append(die.get_list_value())
                all_result.sort(reverse=True)
                if all_result.get_sum() > self.group_value:
                    copy = all_result.copy()
                    die = self.get_group(all_result)

                    for group in die:
                        for val in group:
                            copy.remove(val)
                    
                    self.scalar_result.set_value(len(die))
                    values = []
                    for group in die:
                        values.append('{%s}' % ','.join(map(str, group)))
                    unused = list(map(str, copy))
                    if unused:
                        self.string_result.add_text('%s (%s - [%s])' % (len(die), ','.join(values), ','.join(unused)))
                    else:
                        self.string_result.add_text('%s (%s)' % (len(die), ','.join(values)))
                else:
                    self.scalar_result.set_value(0)

        if self.next_node is not None:
            self.next_node.run(self)

    def to_string(self, with_label):
        if with_label:
            return '{} [label="SplitNode Node"]'.format(self.id)
        else:
            return self.id

    def get_priority(self):
        priority = 0
        if self.next_node is not None:
            priority = self.next_node.get_priority()
        return priority

    def get_copy(self):
        node = GroupNode(self.complex_output)
        if self.next_node is not None:
            node.set_next_node(self.next_node.get_copy())
        return node

    def get_group_value(self):
        return self.group_value

    def set_group_value(self, group_value):
        self.group_value = group_value

    def compose_with_previous(self, previous, first, current, add_value):
        if previous.get_sum() + first + current == self.group_value:
            add_value.extend(previous)
            add_value.append(first)
            add_value.append(current)
            return True

        if not previous:
            return False

        max_combo_length = len(previous)
        has_reach_max = False

        possible_union = []
        for va in previous:
            die_g = DieGroup()
            die_g.append(va)
            possible_union.append(die_g)

        while not has_reach_max:
            tmp_values = previous.copy()
            possible_tmp = []
            for dia_g in possible_union:
                if not tmp_values:
                    break
                tmp_values.remove_value(dia_g)

                for value in tmp_values:
                    dia = DieGroup()
                    dia.extend(dia_g)
                    dia.append(value)
                    if len(dia) >= max_combo_length - 1:
                        has_reach_max = True
                    else:
                        possible_tmp.append(dia)
            if not possible_tmp:
                has_reach_max = True
            else:
                possible_tmp.extend(possible_union)
                possible_union = possible_tmp

        possible_union.sort(key=lambda x: x.get_lost(), reverse=True)
        found = False
        for value in possible_union:
            if value.get_sum() + current + first >= self.group_value:
                add_value.extend(value)
                add_value.append(current)
                add_value.append(first)
                found = True
                break

        return found

    def get_group(self, values):
        if not values:
            return []

        first = values.pop(0)

        result = []
        lose_map = {}
        if first >= self.group_value:
            group = DieGroup()
            group.append(first)
            lose_map[0] = group
        else:
            it = reversed(values)
            found_perfect = False
            cumulated_value = 0
            previous_value = DieGroup()
            while it and not found_perfect:
                if first + it[-1] == self.group_value:
                    found_perfect = True
                    group = DieGroup()
                    group.append(first)
                    group.append(it[-1])
                    lose_map[0] = group
                elif first + it[-1] > self.group_value:
                    group = DieGroup()
                    group.append(first)
                    group.append(it[-1])
                    lose_map[first + it[-1] - self.group_value] = group
                elif first + it[-1] + cumulated_value == self.group_value:
                    group = DieGroup()
                    group.append(first)
                    group.append(it[-1])
                    group.extend(previous_value)
                    found_perfect = True
                    lose_map[0] = group
                elif first + it[-1] + cumulated_value > self.group_value:
                    group = DieGroup()
                    group.excepted_value = self.group_value
                    b = self.compose_with_previous(previous_value, first, it[-1], group)
                    if b:
                        lose_map[group.get_lost()] = group
                previous_value.append(it[-1])
                cumulated_value += it[-1]
                it = it[:-1]

        if lose_map:
            die = lose_map[min(lose_map)]
            result.append(die)
            value_to_remove = die.copy()
            if value_to_remove:
                value_to_remove.remove(value_to_remove[0])
                values.remove_value(value_to_remove)

                if values.get_sum() >= self.group_value:
                    result.extend(self.get_group(values))

        return result