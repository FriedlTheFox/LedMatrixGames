/*
 
*/

#include "MatrixDriver.h"

//Init the Port lines and invoke timer 1 configuration

void MatrixDriver::init()
{

    // set all decoder lines as output and set them to LOW
	DEC_DDR |= _BV(DEC_A0) | _BV(DEC_A1) | _BV(DEC_A2) | _BV(DEC_E3);
	DEC_PORT &=~ (_BV(DEC_A0) | _BV(DEC_A1) | _BV(DEC_A2) | _BV(DEC_E3));

	// set all driver lines as output and set them to LOW
	MY9221_DDR |= _BV(MY9221_DI) | _BV(MY9221_DCKI);
	MY9221_PORT &=~ (_BV(MY9221_DI) | _BV(MY9221_DCKI));

    clearDisplay();

	// use timer1 to create a task which gets called every 100us
    cli();//stop interrupts

	// Register |   7    |   6    |   5    |   4    |   3    |   2    |   1    |   0
	//----------+--------+--------+--------+--------+--------+--------+--------+------
	//  TCCR1A  | COM1A1 | COM1A0 | COM1B1 | COM1B0 |   -    |   -    | WGM11  | WGM10
	//          |   0    |   0    |   0    |   0    |   -    |   -    |   0    |   0
	//  TCCR1B  | ICNC1  | ICES1  |   -    | WGM13  | WGM12  |  CS12  |  CS11  |  CS10
	//          |   -    |   -    |   -    |   0    |   1    |   0    |   0    |   1

	// All COM registers are set to 0, because we don't want a pwm output on a pin
	// CTC, TOP = OCR1A
	// >> WGM 13, 12, 11, 10: 0, 1, 0, 0
	// ICNC1 and ICES1 can be ignored, because no external clock source is used
	// No Prescaling
	// CS 12, 11, 10: 0, 0, 1
    // For more details see chapter 20.14 of Atmega328 datasheet

    _SFR_BYTE(TCCR1A) = 0;
	_SFR_BYTE(TCCR1B) = _BV(WGM12) | _BV(CS10);
	_SFR_BYTE(TIMSK1) |= _BV(OCIE1A);

	OCR1A = 20000;

	sei();//allow interrupts
}

//Routine to send 16bit data to MY9221 driver chips

void MatrixDriver::send16bitData(unsigned int data)
{
    for(unsigned char i=0;i<16;i++)
    {
        if(data&0x8000)
        {
            PORT_Data |= BIT_Data;
        }
        else
        {
            PORT_Data &=~ BIT_Data;
        }

        PORT_Clk ^= BIT_Clk;
        data <<= 1;
    }
}

//latch routine for MY9221 data exchange

void MatrixDriver::latchData(void)
{
    PORT_Data &=~ BIT_Data;

    delayMicroseconds(10);
    switchOffDrive;
    for(unsigned char i=0;i<8;i++)
    {
        PORT_Data ^= BIT_Data;
    }
} 

void MatrixDriver::switchOnDrive(unsigned char line)
{
  unsigned char LineBits = ((line)<<4);
  PORT_Lines &=~ BIT_Lines;
  PORT_Lines |= LineBits;
  PORT_Lines |= 0x80;
}

//clear MY9221 lines. Internally used for avoiding flicker. This is not the same as blank disply.

void MatrixDriver::clearDisplay(void)
{
    unsigned char i=0;
    unsigned char f=0;

    send16bitData(CmdMode);
    PORT_Data &=~ BIT_Data; // bitwise and not; change input
    for(i=0;i<192;i++)
    {
        {
            PORT_Clk ^= BIT_Clk;
        }
    }

    send16bitData(CmdMode);
    PORT_Data &=~ BIT_Data;
    for(i=0;i<192;i++)
    {
        {
            PORT_Clk ^= BIT_Clk;
        }
    }
    latchData();

}

void MatrixDriver::setPixel(int x, int y, rgbValues rgb)
{
    Md.send16bitData(CmdMode);

    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);

    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);

    Md.send16bitData(CmdMode);

    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);

    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);

    Md.latchData();
    Md.switchOnDrive(1);

    PORTD &=~ 0x04;
}

ISR(TIMER1_COMPA_vect)
{
    Md.send16bitData(CmdMode);

    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);

    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);

    Md.send16bitData(CmdMode);

    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);
    Md.send16bitData(0);

    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);
    Md.send16bitData(0);
    Md.send16bitData(255);

    Md.latchData();
    Md.switchOnDrive(1);

    PORTD &=~ 0x04;
}


MatrixDriver Md;
