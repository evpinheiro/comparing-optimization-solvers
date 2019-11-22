import pyomo.opt
import pyomo.environ as pe


class Node(object):
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        return str(self.code)


class Arc:
    def __init__(self, source: Node, destination: Node, upper_bound: int):
        self.source = source
        self.destination = destination
        self.capacity = upper_bound

    def __str__(self):
        return str(self.source) + "-" + str(self.destination)


class Graph:
    def __init__(self, commodity_name, nodes: dict, arcs: dict):
        self.commodity_name = commodity_name
        self.arcs_cost_cap = arcs
        self.nodes_demands = nodes


def multicommodity_minimum_cost_flow(graphs: list, common_arcs: list, integer: bool):
    modelo = pe.ConcreteModel(name="MCFP")

    modelo.dual = pe.Suffix(direction=pe.Suffix.IMPORT)

    commodities_arcs = {(graph_k.commodity_name, str(arc[0])):
                            arc for graph_k in graphs for arc in graph_k.arcs_cost_cap.items()}
    modelo.var_indexes = commodities_arcs.keys()
    modelo.var = pe.Var(modelo.var_indexes, within=pe.NonNegativeIntegers if integer else pe.NonNegativeReals)

    def objetivo(m):
        return sum(commodities_arcs[index][1][0] * m.var[index] for index in modelo.var_indexes)

    modelo.obj = pe.Objective(rule=objetivo, sense=pe.minimize)

    commodities_nodes = [(commodity, node) for commodity in graphs for node in commodity.nodes_demands.items()]

    def conserva_fluxo(m, index):
        commodity, node = commodities_nodes[index]
        from_i = [str(arc) for arc in commodity.arcs_cost_cap.keys() if arc.source == node[0]]
        to_i = [str(arc) for arc in commodity.arcs_cost_cap.keys() if arc.destination == node[0]]
        return sum(m.var[(commodity.commodity_name, v)] for v in from_i) - sum(
            m.var[(commodity.commodity_name, v)] for v in to_i) == node[1]

    modelo.commodities_nodes_indexes = range(len(commodities_nodes))
    modelo.flow_conservation = pe.Constraint(modelo.commodities_nodes_indexes, rule=conserva_fluxo)

    def capacidades_conjuntas(m, index):
        return sum(m.var[(commodity.commodity_name, str(common_arcs[index]))] for commodity in graphs) <= common_arcs[
            index].capacity

    modelo.capacidade_conjunta_arco = pe.Constraint(range(len(common_arcs)), rule=capacidades_conjuntas)

    def capacidades(m, commodity, arc):
        var_index = (commodity, arc)
        return m.var[var_index] <= commodities_arcs.get(var_index)[1][1]

    modelo.capacidade = pe.Constraint(modelo.var_indexes, rule=capacidades)

    solver = pyomo.opt.SolverFactory('cbc')
    results = solver.solve(modelo)
    modelo.display()
    # modelo.pprint()


node_s1 = Node('s1')
node_t1 = Node('t1')
node_s2 = Node('s2')
node_t2 = Node('t2')

arc_s1_t2 = Arc(node_s1, node_t2, 25)
arc_s1_t1 = Arc(node_s1, node_t1, 25)
arc_t2_s2 = Arc(node_t2, node_s2, 25)
arc_s2_s1 = Arc(node_s2, node_s1, 25)
arc_s2_t1 = Arc(node_s2, node_t1, 25)
arc_t1_t2 = Arc(node_t1, node_t2, 25)

graph_1 = Graph('1', {node_s1: 5, node_t1: -5, node_s2: 0, node_t2: 0},
                {arc_s1_t2: (1, 15), arc_s1_t1: (4, 15), arc_t2_s2: (1, 15),
                 arc_s2_s1: (1, 15), arc_s2_t1: (1, 15), arc_t1_t2: (1, 15)})
graph_2 = Graph('2', {node_s1: 0, node_t1: 0, node_s2: 5, node_t2: -5},
                {arc_s1_t2: (1, 15), arc_s1_t1: (1, 15), arc_t2_s2: (1, 15),
                 arc_s2_s1: (1, 15), arc_s2_t1: (1, 15), arc_t1_t2: (1, 15)})

graph_list = [graph_1, graph_2]

multicommodity_minimum_cost_flow(graph_list,
                                 [arc_s1_t2, arc_s1_t1, arc_t2_s2, arc_s2_s1, arc_s2_t1, arc_t1_t2],
                                 True)

# arc12 = Arc(node1, node2, 5)
# arc14 = Arc(node1, node4, 5)
# arc23 = Arc(node2, node3, 5)
# arc31 = Arc(node3, node1, 5)
# arc42 = Arc(node4, node2, 5)
# arc43 = Arc(node4, node3, 5)
#
# graph_32 = Graph('3-2', {node1: 0, node2: -4, node3: 4, node4: 0},
#                  {arc12: (2, 5), arc14: (1, 5), arc23: (1, 5), arc31: (1, 5), arc43: (1, 5), arc42: (1, 5)})
# graph_13 = Graph('1-3', {node1: 4, node2: 0, node3: -4, node4: 0},
#                  {arc12: (1, 5), arc14: (2, 5), arc23: (1, 5), arc31: (1, 5), arc43: (2, 5), arc42: (4, 5)})
# graph_24 = Graph('2-4', {node1: 0, node2: 1, node3: 0, node4: -1},
#                  {arc12: (1, 5), arc14: (2, 5), arc23: (1, 5), arc31: (1, 5), arc43: (2, 5), arc42: (4, 5)})

# graph_list = [graph_32, graph_13, graph_24]


# s1 = Node('s1')
# t1 = Node('t1')
# s2 = Node('s2')
# t2 = Node('t2')
# node1 = Node(1)
# node2 = Node(2)
# node3 = Node(3)
# node4 = Node(4)
#
# arc_s1_1 = Arc(s1, node1, 1)
# arc_1_2 = Arc(node1, node2, 1)
# arc_2_t2 = Arc(node2, t2, 1)
# arc_1_3 = Arc(node1, node3, 1)
# arc_3_2 = Arc(node3, node2, 1)
# arc_3_t1 = Arc(node3, t1, 1)
# arc_4_3 = Arc(node4, node3, 1)
# arc_4_1 = Arc(node4, node1, 1)
# arc_2_4 = Arc(node2, node4, 1)
# arc_s2_4 = Arc(s2, node4, 1)
#
# graph_1 = Graph('s1-t1', {s1: 1, t1: -1, s2: 0, t2: 0, node1: 0, node2: 0, node3: 0, node4: 0},
#                 {arc_s1_1: (1, 5), arc_1_2: (1, 5), arc_2_t2: (1, 5), arc_1_3: (5, 5), arc_3_2: (1, 5),
#                  arc_3_t1: (1, 5), arc_4_3: (1, 5), arc_4_1: (1, 5), arc_2_4: (1, 5), arc_s2_4: (1, 5)})
# graph_2 = Graph('s2-t2', {s1: 0, t1: 0, s2: 1, t2: -1, node1: 0, node2: 0, node3: 0, node4: 0},
#                 {arc_s1_1: (1, 5), arc_1_2: (1, 5), arc_2_t2: (1, 5), arc_1_3: (1, 5), arc_3_2: (1, 5),
#                  arc_3_t1: (1, 5), arc_4_3: (1, 5), arc_4_1: (1, 5), arc_2_4: (1, 5), arc_s2_4: (1, 5)})
