/*
 
*/

#ifndef MATRIXDRIVER_h
#define MATRIXDRIVER_h

#include <Arduino.h>
#include <avr/pgmspace.h>


// MY9221 driver interfaces 
#define MY9221_DI   PORTB0	// data
#define MY9221_DCKI PORTB1	// clock

#define MY9221_DDR  DDRB
#define MY9221_PORT PORTB

#define DDR_Data  DDRB
#define DDR_Clk   DDRB

#define PORT_Data PORTB
#define PORT_Clk  PORTB

#define BIT_Data  0x01
#define BIT_Clk   0x02

// 3-to-8 Decoder Lines
#define DEC_A0 PORTD4
#define DEC_A1 PORTD5
#define DEC_A2 PORTD6
#define DEC_E3 PORTD7

// assume that all decoder pins are on the same port
#define DEC_DDR DDRD
#define DEC_PORT PORTD

// MY9221 command
// TODO: insert description
#define CmdMode 0b0000000000000000

// structure for the RGB definition
typedef struct 
{
	uint8_t red; 
	uint8_t green; 
	uint8_t blue;
}rgbValues;

// rgbValues MatrixBuffer[8][8];

class MatrixDriver
{
public:
    void init();
    void send16bitData(unsigned int data);
    void latchData(void);
    void switchOnDrive(unsigned char line);
    void clearDisplay(void); //Is not made private method as used in ISR. Use this like a private method.
    void updateLine(int lineNumber);

private:

};

extern MatrixDriver Md;

#endif
