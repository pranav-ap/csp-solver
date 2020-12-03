from typing import Dict, List, Tuple
from .Variable import ValueType, Variable
from .Domain import Domain
from .Constraint import Constraint, FunctionConstraint, GlobalConstraint


class CSP:
    def __init__(self) -> None:
        self.variables: Dict[str, Variable] = {}
        self.domains: Dict[str, Domain] = {}
        self.constraints: List[Tuple[Constraint, List[str]]] = []

    def add_variable(self, name: str, domain: List[ValueType]):
        if name in self.variables:
            raise ValueError('${name} is already declared as a variable')

        self.variables[name] = Variable(name)
        self.domains[name] = Domain(domain)

    def add_constraint(self, constraint, names=None):
        if callable(constraint):
            constraint = FunctionConstraint(constraint)
        elif not names:
            names = [name for name in self.variables.keys()]

        self.constraints.append((constraint, names))

    # domains

    def revert_domain_state(self):
        for domain in self.domains.values():
            domain.revert_state()

    def save_domain_state(self):
        for domain in self.domains.values():
            domain.save_state()

    # constraints

    def get_global_constraints(self):
        constraints = [(constraint, names)
                       for constraint, names in self.constraints if isinstance(constraint, GlobalConstraint)]

        return constraints

    def get_constraints(self, k: int):
        constraints = [(constraint, names)
                       for constraint, names in self.constraints
                       if len(names) == k and not isinstance(constraint, GlobalConstraint)]

        return constraints

    def get_related_constraints(self, name: str, k: int):
        constraints = []

        if k == 0:
            constraints = self.get_global_constraints()
        else:
            constraints = self.get_constraints(k)

        filter(lambda _, scope: name in scope, constraints)
        return constraints
