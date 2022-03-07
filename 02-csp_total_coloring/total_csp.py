# Install package python-constraint, not constraint !!!
import constraint
import networkx

def total_coloring(graph):
    """
        Find total chromatic index and total coloring.
        graph - instance of networkx.Graph
        returns - total chromatic index x
        Furthermore, assign property "color" for every vertex and edge. The value of the color has to be an integer between 0 and x-1.

        TODO: The implementation of this function finds some total coloring but the number of colors may not be minimal.
        Find the total chromatic index.

        colors = 0
        for u in graph.nodes():
            graph.nodes[u]["color"] = colors
            colors += 1
        for u,v in graph.edges():
            graph.edges[u,v]["color"] = colors
            colors += 1
        return colors
    """
    # http://labix.org/doc/constraint/
    solutution = None
    for colors in range(1, 100):
        problem = constraint.Problem()

        # Add variables for vertices
        for v in graph.nodes():
            problem.addVariable(get_vrtx_name(v), range(0, colors))

        # Add variables for edges
        edges = {}
        edge = 1000
        for u,v in graph.edges():
            problem.addVariable(edge, range(0, colors))
            edges[get_edge_name(u,v)] = edge
            edges[get_edge_name(v,u)] = edge
            edge = edge + 1

        # Add constrains
        for u,v in graph.edges():
            # Conected vertices
            problem.addConstraint(lambda c1, c2: c1 != c2, (get_vrtx_name(u), get_vrtx_name(v)))

            # Edge its and vertices
            problem.addConstraint(lambda c1, c2: c1 != c2, (get_vrtx_name(v), edges[get_edge_name(u,v)]))

            for n in graph.neighbors(u):
                if n != v:
                    problem.addConstraint(lambda c1, c2: c1 != c2, (edges[get_edge_name(u,n)], edges[get_edge_name(u,v)]))
            
            for n in graph.neighbors(v):
                if n != u:
                    problem.addConstraint(lambda c1, c2: c1 != c2, (edges[get_edge_name(v,n)], edges[get_edge_name(u,v)]))

       
        solutution = problem.getSolution()
        if solutution is not None: break
    
    print("Colors:", colors)
    print("Solution:", solutution)
    
    if solutution is not None:
        # Apply coloring
        for v in graph.nodes():
            graph.nodes[v]["color"] = solutution[get_vrtx_name(v)]
        for u,v in graph.edges():
            graph.edges[u,v]["color"] = solutution[edges[get_edge_name(u,v)]]

    return colors

   
def get_vrtx_name(u): return u
def get_edge_name(u, v): return str(u) + "-" + str(v)
