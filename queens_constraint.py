from constraint import *

# Define the problem
problem = Problem()
n_queens = 5
cols = range(n_queens)
rows = range(n_queens)
problem.addVariables(cols, rows)
for col1 in cols:
    for col2 in cols:
        if col1 < col2:
            # Ensure queens aren't in the same row (row1 != row2), diagonal (abs condition) and column
            problem.addConstraint(lambda row1, row2, col1=col1, col2=col2: abs(row1 - row2) != abs(col1 - col2) and
                                                                           row1 != row2, (col1, col2))

solutions = problem.getSolutions()
print(solutions)
