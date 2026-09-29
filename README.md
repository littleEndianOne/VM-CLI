# VM CLI

Build the command-line VM with GNU Make and GCC:

```sh
make
```

The executable is written to `build/vm-cli`. Run a VM program with:

```sh
make run PROGRAM=VM_CLI/TestCodeFiles/addition.vm
```

Use `make clean` to remove generated build artifacts.
