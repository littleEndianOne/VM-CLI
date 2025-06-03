#ifndef VM_OPCODES_DEBUG_H_INCLUDED
#define VM_OPCODES_DEBUG_H_INCLUDED

#include <stdio.h>

#include "VM/vm_common.h"
#include "VM/vm_cpu.h"

void Inline_PRINT(vm_cpu* vm);

void Inline_PrintFloat(float number);
void Inline_PrintInteger(int32_t number);
void Inline_PrintStrLit(vm_cpu* vm, uint16_t address, uint8_t length);
void Inline_PrintStrRef(vm_cpu* vm, char* address);

#endif // VM_OPCODES_DEBUG_H_INCLUDED
