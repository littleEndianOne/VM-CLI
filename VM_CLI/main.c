/* 
 * File:   main.c
 * Author: David
 *  
 * Created on 6 March 2018, 4:44 PM
 * 
 * VM CLI Application
 * Load and run a VM program from a standard text file.
 */

#include <stdio.h>
#include <stdlib.h>
#include "VM/vm_cpu.h"
#include <errno.h>
#include <string.h>
#include "VM/vm_common.h"
#include "VM Utility/vm_printers.h"
#include "inline_output.h"

#define PROGMEM_SIZE 2048

//No inline functions to implement

boolean_t vm_ExecuteInlineFunction(vm_cpu *vm, vm_opcode opcode) {
	//254 is the opcode assigned to the inline PRINT function
	if (((uint8_t) opcode) == 254) {
		Inline_PRINT(vm);
		return TRUE;
	} else
		return FALSE;
}

//progmem
uint8_t progmem[PROGMEM_SIZE];

uint8_t vm_ReadByte(uint16_t address) {
	return progmem[address];
	return 0;
}

int main(int argc, char *argv[]) {
	uint8_t pc = 0; //Program counter start
	uint8_t gCount = 0; //Number of globals to allocate
	uint8_t verbose = 0;

	printf("\n\n--VM CLI--\n");

	if (argc >= 2) {
		const char *filePath = argv[1];

		if (argc >= 3) //Command line argument exists at index 2
				{
			if (strcmp(argv[2], "-v") == 0) //Was it the verbose switch?
					{
				verbose = 1;
			}
		}

		printf("Opening file: %s \n\n", filePath);

		int c;
		uint16_t byteCount = 0;
		FILE *file;
		file = fopen(filePath, "r");

		if (file) {
			//Get pc start
			c = getc(file);
			if (c != EOF) {
				pc = (uint8_t) c;
				if (verbose)
					printf("pc start: %u \n", c);
			}

			c = getc(file);
			//Get globals count
			if (c != EOF) {
				gCount = (uint8_t) c;
				if (verbose)
					printf("gCount: %u \n", c);
			}

			while (((c = getc(file)) != EOF) & (byteCount < PROGMEM_SIZE)) {
				progmem[byteCount] = (uint8_t) c;
				/*The byteCount will end one higher than the last index stored.
				 which makes is a byte count.
				 */
				byteCount++;
			}

			fclose(file);
			//If we reached the end of the file then the whole program was
			//read into progmem.
			if (c == EOF) {

				int i;
				if (verbose) {
					printf("Program byte count: %u \n", byteCount);
					printf("Code Listing...\n");

					for (i = 0; i < byteCount; i++) {
						printf("%u: %u\n", i, progmem[i]);
					}
				}

				vm_cpu *vm;
				//Pass NULL for the program because the program is using an
				//external array for the program storage.
				vm = vm_New(pc, gCount, byteCount, 20, 4, 4);

				printf("\nStarting Program...\n\n");
				vm_Run(vm);
				printf("\n\nProgram Finished.\n");

				if (vm->errorCode != OK) //If runtime error occurred.
						{
					PrintThreadState(vm);
				} else if (verbose) //Command line argument exists at index 2
				{
					PrintThreadState(vm);
				}
			} else {
				printf("ERROR: Program does not fit into 2048B of progmem");
			}
		} else {
			printf("File Error %u: %s", errno, strerror(errno));
		}
	} else {
		printf("No program file...");
	}

	return (EXIT_SUCCESS);
}
