from .Constraint import Constraint
from itertools import product


class NaryCSP:
    def __init__(self) -> None:
        self.variables = set()  # just the names
        self.constraints = []  # [Constraint]
        self.domains = {}  # name -> set(values)

    def add_variable(self, name, domain):  # domain is a set
        if name in self.variables:
            raise ValueError('${name} is already declared as a variable')

        self.variables.add(name)
        self.domains[name] = domain

    def add_variables(self, names, domain):
        for name in names:
            self.add_variable(name, domain)

    def add_constraint(self, constraint, parameters=None):  # params is a list
        parameters = parameters or list(self.variables)

        if not len(parameters):
            raise ValueError('Scope cannot be empty')

        constraint = Constraint(constraint, parameters)
        self.constraints.append(constraint)


class DualCSP:
    def __init__(self):
        self.variables = set()  # just the names
        self.parameters = {}  # name => [names]
        self.domains = {}  # name => set(tuples)

        # (name 1, name 2) => set(common parameters)
        self.neighbors = {}

    def add_variable(self, name, domain):  # domain is a set
        self.variables.add(name)
        self.domains[name] = domain

    def set_parameters(self, name, parameters):
        self.parameters[name] = parameters

    def set_edge(self, v1, v2, scope_common):
        v1, v2 = (v1, v2) if v1 < v2 else (v2, v1)
        self.neighbors[(v1, v2)] = scope_common


class DualCSPBuilder:
    def __init__(self, csp: NaryCSP):
        super().__init__()
        self.csp = csp
        self.dual_csp = DualCSP()
        self._dual_variable_id = 0

    def _create_dual_name(self):
        id = self._dual_variable_id
        self._dual_variable_id += 1

        dual_name = 'dual_' + str(id)
        return dual_name

    def _create_dual_domain(self, constraint):
        domain = product(*[self.csp.domains[name]
                           for name in constraint.parameters])

        filtered_domain = set()

        for tuple_value in domain:
            if constraint.is_pleased(tuple_value):
                filtered_domain.add(tuple_value)

        return filtered_domain

    def _calculate_neighbors(self):
        for v1, v2 in product(self.dual_csp.variables, self.dual_csp.variables):
            if v1 == v2:
                continue

            scope_v1 = set(self.dual_csp.parameters[v1])
            scope_v2 = set(self.dual_csp.parameters[v2])
            scope_common = scope_v1.intersection(scope_v2)

            if len(scope_common):
                self.dual_csp.set_edge(v1, v2, scope_common)

    def convert(self) -> DualCSP:
        for constraint in self.csp.constraints:
            dual_name = self._create_dual_name()
            domain = self._create_dual_domain(constraint)
            self.dual_csp.add_variable(dual_name, domain)
            self.dual_csp.set_parameters(dual_name, constraint.parameters)

        self._calculate_neighbors()

        return self.dual_csp
