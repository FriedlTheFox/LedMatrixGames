#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const char *byte_to_binary(int x)
{
    static char b[9];
    b[0] = '\0';

    int z;
    for (z = 128; z > 0; z >>= 1)
    {
        strcat(b, ((x & z) == z) ? "1" : "0");
    }

    return b;
}

int main()
{
	char DEC_PORT = 0b10000001;
	char mask = 0b00111000;
	char lineBits = 0;
	char lineNo = 0;

	for(lineNo = 0;lineNo < 8;lineNo++)
		{
		    DEC_PORT &= ~(0b111 << 3);			// clear bit positions
	        lineBits = ((lineNo) << 3); // shift number on first pin position
		    DEC_PORT |= lineBits;		// set new bits
		    printf("lineNo: %d --> %s\n", lineNo, byte_to_binary(DEC_PORT));
/*
A0(4), A1(5), A2(6)
          ## #
0 --> 0b0000 0000 : 0x00
1 --> 0b0000 1000 : 0x08
2 --> 0b0001 0000 : 0x10
3 --> 0b0001 1000 : 0x18
4 --> 0b0010 0000 : 0x20
5 --> 0b0010 1000 : 0x28
6 --> 0b0011 0000 : 0x30
7 --> 0b0011 1000 : 0x38
*/
		}
    return 0;
}