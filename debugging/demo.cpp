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

int calculationDecoderLine()
{
	char DEC_PORT = 0b10000001;
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

// colors of the RGB led
struct ledColor 
{
	int red;
	int green; 
	int blue;
} rgbValue;

int activeBuffer = 1;

// led definition for the full matrix
ledColor MatrixBuffer_01[7][7];
ledColor MatrixBuffer_02[7][7];

ledColor setLedColor(int red, int green, int blue)
{
	rgbValue.red   = red;
	rgbValue.green = green;
	rgbValue.blue  = blue;
	return rgbValue;
}

void clearMatrixBuffer()
{
	if(activeBuffer == 1)
	{
		for(int row=0;row<8;row++)
		{
			for(int colom=0;colom<8;colom++)
			{	
				MatrixBuffer_01[row][colom] = setLedColor(0x00, 0x00, 0x00);
			}
		}
	}
	else
	{
		for(int row=0;row<8;row++)
		{
			for(int colom=0;colom<8;colom++)
			{	
				MatrixBuffer_02[row][colom] = setLedColor(0x00, 0x00, 0x00);
			}
		}
	}
}

void flashMatrixBuffer(int red, int green, int blue)
{
	for(int row=0;row<8;row++)
	{
		for(int colom=0;colom<8;colom++)
		{
			MatrixBuffer_01[row][colom] = setLedColor(red, green, blue);
		}
	}
}


int main()
{
	printf("Hello Word!\n");
	MatrixBuffer_01[0][0] = setLedColor(1,4,3);
	printf("%d\n", MatrixBuffer_01[0][0].red);
	printf("%d\n", MatrixBuffer_01[0][0].green);
	printf("%d\n", MatrixBuffer_01[0][0].blue);
	clearMatrixBuffer();
	printf("%d\n", MatrixBuffer_01[0][0].red);
	printf("%d\n", MatrixBuffer_01[0][0].green);
	printf("%d\n", MatrixBuffer_01[0][0].blue);
	flashMatrixBuffer(5,4,3);
	printf("%d\n", MatrixBuffer_01[0][0].red);
	printf("%d\n", MatrixBuffer_01[0][0].green);
	printf("%d\n", MatrixBuffer_01[0][0].blue);
	return 0;
}