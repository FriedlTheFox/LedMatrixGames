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
    void updateLine(); //called from ISR. treat like private

private:
    uint8_t m_currentLine;
    inline void send16bitData(uint16_t data);
    inline void latchData(void);
};

extern MatrixDriver Md;

#endif
