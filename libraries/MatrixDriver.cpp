/*
 
*/

#include "MatrixDriver.h"

// init the Port lines and invoke timer 1 configuration
void MatrixDriver::init()
{
    #ifdef DEBUG
        DEBUG_DDR  |=  ((1 << DEBUG_DI) | (1 << DEBUG_DCKI) | 
                        (1 << DEBUG_DEC_A0) | (1 << DEBUG_DEC_A1) | (1 << DEBUG_DEC_A2) | 
                        (1 << DEBUG_DEC_E3)); // outputs
        DEBUG_PORT &= ~((1 << DEBUG_DI) | (1 << DEBUG_DCKI) | 
                        (1 << DEBUG_DEC_A0) | (1 << DEBUG_DEC_A1) | (1 << DEBUG_DEC_A2) | 
                        (1 << DEBUG_DEC_E3)); // LOW
        // port |=  (1 << bit number); // set   the bit
        // port &= ~(1 << bit number); // clear the bit
    #endif


    // set all driver lines as output and set them to LOW
    MY9221_DDR  |=   _BV(MY9221_DI) | _BV(MY9221_DCKI);     // outputs
    MY9221_PORT &= ~(_BV(MY9221_DI) | _BV(MY9221_DCKI));    // LOW

    // decoder lines
    DEC_DDR  |=   _BV(DEC_A0) | _BV(DEC_A1) | _BV(DEC_A2) | _BV(DEC_E3);    // outputs
    DEC_PORT &= ~(_BV(DEC_A0) | _BV(DEC_A1) | _BV(DEC_A2) | _BV(DEC_E3));   // LOW

    // init the line counter
    m_currentLine = 0;

    // use timer1 to create a task which gets called every 100us
    cli(); //stop interrupts

    /*
    |----------|--------|--------|--------|--------|-------|------|-------|-------|
    | Register |   7    |   6    |   5    |   4    |   3   |  2   |   1   |   0   |
    |----------|--------|--------|--------|--------|-------|------|-------|-------|
    | TCCR1A   | COM1A1 | COM1A0 | COM1B1 | COM1B0 | -     | -    | WGM11 | WGM10 |
    |          | 0      | 0      | 0      | 0      | -     | -    | 0     | 0     |
    |----------|--------|--------|--------|--------|-------|------|-------|-------|
    | TCCR1B   | ICNC1  | ICES1  | -      | WGM13  | WGM12 | CS12 | CS11  | CS10  |
    |          | -      | -      | -      | 0      | 1     | 0    | 0     | 1     |
    |----------|--------|--------|--------|--------|-------|------|-------|-------|
    
    All COM registers are set to 0, because we don't want a pwm output on a pin
    CTC, TOP = OCR1A
    >> WGM 13, 12, 11, 10: 0, 1, 0, 0
    ICNC1 and ICES1 can be ignored, because no external clock source is used
    No Prescaling
    CS 12, 11, 10: 0, 0, 1
    For more details see chapter 20.14 of Atmega328 datasheet
    */
    
    _SFR_BYTE(TCCR1A) = 0;
    _SFR_BYTE(TCCR1B) = _BV(WGM12) | _BV(CS10);
    _SFR_BYTE(TIMSK1) |= _BV(OCIE1A);

    OCR1A = 20000;

    sei(); //allow interrupts
}

// routine to send 16bit data to MY9221 driver chip
inline void MatrixDriver::send16bitData(uint16_t data)
{
	for (uint8_t i=15; i<16; i--) { // i will overflow to 255 after 0
		if (data & (1 << i)) {
			MY9221_PORT |= _BV(MY9221_DI);
		} else {
			MY9221_PORT &=~ _BV(MY9221_DI);
		}
		MY9221_PORT ^= _BV(MY9221_DCKI);
	}
}

// latch routine for MY9221 data exchange
inline void MatrixDriver::latchData(void)
{
	MY9221_PORT &=~ _BV(MY9221_DI);
    delayMicroseconds(10);
    for(unsigned char i=0;i<8;i++) {
    	MY9221_PORT ^= _BV(MY9221_DI);
    }
} 


// update one line of the matrix
void MatrixDriver::updateLine()
{
    unsigned char i, k, lineBits;

    // disable decoder while configuring the next line
    DEC_PORT &=~ _BV(DEC_E3);

    // clear the MY9221 before we send the data for the next line
    for (k=0;k<2;k++) {
		send16bitData(CmdMode);
		MY9221_PORT &=~ _BV(MY9221_DI);
		for(i=0;i<192;i++) {
			// toggle clock pin
			MY9221_PORT ^= _BV(MY9221_DCKI);
		}
    }

    latchData();

    // now send the real data
    // first data segment for the 2nd MY9221 chip
    send16bitData(CmdMode);
    // BLUE segment
    send16bitData(0);    // A3 --> BLUE8
    send16bitData(255);  // B3 --> BLUE7
    send16bitData(0);    // C3 --> BLUE6
    send16bitData(255);  // A2 --> BLUE5
    send16bitData(0);    // B2 --> BLUE4
    send16bitData(255);  // C2 --> BLUE3
    send16bitData(0);    // A1 --> BLUE2
    send16bitData(255);  // B1 --> BLUE1
    // GREEN segment
    send16bitData(0);    // C1 --> GREEN8
    send16bitData(0);    // A0 --> GREEN7
    send16bitData(0);    // B0 --> GREEN6
    send16bitData(0);    // C0 --> GREEN5

    // second data segment for the 1nd MY9221 chip
    send16bitData(CmdMode);
    // GREEN segment
    send16bitData(0);    // A3 --> GREEN4
    send16bitData(0);    // B3 --> GREEN3
    send16bitData(0);    // C3 --> GREEN2
    send16bitData(0);    // A2 --> GREEN1
    // RED segment
    send16bitData(0);    // B2 --> RED8
    send16bitData(255);  // C2 --> RED7
    send16bitData(0);    // A1 --> RED6
    send16bitData(255);  // B1 --> RED5
    send16bitData(0);    // C1 --> RED4
    send16bitData(255);  // A0 --> RED3
    send16bitData(0);    // B0 --> RED2
    send16bitData(255);  // C0 --> RED1

    // data transfered and latch it
    latchData();

    // change the line. we have 8 lines. m_currentLine uses therefor 3 bits
    // A0, A1, A2 used consecutive ports. we can use the linenumber to switch the ports
    lineBits = ((m_currentLine) << DEC_A0); // DEC_A0 is the first pin
    DEC_PORT &=~ lineBits;
    DEC_PORT |= lineBits;

    // enable the decoder
    DEC_PORT |= _BV(DEC_E3);

    // increment line number and enable decoder
    m_currentLine++;
    if (8 >= m_currentLine) {
    	m_currentLine = 0;
    }
}

ISR(TIMER1_COMPA_vect)
{
    //Md.updateLine();
    #ifdef DEBUG
        DEBUG_PORT ^= (1 << (DEBUG_DCKI)); // toggle the debug clock
    #endif
}


MatrixDriver Md;
