#include "inline_output.h"

#include "VM/vm_opstack_operations.h"
#include "VM/vm_progmem_operations.h"

void Inline_PRINT(vm_cpu* vm) {

    //get value from top of the stack ...
    vm_element e = OpStackPop(vm);

    //branch based on the type.
    switch (e.type)
    {
        case FLOAT:
            Inline_PrintFloat(e.value.float32);
            break;
        case INTEGER:
            Inline_PrintInteger(e.value.int32);
            break;    
        case STRING_LIT:
            Inline_PrintStrLit(vm, e.value.strLit.address, e.value.strLit.length);
            break;
        case STRING_REF:
            Inline_PrintStrRef(vm, e.value.strRef.charPtr);
            break;
        case NONE:
            printf("None");
            break;
        default:
            SYSTEM_ERROR(TYPE_ERROR);
            break;
    }
}

void Inline_PrintFloat(float number) {
    printf("%f", number);
}

void Inline_PrintInteger(int32_t number) {
    printf("%i", number);
}

void Inline_PrintStrLit(vm_cpu* vm, uint16_t address, uint8_t length) {
    uint8_t i = 0; //Start iteration at first character

    //Read each character and print it...
    for (; i < length; i++) //String length does not include the prefixed length.
    {
        char c = (char) PeakCodeAt(vm, address + i);
        printf("%c", c);
    }
}

void Inline_PrintStrRef(vm_cpu* vm, char* address) {
    (void) vm;
    printf("%s", address);
}
