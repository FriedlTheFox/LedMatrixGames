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
  Md.clearDisplay();
}

void loop() 
{
  delay(100);
  Md.setPixel(1, 2, rgb);
  delay(100);
  Md.clearDisplay();
}
