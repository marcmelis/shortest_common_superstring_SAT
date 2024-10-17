import time
import argparse

from pysat.solvers import Solver


def solve(strings, max_len):
    '''
    Solves SCS for the strings for a maximum length of max_len
    '''
    alphabet = sorted(set(''.join(strings)))

    n = len(strings)  # number of strings
    k = max_len       # maximum possible length of the superstring
    m = len(alphabet) # size of the alphabet

    solver = Solver(name="g3")

    # this two dictionaries map from the tuple (2,3) to the actual constant 34
    x = {}
    y = {}
    var_count = 1

    # building variables for x matrix
    for i in range(k):
        for j in range(m):
            x[(i, j)] = var_count
            var_count += 1

    # building variables for y matrix
    for i in range(n):
        for j in range(k - len(strings[i]) + 1):
            y[(i, j)] = var_count
            var_count += 1

    # clauses 1
    for i in range(k):
        solver.add_clause([x[(i, j)] for j in range(m)])

    # clauses 2
    for i in range(k):
        for j1 in range(m):
            for j2 in range(j1 + 1, m):
                solver.add_clause([-x[(i, j1)], -x[(i, j2)]])

    # clauses 3
    for i, string in enumerate(strings):
        valid_positions = [y[(i, j)] for j in range(k - len(string) + 1)]
        solver.add_clause(valid_positions)

    # clauses 4
    for i, string in enumerate(strings):
        for j1 in range(k - len(string) + 1):
            for j2 in range(j1 + 1, k - len(string) + 1):
                solver.add_clause([-y[(i, j1)], -y[(i, j2)]])

    # clauses 5
    for i, string in enumerate(strings):
        for j in range(k - len(string) + 1):
            for s in range(j, j + len(string)):
                char_index = alphabet.index(string[s - j])
                for t in range(m):
                    if t != char_index:
                        solver.add_clause([-y[(i, j)], -x[(s, t)]])

    if solver.solve():
        model = solver.get_model()
        result = [''] * k
        for i in range(k):
            for j in range(m):
                if model[x[(i, j)] - 1] > 0:
                    result[i] = alphabet[j]
                    break
        return ''.join(result).strip()
    else:
        return None

def levenshtein_distance(str1, str2):
    m = len(str1)
    n = len(str2)

    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],
                                   dp[i][j - 1],
                                   dp[i - 1][j - 1])

    return dp[m][n]


if __name__ == '__main__':

    original_solution = None

    parser = argparse.ArgumentParser(description="Shortest Common Superstring Solver")
    parser.add_argument('-i', '--input', type=str, default="input.txt", help="Input file containing strings separated by newlines")
    parser.add_argument('-s', '--solution', type=str, default="solution.txt", help="Original solution file for comparison (optional)")
    args = parser.parse_args()

    input_file = args.input
    solution_file = args.solution

    try:
        with open(input_file, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Missing input file, use: python scs_SAT.py -i <inputfilename>.")
        exit(-1)

    try:
        with open(solution_file, "r") as file:
            original_solution = file.read().split('\n')[0]
    except FileNotFoundError:
        print(f"Solution file '{solution_file}' not found. Skipping comparison.")

    strings = []
    for string in content.split('\n'):
        if string:
            strings.append(string)


    # BINARY SEARCH FOR k
    k = len(''.join(strings))
    upper_bound = k
    lower_bound = max([len(string) for string in strings])
    best_superstring = None
    start_time = time.time()

    while upper_bound > lower_bound + 1:
        k = (upper_bound + lower_bound) // 2
        print(f"Trying for {k} length")
        superstring = solve(strings, k)
        if superstring:
            best_superstring = superstring
            upper_bound = k
        else:
            lower_bound = k

    end_time = time.time()

    with open("output.txt", "w") as file:
        file.write(best_superstring)

    print(f"\nThe shortest common superstring has length {upper_bound} and is:\n{best_superstring}")
    if original_solution:
        print(f"The original sequence was:\n{original_solution}\n")
        distance = levenshtein_distance(original_solution, best_superstring)
        print(f"Levenshtein distance: {distance}")

    print(f"\nExecution time: {end_time-start_time:.3} s")
