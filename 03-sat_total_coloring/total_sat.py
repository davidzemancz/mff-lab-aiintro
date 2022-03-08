# Install package python-sat !!!
from pysat.solvers import Glucose3

def total_coloring(graph):
    """
        Find total chromatic index and total coloring.
        graph - instance of networkx.Graph
        returns - total chromatic index x
        Furthermore, assign property "color" for every vertex and edge. The value of the color has to be an integer between 0 and x-1.

        TODO: The implementation of this function finds some total coloring but the number of colors may be minimal.
        Find the total chromatic index
        
        for u in graph.nodes():
            graph.nodes[u]["color"] = colors
            colors += 1
        for u,v in graph.edges():
            graph.edges[u,v]["color"] = colors
            colors += 1.
    """

    # Get maximum vertex degree
    max_deg = 1
    for v in graph.nodes():
        deg = graph.degree(v)
        if deg > max_deg:
            max_deg = deg

    g = None
    solved = False
    colors = max_deg + 1
    while not solved:
        g = Glucose3()
        #g.add_clause([-1, 2])



        solved = g.solve()
        if solved: break
        else: colors = colors + 1

    if solved:
        model = g.get_model()
    
    return colors

def get_vrtx_name(u): return u
def get_edge_name(u, v): return str(u) + "-" + str(v)


