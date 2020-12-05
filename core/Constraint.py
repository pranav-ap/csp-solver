from core.Variable import ValueType


class Constraint:
    def is_satisfied(self, *scope) -> bool:
        pass


class FunctionConstraint(Constraint):
    def __init__(self, func):
        self._func = func

    def is_satisfied(self, *scope) -> bool:
        return self._func(*scope)


# Equality


class AllDifferentConstraint(Constraint):
    def is_satisfied(self, *scope) -> bool:
        list_len = len(list(scope))
        set_len = len(set(scope))

        return list_len == set_len


class AllEqualConstraint(Constraint):
    def is_satisfied(self, *scope) -> bool:
        set_len = len(set(scope))
        return set_len == 1


class AllEqualToConstraint(Constraint):
    def __init__(self, value: ValueType) -> None:
        self.value = value

    def is_satisfied(self, *scope) -> bool:
        length = scope.count(self.value)
        return length == len(scope)


# Value Count


class ValueCountEqualToConstraint(Constraint):
    def __init__(self, limit: int, value: ValueType) -> None:
        self.limit = limit
        self.value = value

    def is_satisfied(self, *scope) -> bool:
        length = scope.count(self.value)
        return length == self.limit


class ValueCountUpperLimitConstraint(Constraint):
    def __init__(self, upper_limit: int, value: ValueType) -> None:
        self.upper_limit = upper_limit
        self.value = value

    def is_satisfied(self, *scope) -> bool:
        length = scope.count(self.value)
        return length <= self.upper_limit


class ValueCountLowerLimitConstraint(Constraint):
    def __init__(self, lower_limit: int, value: ValueType) -> None:
        self.lower_limit = lower_limit
        self.value = value

    def is_satisfied(self, *scope) -> bool:
        length = scope.count(self.value)
        return length >= self.lower_limit


# Sum


class MaxSumConstraint(Constraint):
    def __init__(self, max_sum: int) -> None:
        self.max_sum = max_sum

    def is_satisfied(self, *scope) -> bool:
        return sum(list(scope)) <= self.max_sum


class MinSumConstraint(Constraint):
    def __init__(self, min_sum: int) -> None:
        self.min_sum = min_sum

    def is_satisfied(self, *scope) -> bool:
        return sum(list(scope)) >= self.min_sum


class ExactSumConstraint(Constraint):
    def __init__(self, exact_sum: int) -> None:
        self.exact_sum = exact_sum

    def is_satisfied(self, *scope) -> bool:
        return sum(list(scope)) == self.exact_sum
