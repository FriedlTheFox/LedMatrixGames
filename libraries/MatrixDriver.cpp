/*
 
*/

#include "MatrixDriver.h"

//Init the Port lines and invoke timer 1 configuration

void MatrixDriver::init()
{
    DDR_Lines |= BIT_Lines;
    PORT_Lines &=~ BIT_Lines;

    DDRD |= 0x04;

    DDR_Data |= BIT_Data;
    DDR_Clk |= BIT_Clk;
    PORT_Data &=~ BIT_Data;
    PORT_Clk &=~ BIT_Clk;

    DDRB |= 0x20;

    clearDisplay();
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

MatrixDriver Md;
