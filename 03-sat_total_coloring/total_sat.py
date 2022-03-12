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

   
    # Find minimal chromatic number
    g = None
    solved = False
    colors = max_deg + 1
    while not solved:
        # Asign unique ints to nodes and edges
        variables = {}
        nodes = {}
        i = 1
        for u in graph.nodes():
            nodes[get_node_name(u)] = {}
            for color in range(1, colors + 1):
                nodes[get_node_name(u)][color] = i
                variables[i] = ("node", u, color)
                i = i + 1
        edges = {}
        for u,v in graph.edges():
            edges[get_edge_name(u, v)] = {}
            edges[get_edge_name(v, u)] = {}
            for color in range(1, colors + 1):
                edges[get_edge_name(u, v)][color] = i
                edges[get_edge_name(v, u)][color] = i
                variables[i] = ("edge", (u, v), color)
                i = i + 1
        
        # Init solver
        g = Glucose3()
        
        # Nodes
        for node in nodes:
            # Each node has at least one color           
            g.add_clause(range(nodes[node][1], nodes[node][1] + colors))

            # Each node has at most one color
            """
            for color1 in nodes[node]:
                for color2 in nodes[node]:
                    if color1 != color2:
                        g.add_clause([-nodes[node][color1], -nodes[node][color2]])
            """

        # Edges
        for edge in edges:
            # Each edge has at least one color
            g.add_clause(range(edges[edge][1], edges[edge][1] + colors))

            # Each edge has at most one color
            """
            for color1 in edges[edge]:
                for color2 in edges[edge]:
                    if color1 != color2:
                        g.add_clause([-edges[edge][color1], -edges[edge][color2]])
            """

        # Diff colors
        for u,v in graph.edges():
            for color in range(1, colors + 1):
                 # Contected nodes have diff color
                g.add_clause([-nodes[get_node_name(u)][color], -nodes[get_node_name(v)][color]])

                # Edge its and nodes have diff color
                g.add_clause([-edges[get_edge_name(u, v)][color], -nodes[get_node_name(u)][color]])
                g.add_clause([-edges[get_edge_name(u, v)][color], -nodes[get_node_name(v)][color]])

                # Edges sharing common nodes
                for n in graph.neighbors(u):
                    if n != v:
                        g.add_clause([-edges[get_edge_name(u, n)][color], -edges[get_edge_name(u, v)][color]])
                for n in graph.neighbors(v):
                    if n != u:
                        g.add_clause([-edges[get_edge_name(v, n)][color], -edges[get_edge_name(u, v)][color]])
        
        # Try solve
        solved = g.solve()
        if solved: break
        else: colors = colors + 1

    if solved:
        # Get model
        model = g.get_model()

        # Color graph
        for var in model:
            if var > 0:
                element = variables[var]  
                if element[0] == "node":
                    graph.nodes[element[1]]["color"] = element[2] - 1
                elif element[0] == "edge":
                    graph.edges[element[1][0], element[1][1]]["color"] = element[2] - 1
            
    return colors

    

def get_node_name(u): return u
def get_edge_name(u, v): return str(u) + "-" + str(v)


