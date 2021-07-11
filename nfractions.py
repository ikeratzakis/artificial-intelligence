"""Solves the n-Fractions puzzle https://www.csplib.org/Problems/prob041/"""
from constraint import *


# Helper functions to avoid symmetry
# Essentially, we order the fractions
def threesymmetryfunc(a, b, c, d, e, f, g, h, i):
    return a * (10 * e + f) < d * (10 * b + c) and d * (10 * h + i) < g * (10 * e + f)


def twosymmetryfunc(a, b, c, d, e, f):
    return a * (10 * e + f) < d * (10 * b + c)


def foursymmetryfunc(a, b, c, d, e, f, g, h, i, j, k, l):
    return a * (10 * e + f) < d * (10 * b + c) and d * (10 * h + i) < g * (10 * e + f) and g * (10 * k + l) < j * (
            10 * h + i)


# n fraction solver according to n
def nfraction(n, problem):
    print('Solving n fractions problem with n = ', n)
    if n == 3:
        # Create the problem
        problem.addVariables(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        # Instead of dealing with fractions, multiply to avoid floating point rounding errors
        problem.addConstraint(
            lambda A, B, C, D, E, F, G, H, I: A * (10 * E + F) * (10 * H + I) + D * (10 * B + C) * (10 * H + I) + G * (
                    10 * B + C) * (10 * E + F) ==
                                              (10 * B + C) * (10 * E + F) * (10 * H + I), [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
        # Ensure that all digits are different
        problem.addConstraint(AllDifferentConstraint())
        # Avoid symmetry (A < D and D < G)
        problem.addConstraint(threesymmetryfunc, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
        # Get and print the solutions
        solutions = problem.getSolutions()
        print(solutions)
    elif n == 2:
        problem.addVariables(['A', 'B', 'C', 'D', 'E', 'F'], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        problem.addConstraint(
            lambda A, B, C, D, E, F: A * (10 * E + F) + D * (10 * B + C) ==
                                     (10 * B + C) * (10 * E + F), [
                'A', 'B', 'C', 'D', 'E', 'F'])
        problem.addConstraint(AllDifferentConstraint())
        problem.addConstraint(twosymmetryfunc, ['A', 'B', 'C', 'D', 'E', 'F'])
        solutions = problem.getSolutions()
        print(solutions)


def main():
    # Solve problem for n = 2 and n = 3
    for n in range(2, 4):
        problem = Problem()
        nfraction(n=n, problem=problem)


main()
