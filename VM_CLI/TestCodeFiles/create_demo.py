#!/usr/bin/env python3
"""Generate the self-contained VM CLI demonstration bytecode program."""

from pathlib import Path


OP = {
    "CONSTF8": 2,
    "CONSTI8": 16,
    "STRLIT": 19,
    "ADDI": 28,
    "DIVF": 22,
    "MULI": 31,
    "EQI": 32,
    "LTI": 33,
    "JMP": 36,
    "JMPT": 37,
    "CALL": 39,
    "RET": 40,
    "LDARG": 41,
    "GDSTR": 47,
    "GSTORE": 48,
    "GLOAD": 49,
    "GAPPND": 50,
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


program = Program()

program.string("VM CLI bytecode demonstration\n")
program.emit("PRINT")

program.string("7 * 6 = ")
program.emit("PRINT")
program.emit("CONSTI8", 7)
program.emit("CONSTI8", 6)
program.emit("MULI")
program.emit("PRINT")
program.string("\n22 / 7 = ")
program.emit("PRINT")
program.emit("CONSTF8", 22)
program.emit("CONSTF8", 7)
program.emit("DIVF")
program.emit("PRINT")
program.string("\n")
program.emit("PRINT")

program.emit("GDSTR", 64, 0)
program.emit("CONSTI8", 0)
program.emit("GSTORE", 1)
program.emit("CONSTI8", 1)
program.emit("GSTORE", 2)
program.label("sum_loop")
program.emit("GLOAD", 1)
program.emit("GLOAD", 2)
program.emit("ADDI")
program.emit("GSTORE", 1)
program.emit("GLOAD", 2)
program.emit("CONSTI8", 1)
program.emit("ADDI")
program.emit("GSTORE", 2)
program.emit("GLOAD", 2)
program.emit("CONSTI8", 11)
program.emit("LTI")
program.address("JMPT", "sum_loop")
program.emit("GLOAD", 0)
program.string("Sum of 1 through 10 = ")
program.emit("GAPPND")
program.emit("GLOAD", 0)
program.emit("GLOAD", 1)
program.emit("GAPPND")
program.emit("GLOAD", 0)
program.emit("PRINT")
program.string("\n")
program.emit("PRINT")

program.emit("GDARRAY", 3, 3)
for index, value in enumerate((4, 8, 15)):
    program.emit("CONSTI8", value)
    program.emit("CONSTI8", index)
    program.emit("GSTOREAE", 3)
program.string("Array element [1] = ")
program.emit("PRINT")
program.emit("CONSTI8", 1)
program.emit("GLOADAE", 3)
program.emit("PRINT")
program.string("\n")
program.emit("PRINT")

program.emit("CONSTI8", 10)
program.emit("CONSTI8", 10)
program.emit("EQI")
program.address("JMPT", "comparison_true")
program.string("Comparison failed\n")
program.emit("PRINT")
program.address("JMP", "after_comparison")
program.label("comparison_true")
program.string("10 equals 10: true\n")
program.emit("PRINT")
program.label("after_comparison")

program.string("Square(12) = ")
program.emit("PRINT")
program.emit("CONSTI8", 12)
program.address("CALL", "square", 1, 0)
program.emit("PRINT")
program.string("\nDone.\n")
program.emit("PRINT")
program.emit("HALT")

program.label("square")
program.emit("LDARG", 0)
program.emit("LDARG", 0)
program.emit("MULI")
program.emit("RET")

program.resolve()

# The CLI consumes a two-byte container header before loading VM code.
output = Path(__file__).with_name("demo.vm")
output.write_bytes(bytes((0, 4)) + program.code)
