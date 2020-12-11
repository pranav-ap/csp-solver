from typing import List, Union
from random import choice, shuffle
from .CSP import CSP
from .Variable import ValueType, Variable, NameType
from .Assignment import Assignment
from .Inference import MAC


class ConstraintSolver:
    def __init__(self, csp: CSP) -> None:
        self.csp = csp

    def _make_node_consistent(self):
        for name in self.csp.variables:
            constraints = self.csp.get_related_constraints(name, 1)

            for constraint, [name] in constraints:
                X = self.csp.domains[name]
                revised_domain = [x for x in X if constraint.is_satisfied(x)]

                if not revised_domain:
                    return False

                self.csp.domains[name].replace(revised_domain)

        return True

    def solve(self) -> Assignment:
        raise NotImplementedError()


class BacktrackingSolver(ConstraintSolver):
    def __init__(self, csp: CSP) -> None:
        super().__init__(csp)

    def _is_complete(self, assignment):
        keys1 = set(assignment.keys())
        keys2 = set(self.csp.variables.keys())

        return keys1 == keys2

    def _inference(self, name: NameType):
        is_consistent = MAC(self.csp, name)

        if not is_consistent:
            return False

        inferences = {
            name: domain[0] for name, domain in self.csp.domains.items() if len(domain) == 1}

        return inferences

    def _create_parameters(self, assignment: Assignment, name: NameType, value: ValueType, names: List[NameType]):
        values = []

        for n in names:
            if n == name:
                values.append(value)
            elif n in assignment:
                values.append(assignment[n])
            else:
                return None

        return values

    def _select_unassigned_variable(self, assignments) -> Variable:
        variable_names = list(
            set(self.csp.variables.keys()) - set(assignments.keys()))

        if not variable_names:
            return None

        # Minimum remaining values

        variable_name = min(
            variable_names, key=lambda name: len(self.csp.domains[name]))

        # todo: consider degree heuristic here as secondary

        return self.csp.variables[variable_name]

    def _get_ordered_domain_values(self, variable: Variable):
        domain = self.csp.domains[variable.name]
        # todo: perform value ordering
        shuffle(domain.values)
        return domain

    def _is_k_consistent(self, assignment: Assignment, name: NameType, value: ValueType, k: int):
        constraints = self.csp.get_related_constraints(name, k)

        for constraint, names in constraints:
            values = self._create_parameters(assignment, name, value, names)

            if values and not constraint.is_satisfied(*values):
                return False

        return True

    def _is_consistent(self, assignment: Assignment, name: NameType, value: ValueType):
        return self._is_k_consistent(assignment, name, value, 2) and self._is_k_consistent(assignment, name, value, 0)

    def _backtrack(self, assignment):
        if self._is_complete(assignment):
            return assignment

        variable = self._select_unassigned_variable(assignment)
        ordered_domain = self._get_ordered_domain_values(variable)

        for value in ordered_domain:
            name = variable.name

            if self._is_consistent(assignment, name, value):
                variable.value = value
                self.csp.save_domain_state()

                inferences = self._inference(name)

                if inferences or inferences == {}:
                    result = self._backtrack(
                        {**assignment, name: value, **inferences})

                    if result:
                        return result

                self.csp.revert_domain_state()

        return False

    def solve(self) -> Union[Assignment, bool]:
        assignment = {}

        is_consistent = self._make_node_consistent()

        if not is_consistent:
            return False

        return self._backtrack(assignment)


class MinConflictsSolver(ConstraintSolver):
    def __init__(self, csp: CSP, steps=500) -> None:
        super().__init__(csp)
        self._steps = steps

    def _is_solution(self, conflicted_variables):
        result = all([value == 0 for value in conflicted_variables.values()])
        return result

    def _create_parameters(self, assignment: Assignment, names: List[NameType]):
        values = []

        for n in names:
            if n in assignment:
                values.append(assignment[n])
            else:
                return None

        return values

    def _value_with_min_conflicts(self, name: NameType, assignment: Assignment):
        conflicts_count = {}

        for value in self.csp.domains[name].values:
            conflicts_count[value] = 0

            for constraint, names in self.csp.constraints:
                assignment[name] = value
                values = self._create_parameters(assignment, names)

                if values and not constraint.is_satisfied(*values):
                    conflicts_count[value] += 1

        min_value = min(conflicts_count, key=conflicts_count.get)
        return min_value

    def _get_conflicted_variable(self, conflict_counts):
        conflict_counts = {name: conflicts
                           for name, conflicts in conflict_counts.items() if conflicts > 0}

        name = choice(list(conflict_counts.keys()))

        return name

    def _get_conflict_counts(self, assignment: Assignment):
        conflicted_variables = {key: 0 for key in assignment.keys()}

        for constraint, names in self.csp.constraints:
            values = self._create_parameters(assignment, names)

            if values and not constraint.is_satisfied(*values):
                for name in names:
                    conflicted_variables[name] += 1

        return conflicted_variables

    def _min_conflicts(self, assignment):
        # Initial complete assignment
        for name, domain in self.csp.domains.items():
            assignment[name] = choice(domain.values)

        for _ in range(self._steps):
            conflict_counts = self._get_conflict_counts(assignment)

            if self._is_solution(conflict_counts):
                return assignment, True

            name = self._get_conflicted_variable(conflict_counts)
            value = self._value_with_min_conflicts(name, assignment)

            # set value
            assignment[name] = value
            self.csp.variables[name].value = value

        return assignment, False

    def solve(self, assignment=None) -> Assignment:
        assignment = assignment or {}

        is_consistent = self._make_node_consistent()

        if not is_consistent:
            return assignment, False

        return self._min_conflicts(assignment)
