class Constraint:
    def __init__(self, condition, parameters):
        self.condition = condition
        self.parameters = parameters  # list

    def _get_params(self, assignment):
        return [assignment[name] for name in self.parameters]

    def is_satisfied(self, assignment):
        params = self._get_params(assignment)
        return self.condition(*params)

    def is_pleased(self, input):
        return self.condition(*input)


# Equality


def all_different_constraint():
    def constraint(*params):
        list_len = len(params)
        set_len = len(set(params))

        return list_len == set_len

    return constraint


def all_equal_constraint():
    def constraint(*params):
        set_len = len(set(params))
        return set_len == 1

    return constraint


def all_equal_to_constraint(value):
    def constraint(*params):
        return all(params, lambda p: p == value)

    return constraint


# Count


def count_equal_to_constraint(limit, value):
    def constraint(*params):
        length = params.count(value)
        return length == limit

    return constraint


def count_greater_than_constraint(limit, value):
    def constraint(*params):
        length = params.count(value)
        return length > limit

    return constraint


def count_less_than_constraint(limit, value):
    def constraint(*params):
        length = params.count(value)
        return length < limit

    return constraint


def count_ge_constraint(limit, value):
    def constraint(*params):
        length = params.count(value)
        return length >= limit

    return constraint


def count_le_constraint(limit, value):
    def constraint(*params):
        length = params.count(value)
        return length <= limit

    return constraint


# Sum


def max_sum_constraint(max_sum):
    def constraint(*params):
        return sum(params) <= max_sum

    return constraint


def min_sum_constraint(min_sum):
    def constraint(*params):
        return sum(params) >= min_sum

    return constraint


def exact_sum_constraint(exact_sum):
    def constraint(*params):
        return sum(params) == exact_sum

    return constraint
