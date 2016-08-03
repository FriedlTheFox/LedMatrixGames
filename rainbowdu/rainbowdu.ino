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
  delay(100);
  Md.updateLine(0);
}
