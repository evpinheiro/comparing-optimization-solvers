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
            string = " - " + str(self.relaxation.get_bound()) + " - " + str(self.relaxation.get_solution())
        parent = " from " + (str(self.parent_node.number) if self.parent_node is not None else "N")
        return "Node " + str(self.number) + parent + string


class BranchAndBound:

    def __init__(self, relaxation: Relaxation, node_selection="FIFO"):
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
        while not not self.available_nodes:
            next_node = self.select_node()
            if not self.prune(next_node):
                self.branch(next_node)

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
        relaxation1.add_upper_bound(i + 1, math.floor(solution[i]))
        self.available_nodes.append(Node(parent_node.number + 1, parent_node, relaxation1))
        relaxation2 = copy.deepcopy(parent_node.relaxation)
        relaxation2.add_lower_bound(i + 1, math.ceil(solution[i]))
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
            self.model.x = pe.Var([1, 2], domain=pe.NonNegativeReals)
            self.model.obj = pe.Objective(expr=5.5 * self.model.x[1] + 2.1 * self.model.x[2], sense=pe.maximize)
            self.model.c = pe.ConstraintList()
            self.model.c.add(expr=8 * self.model.x[1] + 2 * self.model.x[2] <= 17)
            self.model.c.add(expr=-self.model.x[1] + self.model.x[2] <= 2)

        def add_upper_bound(self, var_index, bound_value):
            self.model.c.add(self.model.x[var_index] <= bound_value)

        def add_lower_bound(self, var_index, bound_value):
            self.model.c.add(self.model.x[var_index] >= bound_value)

        def execute(self):
            self.results = self.solver.solve(self.model)

        def is_feasible(self):
            return self.results.solver.status == pyo.opt.SolverStatus.ok

        def get_bound(self):
            return self.model.obj()

        def get_solution(self):
            return [self.model.x[1](), self.model.x[2]()]

    lp = LinearProgramInstance()
    branch_and_bound = BranchAndBound(lp, node_selection="FIFO")
    branch_and_bound.execute()
    branch_and_bound.best_lower_bound_solution
