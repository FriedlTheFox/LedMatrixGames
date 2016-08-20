/* 
 * rainbowduino middleware
 * 
 * Interface between the MY9221 driver and the serial connection of the ATmega
 * 
 */

#include <MatrixDriver.h>

int8_t errCode 	 = 0;
char*  errList[] = {"INFO: All fine\n", 
					"ERROR: Row is worng\n", 
					"ERROR: Colom is worng\n",
					"ERROR: Red is wrong\n", 
					"ERROR: Green is wrong\n",
					"ERROR: Blue is Wrong\n"};

int8_t row   = 0;
int8_t col   = 0;

int16_t red   = 0x00;
int16_t green = 0x00;
int16_t blue  = 0x00;

void setup()
{
	// init serial port
	Serial.begin(115200);
	Serial.write("INFO: Port is open\n");
	// init led matrix and clear buffer
	Md.init();
  	Md.flashMatrixBuffer(red,blue,green);
  	Md.setMatrixPixel(0, 0, 0, 0, 255);
  	Md.setMatrixPixel(0, 6, 0, 255, 0);
  	Md.setMatrixPixel(5, 0, 255, 0, 0);
  	Md.setMatrixPixel(4, 4, 255, 255, 255);
}

void loop() 
{
	while (Serial.available() > 0)
	{
		// get pixel position
		row   = Serial.parseInt();
		col   = Serial.parseInt();
		// get LED colors
		red   = Serial.parseInt();
		green = Serial.parseInt();
		blue  = Serial.parseInt();
		if (Serial.read() == '\n')
		{
/*
			// check pixel row
			if((row > 7) || (row < 0)) errCode = 1;
			if((col > 7) || (col < 0)) errCode = 2;
			// check color
			if((red > 255) || (red < 0)) errCode = 3;
			if((red > 255) || (red < 0)) errCode = 4;
			if((red > 255) || (red < 0)) errCode = 5;
			// if no error then set pixel
			if(errCode == 0) Md.setMatrixPixel(row, col, red, green, blue);
*/
			Md.setMatrixPixel(row, col, red, green, blue);
		}
//	Serial.write(errList[errCode]);
	}
	// update full matrix with current buffer as fast as possible
	Md.updateMatrix();
}
