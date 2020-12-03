from typing import List, Union
from .CSP import CSP
from .Variable import ValueType, Variable
from .Assignment import Assignment
from .Inference import MAC
from random import random


class ConstraintSolver:
    def __init__(self, csp: CSP) -> None:
        self.csp = csp

    def _is_complete(self, assignment):
        keys1 = set(assignment.keys())
        keys2 = set(self.csp.variables.keys())

        return keys1 == keys2

    def _create_values_list(self, assignment: Assignment, name: str, value: ValueType, names: List[str]):
        values = []

        for n in names:
            if n == name:
                values.append(value)
            elif n in assignment and assignment[n]:
                values.append(assignment[n])
            else:
                return None

        return values

    def _is_k_consistent(self, assignment: Assignment, name: str, value: ValueType, k: int):
        constraints = self.csp.get_related_constraints(name, k)

        for constraint, names in constraints:
            values = self._create_values_list(assignment, name, value, names)

            if values and not constraint.is_satisfied(*values):
                return False

        return True

    def _is_consistent(self, assignment: Assignment, name: str, value: ValueType):
        # test arc consistency
        if not self._is_k_consistent(assignment, name, value, 2):
            return False

        # test global consistency
        if not self._is_k_consistent(assignment, name, value, 0):
            return False

        return True

    def _make_node_consistent(self, name: str):
        constraints = self.csp.get_related_constraints(name, 1)

        for constraint, [name] in constraints:
            X = self.csp.domains[name]
            revised_domain = [x for x in X if constraint.is_satisfied(x)]

            if not revised_domain:
                return False

            self.csp.domains[name].replace(revised_domain)

        return True

    def _inference(self, name: str):
        is_consistent = MAC(self.csp, name)

        if not is_consistent:
            return False

        inferences = {
            name: domain[0] for name, domain in self.csp.domains.items() if len(domain) == 1}

        return inferences

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
        return domain

    def solve(self) -> Assignment:
        raise NotImplementedError()


class BacktrackingSolver(ConstraintSolver):
    def __init__(self, csp: CSP) -> None:
        super().__init__(csp)

    def _backtrack(self, assignment):
        if self._is_complete(assignment):
            return assignment

        variable = self._select_unassigned_variable(assignment)
        ordered_domain = self._get_ordered_domain_values(variable)

        for value in ordered_domain:
            name = variable.name

            if self._is_consistent(assignment, name, value):
                variable.value = value
                assignment[name] = value

                self.csp.save_domain_state()

                inferences = self._inference(name)

                if inferences or inferences == {}:
                    assignment = {**assignment, **inferences}
                    result = self._backtrack(assignment)

                    if result:
                        return result

                # reset

                self.csp.revert_domain_state()

                del assignment[name]
                for key, _ in inferences.items():
                    assignment.pop(key, None)

        return False

    def solve(self) -> Union[Assignment, bool]:
        assignment = {}

        for name in self.csp.variables.keys():
            is_consistent = self._make_node_consistent(name)

            if not is_consistent:
                return False

        return self._backtrack(assignment)


class MinConflictsSolver(ConstraintSolver):
    def __init__(self, csp: CSP, steps=1000) -> None:
        super().__init__(csp)
        self._steps = steps

    def solve(self) -> Assignment:
        assignment = {}

        # Initial assignment

        for name, variable in self.csp.variables:
            assignment[name] = random.choice(variable.domain)

        for _ in range(self._steps):
            conflicted = False

            if not conflicted:
                return assignment

        return None
