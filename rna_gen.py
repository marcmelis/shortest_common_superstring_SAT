import random
import argparse


def gen_rand_segment(string):
    n = len(string)
    begining = random.randint(0, n - 1)
    end = min(n, random.randint(0, max_segment_len) + begining)
    return string[begining:end]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate random segments from a RNA string")

    parser.add_argument('-n', type=int, default=100, help='The size of the original string')
    parser.add_argument('-m', type=int, default=20, help='The maximum segment length')
    parser.add_argument('-s', type=int, default=60, help='The number of segments to generate')

    args = parser.parse_args()

    n = args.n
    max_segment_len = args.m
    num_segments = args.s

    rna_dict = {0: 'A', 1: 'G', 2: 'C', 3: 'U'}

    original = ''.join([rna_dict[random.randint(0,3)] for _ in range(n)])
    print(original)

    output = "\n".join([gen_rand_segment(original) for _ in range(num_segments)])

    with open("input.txt", "w") as file:
        file.write(output)

    with open("solution.txt", "w") as file:
        file.write(f"{original}\n{len(original)}\n")
