# Shortest Common Superstring SAT python implementation

This python implementation follows the proposed implementation by [Gorbenko & Popov](https://www.m-hikari.com/ams/ams-2013/ams-45-48-2013/popovAMS45-48-2013-4.pdf).

## SCS_SAT

This script will take the strings from **input.txt**, where each string is separated by a newline (`\n`), and attempt to find the Shortest Common Superstring (SCS) using a SAT solver.

### Requirements

You need to install the `pysat` Python package, which provides the tools for working with SAT solvers.

You can install it using `pip`:

```bash
pip install pysat
```

### Usage

To run the script, you need to pass the following parameters:

- `-i`: the input file with all the strings separated by a newline (`\n`) (default: `input.txt`).
- `-s` (optional): the actual solution if you have it (default: `solution.txt`).

### Example

```bash
python scs_SAT.py -i rna_strings.txt
```

## RNA Random Segment Generator

### Usage

To run the script, you need to pass the following parameters:

- `-n`: The size of the original RNA string (default: 100).
- `-m`: The maximum segment length (default: 20).
- `-s`: The number of segments to generate (default: 60).

### Example

```bash
python rna_gen.py -n 150 -m 25 -s 80
```

In this example:
- The RNA string will have a length of 150 characters.
- The segments extracted will have a maximum length of 25 characters.
- 80 random segments will be generated.

### Output Files

1. **input.txt**: Contains the generated random segments.
2. **solution.txt**: Contains the original RNA string and its length.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
