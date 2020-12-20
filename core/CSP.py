from .Constraint import Constraint
from itertools import product


class DualCSP:
    def __init__(self):
        self.variables = set()  # just the names
        self.parameters = {}  # name -> [names]
        self.domains = {}  # name -> set(tuples)

        self.neighbors = {}  # (name 1, name 2) => set(common parameters)


class NaryCSP:
    def __init__(self) -> None:
        self.variables = set()  # just the names
        self.constraints = []  # [Constraint]
        self.domains = {}  # name -> set(values)

        # book-keeping

        self.scope_to_constraints = {}  # set(scope) -> [Constraint]
        self.name_to_constraints = {}  # name -> [Constraint]
        self.neighbors = {}  # name -> set(names)

    def add_variable(self, name, domain):  # domain is a set
        if name in self.variables:
            raise ValueError('${name} is already declared as a variable')

        self.variables.add(name)
        self.domains[name] = domain
        self.name_to_constraints[name] = set()
        self.neighbors[name] = set()

    def add_variables(self, names, domain):
        for name in names:
            self.add_variable(name, domain)

    def add_constraint(self, constraint, params=None):  # params is a list
        params = params or list(self.variables)
        scope = set(params)

        if not len(scope):
            raise ValueError('Scope cannot be empty')

        constraint = Constraint(constraint, scope, params)
        self.constraints.append(constraint)

        # book-keeping

        if scope not in self.scope_to_constraints:
            self.scope_to_constraints[tuple(params)] = set()

        self.scope_to_constraints[tuple(params)].add(constraint)

        for name in scope:
            # name_to_constraints
            self.name_to_constraints[name].add(constraint)

            # neighbors
            other_neighbors = scope.difference({name})
            self.neighbors[name].update(other_neighbors)

    # Domain

    def restore(self, removals):
        for name, value in removals:
            self.domains[name].add(value)

    def suppose(self, name, value):
        removals = [(name, val) for val in self.domains[name] if val != value]
        self.domains[name] = {value}
        return removals

    # Assignment

    def assign(self, var, val, assignment):
        assignment[var] = val

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    def is_complete(self, assignment):
        keys = set(assignment.keys())
        return keys == self.variables


class DualGraphMaker:
    def __init__(self, csp: CSP):
        super().__init__()
        self.csp = csp
        self.dual_csp = CSP()

        self.auxillary_neighbors = {}  # name -> set(names)
        self.auxillary_name_to_originals = {}  # name -> set(names)
        self.original_to_auxillaries = {}  # name -> set(names)
        self.auxillary_name_to_constraint = {}  # name -> Constraint

        self._auxillary_variable_id = 0

    def _get_aux_var_id(self):
        id = self._auxillary_variable_id
        self._auxillary_variable_id += 1
        return id

    def create_auxillary_name(self):
        auxillary_name = 'aux_' + self._get_aux_var_id()

        if auxillary_name in self.dual_csp.variables:
            raise ValueError('${auxillary_name} is already declared')

        return auxillary_name

    def create_auxillary_domain(self, constraint):
        domain = product(*[self.csp.domains[name]
                           for name in constraint.parameters])
        filter(domain, lambda tuple_value: constraint.is_satisfied(*tuple_value))
        return domain

    def add_auxillary_variable(self, auxillary_name, domain):
        self.dual_csp.add_variable(auxillary_name, domain)

    def calc_original_to_auxillaries(self):
        for original in self.csp.variables:
            original_neighbors = self.csp.neighbors[original]
            auxillary_neighbors = [auxillary
                                   for auxillary, originals in self.auxillary_name_to_originals.items()
                                   if original_neighbors.intersection(originals)]

            self.original_to_auxillaries[original] = auxillary_neighbors

    def calc_neighbors(self):
        for aux_name, originals in self.auxillary_name_to_originals.items():
            aux_neighbors = [self.original_to_auxillaries[original]
                             for original in originals]

            if aux_name not in self.auxillary_neighbors:
                self.auxillary_neighbors[aux_name] = set()

            self.auxillary_neighbors[aux_name].update(aux_neighbors)

    def add_auxillary_constraint(self, aux_name, constraint):
        pass

    def convert(self) -> CSP:
        for constraint in self.csp.constraints:
            # add auxillary variable
            aux_name = self.create_auxillary_name()
            domain = self.create_auxillary_domain(constraint)
            self.add_auxillary_variable(aux_name, domain)

            # book-keeping
            self.auxillary_name_to_originals[aux_name] = constraint.scope
            self.auxillary_name_to_constraint[aux_name] = constraint

        self.calc_original_to_auxillaries()
        self.calc_neighbors()

        for aux_name, constraint in self.auxillary_name_to_constraint.items():
            self.add_auxillary_constraint(aux_name, constraint)

        return self.dual_csp
