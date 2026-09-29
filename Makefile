CC ?= gcc
CPPFLAGS := -I VM_CLI -I VM_CLI/VM -I VM_CLI/VM\ Utility
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -O2
LDFLAGS ?=
LDLIBS ?=

TARGET := build/vm-cli
OBJECTS := \
	build/main.o \
	build/inline_output.o \
	build/VM/vm_array_operations.o \
	build/VM/vm_cpu.o \
	build/VM/vm_event_buffer.o \
	build/VM/vm_opstack_operations.o \
	build/VM/vm_progmem_operations.o \
	build/VM/vm_string_operations.o \
	build/VM/vm_variable_operations.o \
	build/vm_utility/vm_printers.o
DEPS := $(OBJECTS:.o=.d)

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(OBJECTS)
	@mkdir -p $(@D)
	$(CC) $(LDFLAGS) -o $@ $^ $(LDLIBS)

build/%.o: VM_CLI/%.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c -o "$@" "$<"

build/vm_utility/vm_printers.o: VM_CLI/VM\ Utility/vm_printers.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c -o "$@" "$<"

run: $(TARGET)
	./$(TARGET) $(PROGRAM)

clean:
	$(RM) -r build

-include $(DEPS)
