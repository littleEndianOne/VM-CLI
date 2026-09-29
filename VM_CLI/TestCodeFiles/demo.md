# VM CLI bytecode demonstration

`demo.vm` is a self-contained VM program: it needs no input and terminates with
`HALT`. Run it with:

```sh
make run PROGRAM=VM_CLI/TestCodeFiles/demo.vm
```

It demonstrates string literals and inline output, integer and floating-point
arithmetic, global variables, string construction, a loop and conditional
jump, global arrays, and a one-argument function call.

The file begins with the CLI's two-byte container header: start program counter
`0`, followed by global variable count `4`. `create_demo.py` generates the
checked-in bytecode from the opcode values declared in `VM_CLI/VM/vm_common.h`.
Regenerate it after modifying the script:

```sh
python3 VM_CLI/TestCodeFiles/create_demo.py
```

Expected program output, after the CLI banner, is:

```text
VM CLI bytecode demonstration
7 * 6 = 42
22 / 7 = 3.142857
Sum of 1 through 10 = 55
Array element [1] = 8
10 equals 10: true
Square(12) = 144
Done.
```
