#!/usr/bin/env python3
"""Generate a VM bytecode program that bubble-sorts ten integers."""

from pathlib import Path


OP = {
    "CONSTI8": 16,
    "STRLIT": 19,
    "ADDI": 28,
    "LTI": 33,
    "GTI": 34,
    "JMP": 36,
    "JMPT": 37,
    "JMPF": 38,
    "GSTORE": 48,
    "GLOAD": 49,
    "GDARRAY": 56,
    "GSTOREAE": 57,
    "GLOADAE": 58,
    "HALT": 255,
    "PRINT": 254,
}


class Program:
    def __init__(self):
        self.code = bytearray()
        self.labels = {}
        self.addresses = []

    def emit(self, opcode, *operands):
        self.code.append(OP[opcode])
        self.code.extend(operands)

    def string(self, text):
        encoded = text.encode("ascii")
        if len(encoded) > 255:
            raise ValueError("String literal exceeds the VM's 255-byte limit")
        self.emit("STRLIT", len(encoded))
        self.code.extend(encoded)
        self.code.append(0)

    def label(self, name):
        self.labels[name] = len(self.code)

    def address(self, opcode, label, *operands):
        self.emit(opcode, 0, 0, *operands)
        self.addresses.append((len(self.code) - len(operands) - 2, label))

    def resolve(self):
        for offset, label in self.addresses:
            address = self.labels[label]
            self.code[offset] = address & 0xFF
            self.code[offset + 1] = address >> 8


ARRAY = 0
OUTER = 1
INNER = 2
TEMP = 3

program = Program()
program.string("Bubble sort: 42 7 19 3 88 1 56 24 11 5\n")
program.emit("PRINT")

program.emit("GDARRAY", 10, ARRAY)
for index, value in enumerate((42, 7, 19, 3, 88, 1, 56, 24, 11, 5)):
    program.emit("CONSTI8", value)
    program.emit("CONSTI8", index)
    program.emit("GSTOREAE", ARRAY)

program.emit("CONSTI8", 0)
program.emit("GSTORE", OUTER)
program.label("outer_loop")
program.emit("GLOAD", OUTER)
program.emit("CONSTI8", 9)
program.emit("LTI")
program.address("JMPF", "print_values")

program.emit("CONSTI8", 0)
program.emit("GSTORE", INNER)
program.label("inner_loop")
program.emit("GLOAD", INNER)
program.emit("GLOAD", OUTER)
program.emit("ADDI")
program.emit("CONSTI8", 9)
program.emit("LTI")
program.address("JMPF", "advance_outer")

# Swap adjacent values when array[inner] is greater than array[inner + 1].
program.emit("GLOAD", INNER)
program.emit("GLOADAE", ARRAY)
program.emit("GLOAD", INNER)
program.emit("CONSTI8", 1)
program.emit("ADDI")
program.emit("GLOADAE", ARRAY)
program.emit("GTI")
program.address("JMPF", "advance_inner")

program.emit("GLOAD", INNER)
program.emit("GLOADAE", ARRAY)
program.emit("GSTORE", TEMP)

program.emit("GLOAD", INNER)
program.emit("CONSTI8", 1)
program.emit("ADDI")
program.emit("GLOADAE", ARRAY)
program.emit("GLOAD", INNER)
program.emit("GSTOREAE", ARRAY)

program.emit("GLOAD", TEMP)
program.emit("GLOAD", INNER)
program.emit("CONSTI8", 1)
program.emit("ADDI")
program.emit("GSTOREAE", ARRAY)

program.label("advance_inner")
program.emit("GLOAD", INNER)
program.emit("CONSTI8", 1)
program.emit("ADDI")
program.emit("GSTORE", INNER)
program.address("JMP", "inner_loop")

program.label("advance_outer")
program.emit("GLOAD", OUTER)
program.emit("CONSTI8", 1)
program.emit("ADDI")
program.emit("GSTORE", OUTER)
program.address("JMP", "outer_loop")

program.label("print_values")
program.string("Sorted values: ")
program.emit("PRINT")
program.emit("CONSTI8", 0)
program.emit("GSTORE", INNER)
program.label("print_loop")
program.emit("GLOAD", INNER)
program.emit("CONSTI8", 10)
program.emit("LTI")
program.address("JMPF", "done")
program.emit("GLOAD", INNER)
program.emit("GLOADAE", ARRAY)
program.emit("PRINT")
program.string(" ")
program.emit("PRINT")
program.emit("GLOAD", INNER)
program.emit("CONSTI8", 1)
program.emit("ADDI")
program.emit("GSTORE", INNER)
program.address("JMP", "print_loop")

program.label("done")
program.string("\n")
program.emit("PRINT")
program.emit("HALT")
program.resolve()

# The CLI consumes a two-byte container header before loading VM code.
output = Path(__file__).with_name("sort_demo.vm")
output.write_bytes(bytes((0, 4)) + program.code)
