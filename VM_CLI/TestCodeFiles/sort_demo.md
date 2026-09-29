# VM CLI sorting demonstration

`sort_demo.vm` is a self-contained bytecode program that bubble-sorts the ten
integers `42, 7, 19, 3, 88, 1, 56, 24, 11, 5` in ascending order.

```sh
make run PROGRAM=VM_CLI/TestCodeFiles/sort_demo.vm
```

It allocates a global array, uses global variables for loop indices and the
swap temporary, and performs conditional jumps for the bubble-sort loops. The
expected result is:

```text
Sorted values: 1 3 5 7 11 19 24 42 56 88
```

The CLI container header specifies start program counter `0` and four global
variables. Regenerate the checked-in bytecode after editing its generator:

```sh
python3 VM_CLI/TestCodeFiles/create_sort_demo.py
```
