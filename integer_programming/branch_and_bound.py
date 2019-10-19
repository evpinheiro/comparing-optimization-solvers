import math
import copy


class Relaxation:

    def __init__(self):
        self.bound = None

    def execute(self):
        pass

    def add_upper_bound(self, var_index, bound_value):
        pass

    def add_lower_bound(self, var_index, bound_value):
        pass

    def is_feasible(self):
        pass

    def get_bound(self):
        pass

    def get_solution(self) -> list:
        pass

    def get_dual(self) -> list:
        pass

    def get_reduced_cost(self) -> list:
        pass

    def evaluate_solution(self, solution):
        pass


class Node:

    def __init__(self, number, parent_node, relaxation: Relaxation):
        self.number = number
        self.parent_node = parent_node
        self.relaxation = relaxation

    def execute(self):
        self.relaxation.execute()
        print(self.__str__())

    def choose_variable(self):
        for i, sol in enumerate(self.relaxation.get_solution()):
            if int(sol) != sol:
                return i
        return -1  # if this happens, there's an error

    def is_integer_solution(self):
        for xi in self.relaxation.get_solution():
            if int(xi) != xi:
                return False
        return True

    def __str__(self):
        string = " - Infeasible"
        if self.relaxation.is_feasible():
            string = " - " + str(self.relaxation.get_bound()) + " - " + str(self.relaxation.get_solution()) \
                     + " - " + str(self.relaxation.get_dual()) + " - " + str(self.relaxation.get_reduced_cost())
        parent = " from " + (str(self.parent_node.number) if self.parent_node is not None else "N")
        return "Node " + str(self.number) + parent + string


class BranchAndBound:

    def __init__(self, relaxation: Relaxation, node_selection="FIFO", heuristic_initialization=False):
        self.heuristic_initialization = heuristic_initialization
        self.available_nodes = [Node(0, None, relaxation)]
        self.best_lower_bound_value = None
        self.best_lower_bound_solution = None
        self.node_selection = node_selection

    """
        Doctest not configure here. TODO how to do it?
        >>> lp = LinearProgramInstance()
        >>> branch_and_bound = BranchAndBound(lp)
        >>> branch_and_bound.execute()
        >>> branch_and_bound.best_lower_bound_solution
        [1.0, 3.0]
    """
    def execute(self):
        finalize = self.initialize()
        while not finalize:
            next_node = self.select_node()
            if not self.prune(next_node):
                self.branch(next_node)
            finalize = not self.available_nodes  # check if it's an empty list

    def initialize(self):
        root = self.available_nodes.pop()
        root.execute()
        if root.is_integer_solution():
            return True
        if self.heuristic_initialization:
            self.heuristic_integer_solution(root)
        self.branch(root)
        return False

    def heuristic_integer_solution(self, root):
        # integer_solution = []
        # for value in root.relaxation.get_solution():
        #     integer_solution.append(float(round(value)))
        # self.best_lower_bound_solution = integer_solution
        # self.best_lower_bound_value = root.relaxation.evaluate_solution(integer_solution)
        pass

    """
    There's many ways to select a node, here is just a simple one
    """
    def select_node(self):
        return self.available_nodes.pop(0 if self.node_selection == "FIFO" else
                                        -1 if self.node_selection == "LIFO" else -1)

    """
    :return Should branch?
    """
    def prune(self, node):
        node.execute()
        "prune by infeasibility"
        if not node.relaxation.is_feasible():
            return True
        "prune by bound"
        objective_value = node.relaxation.get_bound()
        if self.best_lower_bound_value is not None and objective_value <= self.best_lower_bound_value:
            return True
        "prune by integrality"
        if node.is_integer_solution():
            self.best_lower_bound_value = objective_value
            self.best_lower_bound_solution = node.relaxation.get_solution()
            return True
        return False

    """
    variable branching strategy
    """
    def branch(self, parent_node):
        solution = parent_node.relaxation.get_solution()
        i = parent_node.choose_variable()
        relaxation1 = copy.deepcopy(parent_node.relaxation)
        relaxation1.add_upper_bound(i, math.floor(solution[i]))
        self.available_nodes.append(Node(parent_node.number + 1, parent_node, relaxation1))
        relaxation2 = copy.deepcopy(parent_node.relaxation)
        relaxation2.add_lower_bound(i, math.ceil(solution[i]))
        self.available_nodes.append(Node(parent_node.number + 2, parent_node, relaxation2))


if __name__ == '__main__':
    import pyomo.environ as pe
    import pyomo as pyo
    import logging


    class LinearProgramInstance(Relaxation):

        def __init__(self):
            logging.getLogger('pyomo.core').setLevel(logging.ERROR)
            self.solver = pyo.opt.SolverFactory('cbc')
            self.results = "NotExecuted"
            self.model = pe.ConcreteModel()
            self.model.J = [0, 1]
            self.model.x = pe.Var(self.model.J, domain=pe.NonNegativeReals)
            self.cost_vector = [5.5, 2.1]
            self.model.obj = pe.Objective(expr=sum(self.cost_vector[i] * self.model.x[i]
                                                   for i in self.model.J), sense=pe.maximize)
            self.model.dual = pe.Suffix(direction=pe.Suffix.IMPORT)
            self.model.rc = pe.Suffix(direction=pe.Suffix.IMPORT_EXPORT)
            self.model.constraints = pe.ConstraintList()
            # self.model.constraints.add(expr=6.7*self.model.x[0] + 2 * self.model.x[1] <= 17)
            # self.model.constraints.add(expr=-2.5*self.model.x[0] + self.model.x[1] <= 2)
            self.model.constraint_row1 = pe.Constraint(expr=8*self.model.x[0] + 2 * self.model.x[1] <= 17)
            self.model.constraint_row2 = pe.Constraint(expr=-self.model.x[0] + self.model.x[1] <= 2)

        def add_upper_bound(self, var_index, bound_value):
            self.model.constraints.add(self.model.x[var_index] <= bound_value)

        def add_lower_bound(self, var_index, bound_value):
            self.model.constraints.add(self.model.x[var_index] >= bound_value)

        def execute(self):
            self.results = self.solver.solve(self.model)
            # self.model.display()
            # self.model.dual.display()
            # self.model.rc.display()

        def is_feasible(self):
            return self.results.solver.status == pyo.opt.SolverStatus.ok

        def get_bound(self):
            return self.model.obj()

        def get_solution(self):
            return [self.model.x[j]() for j in self.model.J]

        def evaluate_solution(self, solution):
            return sum(self.cost_vector[i] * solution[i] for i in self.model.J)

        def get_dual(self):
            duals_by_constraint = {}
            for constraints in self.model.component_objects(pe.Constraint, active=True):
                if constraints.name != "constraints":
                    duals_by_constraint[constraints.name] = self.model.dual[constraints]
            return duals_by_constraint

        def get_reduced_cost(self):
            rc = {}
            for var in self.model.component_objects(pe.Var, active=True):
                for i in var:
                    rc[var[i].name] = self.model.rc[var[i]]
            return rc


    lp = LinearProgramInstance()
    branch_and_bound = BranchAndBound(lp, node_selection="LIFO",  heuristic_initialization=False)
    branch_and_bound.execute()
    print("Result:", "x = ", branch_and_bound.best_lower_bound_solution,
          " obj(x) = ", branch_and_bound.best_lower_bound_value)