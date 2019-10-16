import pyomo.environ as pe
import pyomo as pyo
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

    def get_solution(self):
        pass


class Node:

    def __init__(self, number, parent_node, relaxation: Relaxation):
        self.number = number
        self.parent_node = parent_node
        self.relaxation = relaxation
        # self.variables = []

    def execute(self):
        self.relaxation.execute()

    # def next_node(self, direction):
    #     pass

    def __str__(self):
        string = " - Infeasible"
        if self.relaxation.is_feasible():
            string = " - " + str(self.relaxation.get_bound()) + " - " + str(self.relaxation.get_solution())
        return str(self.number) + string


class BranchAndBound:

    def __init__(self, relaxation: Relaxation):
        self.available_nodes = [Node(0, None, relaxation)]
        self.best_lower_bound_value = None
        self.best_lower_bound_solution = None

    def execute(self):
        while not not self.available_nodes:
            next_node = self.select_node()
            if not self.prune(next_node):
                self.branch(next_node)

    """
    There's many ways to select a node, here is just a simple one
    """

    def select_node(self):
        return self.available_nodes.pop(0)

    """
    :return Should branch?
    """

    def prune(self, node):
        node.relaxation.execute()
        print(node)
        "prune by infeasibility"
        if not node.relaxation.is_feasible():
            return True
        "prune by bound"
        objective_value = node.relaxation.get_bound()
        if self.best_lower_bound_value is not None and objective_value <= self.best_lower_bound_value:
            return True
        "prune by integrality"
        optimal_solution = node.relaxation.get_solution()
        if self.is_integer_vector(optimal_solution):
            self.best_lower_bound_value = objective_value
            self.best_lower_bound_solution = optimal_solution
            return True
        return False

    """
    variable branching
    """
    def branch(self, parent_node):
        solution = parent_node.relaxation.get_solution()
        i = self.choose_variable(solution)
        relaxation1 = copy.deepcopy(parent_node.relaxation)
        relaxation1.add_upper_bound(i, math.floor(solution[i]))
        self.available_nodes.append(Node(parent_node.number + 1, parent_node, relaxation1))
        relaxation2 = copy.deepcopy(parent_node.relaxation)
        relaxation2.add_lower_bound(i, math.ceil(solution[i]))
        self.available_nodes.append(Node(parent_node.number + 2, parent_node, relaxation2))

    def choose_variable(self, solution):
        for i, sol in enumerate(solution):
            if int(sol) != sol:
                return i
        return -1  # if this happens, there's an error

    def is_integer_vector(self, optimal_solution):
        for xi in optimal_solution:
            if int(xi) != xi:
                return False
        return True


if __name__ == '__main__':
    class LinearProgramInstance(Relaxation):

        def __init__(self):
            self.solver = pyo.opt.SolverFactory('cbc')
            self.upper_bound = [None, None]
            self.lower_bound = [None, None]
            self.results = "NotExecuted"
            self.model = None

        def add_upper_bound(self, var_index, bound_value):
            self.upper_bound[var_index] = bound_value

        def add_lower_bound(self, var_index, bound_value):
            self.lower_bound[var_index] = bound_value

        def obj_rule(self, model):
            return 5.5 * model.x1 + 2.1 * model.x2

        def constraint1_rule(self, model):
            return -model.x1 + model.x2 <= 2

        def constraint2_rule(self, model):
            return 8 * model.x1 + 2 * model.x2 <= 17

        def execute(self):
            self.model = pe.ConcreteModel()
            self.model.x1 = pe.Var(domain=pe.NonNegativeReals, bounds=(self.lower_bound[0], self.upper_bound[0]))
            self.model.x2 = pe.Var(domain=pe.NonNegativeReals, bounds=(self.lower_bound[1], self.upper_bound[1]))
            self.model.obj = pe.Objective(rule=self.obj_rule, sense=pe.maximize)
            self.model.constraint1 = pe.Constraint(rule=self.constraint1_rule)
            self.model.constraint2 = pe.Constraint(rule=self.constraint2_rule)
            self.results = self.solver.solve(self.model)

        def is_feasible(self):
            return self.results.solver.status == pyo.opt.SolverStatus.ok

        def get_bound(self):
            return self.model.obj()

        def get_solution(self):
            return [self.model.x1(), self.model.x2()]

    lp = LinearProgramInstance()
    branch_and_bound = BranchAndBound(lp)
    branch_and_bound.execute()
    x = branch_and_bound.best_lower_bound_solution
    z = branch_and_bound.best_lower_bound_value
