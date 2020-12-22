from .Constraint import Constraint
from itertools import product
from collections import defaultdict, namedtuple


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
        self.originals = set()  # just the names

        self.variables = set()  # just the names
        self.parameters = {}  # name => [names]
        self.domains = {}  # name => { tuples }

        self.overlaps = {}
        self.neighbors = defaultdict(set)

    def add_variable(self, name, domain):  # domain is a set
        self.variables.add(name)
        self.domains[name] = domain

    def set_parameters(self, name, parameters):
        self.parameters[name] = parameters

    def add_neighbor(self, n1, n2):
        self.neighbors[n1].add(n2)
        self.neighbors[n2].add(n1)

    def get_edges(self, of=None):
        if of is not None:
            edges = [(of, Y) for Y in self.neighbors[of]]
            return edges

        all_edges = list(self.overlaps.keys())
        return all_edges

    # overlap

    def set_overlap(self, name1, name2, scope_common):
        name1, name2 = (name1, name2) if name1 < name2 else (name2, name1)
        self.overlaps[(name1, name2)] = scope_common

    def get_overlap(self, name1, name2):
        name1, name2 = (name1, name2) if name1 < name2 else (name2, name1)
        return self.overlaps[(name1, name2)]

    def overlap_equality(self, tuple_n1, tuple_n2, common_names):
        for name in common_names:
            name = 'attr_' + str(name)
            element_n1 = getattr(tuple_n1, name)
            element_n2 = getattr(tuple_n2, name)

            if element_n1 != element_n2:
                return False

        return True

    # Domain

    def restore(self, removals):
        for name, tuple_value in removals:
            self.domains[name].add(tuple_value)

    def suppose(self, name, value):
        removals = [(name, val) for val in self.domains[name] if val != value]
        self.domains[name] = {value}
        return removals

    # Assignment

    def assign(self, name, value, assignment):
        assignment[name] = value

    def unassign(self, name, assignment):
        if name in assignment:
            del assignment[name]

    def twin_assignment(self, assignment):
        twin = {}

        for name in self.originals:
            name_attr = 'attr_' + str(name)
            for tuple_value in assignment.values():
                if hasattr(tuple_value, name_attr):
                    twin[name] = getattr(tuple_value, name_attr)
                    break

        return twin

    def is_complete(self, assignment):
        keys = set(assignment.keys())
        return keys == self.variables


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
        str_params = ['attr_' + str(p) for p in constraint.parameters]
        named_tuple = namedtuple('domain', str_params)

        domain = product(*[self.csp.domains[name]
                           for name in constraint.parameters])

        filtered_domain = set()

        for tuple_value in domain:
            if constraint.is_pleased(tuple_value):
                filtered_domain.add(named_tuple(*tuple_value))

        return filtered_domain

    def _calculate_neighbors(self):
        for n1, n2 in product(self.dual_csp.variables, self.dual_csp.variables):
            if n1 == n2:
                continue

            scope_n1 = set(self.dual_csp.parameters[n1])
            scope_n2 = set(self.dual_csp.parameters[n2])
            scope_common = scope_n1.intersection(scope_n2)

            if len(scope_common):
                self.dual_csp.add_neighbor(n1, n2)
                self.dual_csp.set_overlap(n1, n2, scope_common)

    def _calculate_variables(self):
        self.dual_csp.originals = self.csp.variables

        for constraint in self.csp.constraints:
            dual_name = self._create_dual_name()
            domain = self._create_dual_domain(constraint)
            self.dual_csp.add_variable(dual_name, domain)
            self.dual_csp.set_parameters(dual_name, constraint.parameters)

    def convert(self) -> DualCSP:
        self._calculate_variables()
        self._calculate_neighbors()
        return self.dual_csp
