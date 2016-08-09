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
	Md.flashMatrixBuffer(random(0, 150),random(0, 150),random(0, 150));
	// update Matrix
	for(char i=0;i<8;i++)
	{
		Md.updateLine(i);
		delay(1);
	}
}
