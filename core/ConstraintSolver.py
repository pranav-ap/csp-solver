from copy import deepcopy
from random import choice, shuffle
from .CSP import DualCSP
from .Inference import MAC


class ConstraintSolver:
    def __init__(self, csp: DualCSP):
        self.csp = csp

    def _nconflicts(self, name, value, assignment):
        raise NotImplementedError()

    def solve(self):
        raise NotImplementedError()


class MinConflictsSolver(ConstraintSolver):
    def __init__(self, csp: DualCSP, max_steps=100000):
        super().__init__(csp)
        self._max_steps = max_steps

    def _nconflicts(self, name, value, assignment):
        suppose = deepcopy(assignment)
        suppose[name] = value

        count = 0

        for (X, Y), overlap in self.csp.overlaps.items():
            tuple_value_X = suppose[X]
            tuple_value_Y = suppose[Y]

            if not self.csp.overlap_equality(tuple_value_X, tuple_value_Y, overlap):
                count += 1

        return count

    def _min_conflicts_value(self, name, assignment):
        domain = list(self.csp.domains[name])
        shuffle(domain)
        return min(domain, key=lambda value: self._nconflicts(name, value, assignment))

    def _conflicted_variables(self, assignment):
        return [name
                for name in self.csp.variables
                if self._nconflicts(name, assignment[name], assignment) > 0]

    def _initial_complete_assignment(self):
        assignment = {}

        for name in self.csp.variables:
            domain = self.csp.domains[name]
            tuple_value = choice(list(domain))
            self.csp.assign(name, tuple_value, assignment)

        return assignment

    def _min_conflicts(self, assignment):
        for step in range(self._max_steps):
            print('Step ', step)
            conflicted = self._conflicted_variables(assignment)

            if not conflicted:
                return assignment, True

            name = choice(conflicted)
            value = self._min_conflicts_value(name, assignment)
            self.csp.assign(name, value, assignment)

        return assignment, False

    def solve(self):
        assignment = self._initial_complete_assignment()
        assignment, is_valid = self._min_conflicts(assignment)
        assignment = self.csp.twin_assignment(assignment)
        return assignment, is_valid


# class BacktrackingSolver(ConstraintSolver):
#     def __init__(self, csp: DualCSP):
#         super().__init__(csp)

#     def _nconflicts(self, name, value, assignment):
#         count = 0

#         suppose = deepcopy(assignment)
#         suppose[name] = value
#         scope = set(suppose.keys())

#         for constraint in self.csp.constraints_map[name]:
#             if constraint.scope.issubset(scope) and not constraint.is_satisfied(suppose):
#                 count += 1

#         return count

#     def _select_unassigned_variable(self, assignment):
#         assigned_variables = set(assignment.keys())
#         unassigned_variables = list(
#             self.csp.variables.difference(assigned_variables))
#         shuffle(unassigned_variables)

#         name = min(
#             unassigned_variables,
#             key=lambda name: len(self.csp.domains[name]))

#         return name

#     def _order_domain_values(self, name, assignment):
#         return sorted(self.csp.domains[name], key=lambda value: self._nconflicts(name, value, assignment))

#     def _backtrack(self, assignment):
#         if self.csp.is_complete(assignment):
#             return assignment, True

#         name = self._select_unassigned_variable(assignment)
#         ordered_domain = self._order_domain_values(name, assignment)

#         for value in ordered_domain:
#             if self._nconflicts(name, value, assignment) == 0:
#                 self.csp.assign(name, value, assignment)
#                 removals = self.csp.suppose(name, value)

#                 if MAC(self.csp, name):
#                     assignment, valid = self._backtrack(assignment)
#                     if valid:
#                         return assignment, valid

#                 self.csp.restore(removals)

#         # no value for 'name' is consistent
#         self.csp.unassign(name, assignment)
#         return assignment, False

#     def solve(self):
#         assignment = {}
#         is_consistent = self._make_node_consistent()

#         if not is_consistent:
#             return assignment, False

#         return self._backtrack(assignment)
