/* 
 * rainbowduino middleware
 * 
 * Interface between the MY9221 driver and the serial connection of the ATmega
 * 
 */

#include <MatrixDriver.h>

void setup()
{
  Md.init();
}

void loop() 
{
	// flash buffer
	Md.flashMatrixBuffer(0x00,0x00,0x00); // BLACK
	// update Matrix
	for(char i=0;i<8;i++)
	{
		delay(1);
		Md.updateLine(i);
	}
	// flash buffer
	Md.flashMatrixBuffer(0xFF,0x00,0x00); // RED
	// update Matrix
	for(char i=0;i<8;i++)
	{
		delay(1);
		Md.updateLine(i);
	}
	
}
