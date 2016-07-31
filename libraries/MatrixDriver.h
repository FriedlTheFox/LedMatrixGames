/*
 Matrix diver for the Rainbowduino board
*/

#ifndef MATRIXDRIVER_h
#define MATRIXDRIVER_h

#include <Arduino.h>
#include <avr/pgmspace.h>

'''
REGISTER
'''

// MY9221 :: 12-Channel LED Driver
#define MY9221_DI   PORTB0	// data
#define MY9221_DCKI PORTB1	// clock

#define MY9221_DDR  DDRB	// direction
#define MY9221_PORT PORTB	// active/passive

// 74HC138 :: 3-to-8 Line Decoder
/*
E = Control; A = Input; Y = Output
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| E1 | E2 | E3 | A2 | A1 | A0 | Y7 | Y6 | Y5 | Y4 | Y3 | Y2 | Y1 | Y0 |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| H  | X  | X  | X  | X  | X  | H  | H  | H  | H  | H  | H  | H  | H  |
| X  | H  | X  |    |    |    |    |    |    |    |    |    |    |    |
| X  | X  | L  |    |    |    |    |    |    |    |    |    |    |    |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| L  | L  | H  | L  | L  | L  | H  | H  | H  | H  | H  | H  | H  | L  |
|    |    |    | L  | L  | H  | H  | H  | H  | H  | H  | H  | L  | H  |
|    |    |    | L  | H  | L  | H  | H  | H  | H  | H  | L  | H  | H  |
|    |    |    | L  | H  | H  | H  | H  | H  | H  | L  | H  | H  | H  |
|    |    |    | H  | L  | L  | H  | H  | H  | L  | H  | H  | H  | H  |
|    |    |    | H  | L  | H  | H  | H  | L  | H  | H  | H  | H  | H  |
|    |    |    | H  | H  | L  | H  | L  | H  | H  | H  | H  | H  | H  |
|    |    |    | H  | H  | H  | L  | H  | H  | H  | H  | H  | H  | H  |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
H = HIGH voltage; L = LOW voltage; X = don't care
E1 = L and E2 = L
*/
#define DEC_A0 PORTD4
#define DEC_A1 PORTD5
#define DEC_A2 PORTD6
#define DEC_E3 PORTD7

// assume that all decoder pins are on the same port
#define DEC_DDR DDRD
#define DEC_PORT PORTD

'''
DATA
'''

// MY9221 command
/*
|------------|----------|---------|----------------------------------------------------------------|
|  BIT No.   |   Name   | Default |                      DESCRIPTION FUNCTION                      |
|------------|----------|---------|----------------------------------------------------------------|
| CMD[15:11] | Temp     |   00000 | Not used Please filled with all “0”                            |
| CMD[10]    | hspd     |       0 | Iout Tr/Tf select                                              |
|            |          |         | 0 : Iout slow mode                                             |
|            |          |         | 1 : Iout fast mode                                             |
| CMD[9:8]   | bs[1:0]  |       0 | Grayscale resolution select                                    |
|            |          |         | 00 : 8-bit grayscale application                               |
|            |          |         | 01 : 12-bit grayscale application                              |
|            |          |         | 10 : 14-bit grayscale application                              |
|            |          |         | 11 : 16-bit grayscale application                              |
| CMD[7:5]   | gck[2:0] |     000 | Internal oscillator freq. select                               |
|            |          |         | 000 : original freq (8.6MHz)                                   |
|            |          |         | 001 : original freq/2                                          |
|            |          |         | 010 : original freq/4                                          |
|            |          |         | 011 : original freq/8                                          |
|            |          |         | 100 : original freq/16                                         |
|            |          |         | 101 : original freq/64                                         |
|            |          |         | 110 : original freq/128                                        |
|            |          |         | 111 : original freq/256                                        |
|            |          |         | If CMD[3]=1, please set CMD[7:5]=000                           |
| CMD[4]     | sep      |       0 | Output waveform select                                         |
|            |          |         | 0 : MY-PWM output waveform (similar to traditional waveform)   |
|            |          |         | 1 : APDM output waveform                                       |
| CMD[3]     | osc      |       0 | Grayscale clock source select                                  |
|            |          |         | 0 : internal oscillator (8.6MHz) (internal GCK source)         |
|            |          |         | 1 : external clock from GCKI pin (external GCK source)         |
| CMD[2]     | pol      |       0 | Output polarity select                                         |
|            |          |         | 0 : work as LED driver                                         |
|            |          |         | 1 : work as MY-PWM/APDM generator                              |
| CMD[1]     | cntset   |       0 | Counter reset select                                           |
|            |          |         | 0 : free running mode                                          |
|            |          |         | 1 : counter reset mode (Only usable when osc = “1”)            |
| CMD[0]     | onest    |       0 | One-shot select                                                |
|            |          |         | 0 : frame cycle repeat mode                                    |
|            |          |         | 1 : frame cycle One-shot mode (Only usable when  cntset = “1”) |
|------------|----------|---------|----------------------------------------------------------------|
*/
#define CmdMode 0b0000000000000000

'''
DATA TYPES
'''

// structure for the RGB definition
typedef struct 
{
	uint8_t red; 
	uint8_t green; 
	uint8_t blue;
}rgbValues;

// rgbValues MatrixBuffer[8][8];


'''
CLASSES and METHODS
'''

class MatrixDriver
{
public:
    void init();		// inti driver
    void updateLine();	// called from ISR. treat like private

private:
    uint8_t m_currentLine;						// current line number of the matirx display to update
    inline void send16bitData(uint16_t data);	// send data to the MY9221
    inline void latchData(void);				// latch funtcion for MY9221
};

extern MatrixDriver Md;

#endif
