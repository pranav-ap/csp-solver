from typing import Dict, List, Tuple
from .Variable import ValueType, NameType, Variable
from .Domain import Domain
from .Constraint import Constraint, FunctionConstraint


class CSP:
    def __init__(self) -> None:
        self.variables: Dict[NameType, Variable] = {}
        self.domains: Dict[NameType, Domain] = {}
        self.constraints: List[Tuple[Constraint, List[str]]] = []

    def add_variable(self, name: NameType, domain: List[ValueType]):
        if name in self.variables:
            raise ValueError('${name} is already declared as a variable')

        self.variables[name] = Variable(name)
        self.domains[name] = Domain(domain)

    def add_variables(self, names: List[NameType], domain: List[ValueType]):
        for name in names:
            self.add_variable(name, domain)

    def add_constraint(self, constraint, names=None):
        if callable(constraint):
            constraint = FunctionConstraint(constraint)
        elif not names:
            names = list(self.variables.keys())

        self.constraints.append((constraint, names))

    # domains

    def revert_domain_state(self):
        for domain in self.domains.values():
            domain.revert_state()

    def save_domain_state(self):
        for domain in self.domains.values():
            domain.save_state()

    # constraints

    def get_constraints(self, k: int):
        constraints = [(constraint, names)
                       for constraint, names in self.constraints
                       if len(names) == k]

        return constraints

    def get_related_constraints(self, name: NameType, k: int):
        constraints = []

        if k == 0:
            k = len(self.variables)

        constraints = self.get_constraints(k)
        filter(lambda _, scope: name in scope, constraints)
        return constraints
