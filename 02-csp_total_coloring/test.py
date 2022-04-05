import constraint

problem = constraint.Problem()
problem.addVariable("a", [1,2,3])
problem.addVariable("b", [4,5,6])
problem.getSolutions()
print(problem.getSolutions())

problem.addConstraint(lambda a, b: a*2 == b,("a", "b"))
print(problem.getSolutions())

problem = constraint.Problem()
problem.addVariables(["a", "b"], [1, 2, 3])
problem.addConstraint(constraint.AllDifferentConstraint())

print(problem.getSolutions())