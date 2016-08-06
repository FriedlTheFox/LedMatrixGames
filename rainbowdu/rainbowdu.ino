/* 
 * rainbowduino middleware
 * 
 * Interface between the MY9221 driver and the serial connection of the ATmega
 * 
 */

#include <MatrixDriver.h>

rgbValues rgb = {255, 0, 0};

void setup()
{
  Md.init();
}

void loop() 
{
	for(uint8_t i=0;i<8;i++)
	{
		delay(1);
		Md.updateLine(i);
	}
}
