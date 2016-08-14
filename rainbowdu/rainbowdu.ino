/* 
 * rainbowduino middleware
 * 
 * Interface between the MY9221 driver and the serial connection of the ATmega
 * 
 */

#include <MatrixDriver.h>

int8_t row   = 0;
int8_t col   = 0;

int16_t red   = 0x00;
int16_t green = 0x10;
int16_t blue  = 0x00;

void setup()
{
	// init serial port
	Serial.begin(115200);
	// init led matrix and clear buffer
	Md.init();
  	Md.flashMatrixBuffer(red,blue,green);
}

void loop() 
{
	// TODO: serial communication
	while (Serial.available() > 0)
	{
		//row   = Serial.parseInt();
		//col   = Serial.parseInt();
		
		red   = Serial.parseInt();
		green = Serial.parseInt();
		blue  = Serial.parseInt();
		if (Serial.read() == '\n')
		{
			//Md.setMatrixPixel(row, col, red, green, blue);
			Md.flashMatrixBuffer(red, green, blue);
		}
		Serial.write('Check\n');
	}

	// update full matrix with current buffer as fast as possible
	Md.updateMatrix();
}
