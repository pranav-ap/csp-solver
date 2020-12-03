class Constraint:
    def is_satisfied(self, *scope) -> bool:
        pass


class FunctionConstraint(Constraint):
    def __init__(self, func):
        self._func = func

    def is_satisfied(self, *scope) -> bool:
        return self._func(*scope)


class GlobalConstraint(Constraint):
    def is_satisfied(self, *scope) -> bool:
        pass


class AllDifferentConstraint(GlobalConstraint):
    def is_satisfied(self, *scope) -> bool:
        return len(list(scope)) == len(set(scope))


class AllEqualConstraint(GlobalConstraint):
    def is_satisfied(self, *scope) -> bool:
        return len(set(scope)) == 1


class MaxSumConstraint(GlobalConstraint):
    def __init__(self, max_sum: int) -> None:
        self.max_sum = max_sum

    def is_satisfied(self, *scope) -> bool:
        return sum(list(scope)) <= self.max_sum


class MinSumConstraint(GlobalConstraint):
    def __init__(self, min_sum: int) -> None:
        self.min_sum = min_sum

    def is_satisfied(self, *scope) -> bool:
        return sum(list(scope)) >= self.min_sum


class ExactSumConstraint(GlobalConstraint):
    def __init__(self, exact_sum: int) -> None:
        self.exact_sum = exact_sum

    def is_satisfied(self, *scope) -> bool:
        return sum(list(scope)) == self.exact_sum
