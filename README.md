# VM CLI

## Related projects

- [Assembler](https://github.com/littleEndianOne/Assembler) converts source programs into the bytecode files executed by this CLI.
- [virtual-machine](https://github.com/littleEndianOne/virtual-machine) provides the C virtual-machine implementation used by this CLI.

Build the command-line VM with GNU Make and GCC:

```sh
make
```

The executable is written to `build/vm-cli`. Run a VM program with:

```sh
make run PROGRAM=VM_CLI/TestCodeFiles/addition.vm
```

Use `make clean` to remove generated build artifacts.

## Bytecode demonstration programs

The self-contained programs below are in
[`VM_CLI/TestCodeFiles`](VM_CLI/TestCodeFiles). They do not need command-line
input beyond the file path supplied by `make run`, and each terminates with the
VM `HALT` instruction.

| Program | Location | What it demonstrates | Run it |
| --- | --- | --- | --- |
| General VM demo | [`demo.vm`](VM_CLI/TestCodeFiles/demo.vm) | Inline output; integer and floating-point arithmetic; global variables; string construction; a summation loop; array access; conditional branching; and a function call. It prints the results of each calculation. | `make run PROGRAM=VM_CLI/TestCodeFiles/demo.vm` |
| Bubble-sort demo | [`sort_demo.vm`](VM_CLI/TestCodeFiles/sort_demo.vm) | Sorting the unordered integers `42, 7, 19, 3, 88, 1, 56, 24, 11, 5` into ascending order using a global array, loop counters, comparisons, conditional jumps, and element swaps. | `make run PROGRAM=VM_CLI/TestCodeFiles/sort_demo.vm` |

The checked-in `.vm` files are executable bytecode. Their companion
documentation describes expected output and their Python generators can
regenerate them after changes:

```sh
python3 VM_CLI/TestCodeFiles/create_demo.py
python3 VM_CLI/TestCodeFiles/create_sort_demo.py
```

See [`demo.md`](VM_CLI/TestCodeFiles/demo.md) and
[`sort_demo.md`](VM_CLI/TestCodeFiles/sort_demo.md) for the complete program
details.
