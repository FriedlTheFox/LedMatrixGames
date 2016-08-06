/*
 
*/

#include "MatrixDriver.h"

// init the Port lines and invoke timer 1 configuration
void MatrixDriver::init()
{
    // port |=  (1 << bit number); // set   the bit
    // port &= ~(1 << bit number); // clear the bit


    // set all driver lines as output and set them to LOW
    MY9221_DDR  |=   _BV(MY9221_DI) | _BV(MY9221_DCKI);     // outputs
    MY9221_PORT &= ~(_BV(MY9221_DI) | _BV(MY9221_DCKI));    // LOW

    // decoder lines
    DEC_DDR  |=   _BV(DEC_A0) | _BV(DEC_A1) | _BV(DEC_A2) | _BV(DEC_E3);    // outputs
    DEC_PORT &= ~(_BV(DEC_A0) | _BV(DEC_A1) | _BV(DEC_A2) | _BV(DEC_E3));   // LOW

    // use timer1 to create a task which gets called every 100us
    cli(); //stop interrupts

    /*
    TCCR1A/B/C (Timer/Counter1 Control Regiser A/B/C
    |-----------|--------|--------|--------|--------|-------|------|-------|-------|
    |  Register |   7    |   6    |   5    |   4    |   3   |  2   |   1   |   0   |
    |-----------|--------|--------|--------|--------|-------|------|-------|-------|
    | TCCR1A    | COM1A1 | COM1A0 | COM1B1 | COM1B0 | -     | -    | WGM11 | WGM10 |
    | bit value | 0      | 0      | 0      | 0      | -     | -    | 0     | 0     |
    |-----------|--------|--------|--------|--------|-------|------|-------|-------|
    | TCCR1B    | ICNC1  | ICES1  | -      | WGM13  | WGM12 | CS12 | CS11  | CS10  |
    | bit value | -      | -      | -      | 0      | 1     | 0    | 0     | 1     |
    |-----------|--------|--------|--------|--------|-------|------|-------|-------|
    | TCCR1C    | FOC1A  | FOC1B  | -      | -      | -     | -    | -     | -     |
    | bit value | 0      | 0      | -      | -      | -     | -    | -     | -     |
    |-----------|--------|--------|--------|--------|-------|------|-------|-------|
    
    COM1A1, COM1A0/COM1B1, COM1B0 (Compare Output Mode Bits)
    --> 0b0000 : normal port operation, OC1A/OC1B disconnected

    WGM13, WGM12, WGM11, WGM10 (Waveform Generation Mode Bits)
    --> 0b0100 : Clear Timer on Compare match (CTC); TOP = OCR1A; update of OCR1x at immediate; TOV1 Flag set on MAX

    ICNC1 (Input Capture Noise Canceler)
    --> 0b0    : ICP1 is not used. Filter is disabled.

    ICES1 (Input Capture Edge Select)
    --> 0b0    : ICP1 is not used. 0 = falling edge; 1 = rising edge

    CS12, CS11, CS10 (Clock Select)
    --> 0b001  : clk/1 (no prescaling)

    FOC1A, FOC1B (Force Output Compare for Channel A/B)
    --> 0b00   : WGM13:0 must be specifies a non_PWM mode
    */
    
    TCCR1A = 0x00;
    TCCR1B = (1 << WGM12) | (1 << CS10);
    TCCR1C = 0x00;

    /*
    TCNT1H, TCNT1L (Timer/Counter1)
    */

    /*
    OCR1AH, OCR1AL, OCR1BH, OCR1BL (Output Compare Register 1 A/B)
    Register contain a 16 bit value that is compared with the counter value TCNT1
    
    OCR1A = external clock * time between events 
    100us --> 16MHz * 0,0001s = 1600
    */
    OCR1A = 1600;


    /*
    TIMSK1 (Timer/Counter1 Interrupt Mask Register)
    |-----------|---|---|-------|---|---|--------|--------|-------|
    |  Register | 7 | 6 |   5   | 4 | 3 |   2    |   1    |   0   |
    |-----------|---|---|-------|---|---|--------|--------|-------|
    | TCCR1A    | - | - | ICIE1 | - | - | OCIE1B | OCIE1A | TOIE1 |
    | bit value | - | - | 0     | - | - | 0      | 1      | 0     |
    |-----------|---|---|-------|---|---|--------|--------|-------|
    ICIE1 (Input Captre Interrupt Enable)
    --> 0b?  : ???
    OCIE1B, OCIE1A (Output Compare B/A Match Interrupt Enable)
    --> 0b01 : Interrupt enable for A. OCF1A/B - TIFR1
    TPOE1 (Overflow Interrupt Enable)
    --> 0b0  : Interrupt disable.
    */
    TIMSK1 |= (1 << OCIE1A);

    /*
    TIFR1 (Iterrupt Flag Register)
    */


    sei(); // allow interrupts
}

// routine to send 16 bit data to MY9221 driver chip
inline void MatrixDriver::send16bitData(uint16_t data)
{
    uint16_t mask = 0x8000;                  // mask to select one bit
	for (uint8_t i=15; i<16; i--)            // decreasing 15,14,..,1,0,255
    {
        if (data & mask)                     // if the masked bit of data is equal 1
        {
			MY9221_PORT |= _BV(MY9221_DI);   // data to 1
        }
		else                                 // if the masked bit of data is equal 0
        {
			MY9221_PORT &=~ _BV(MY9221_DI);  // data to 0
		}
		MY9221_PORT ^= _BV(MY9221_DCKI);     // toggle clock
        mask = mask >> 1;                    // shift the mask bit one step right
	}
}

// latch routine for MY9221 data exchange
inline void MatrixDriver::latchData(void)
{
    // 1. step
                                           // keeping clock at a fixed level
	MY9221_PORT &=~ _BV(MY9221_DI);        // set data to 0
    delayMicroseconds(10);                  // wait Tstart > 220us
    // 2. step
    for(unsigned char i=0;i<8;i++)         // send four data pulses (tH>70ns, tL>230ns)
    {
    	MY9221_PORT ^= _BV(MY9221_DI);     // toggle data
    }
    // 3. step
                                           // data is loaded in the latch register
    delayMicroseconds(10);                  // Tstop > 200ns + N * 10ns (N=2 MY9221 chips)
} 


// update one line of the matrix
void MatrixDriver::updateLine(uint8_t lineNumber)
{
    // send the new data
    // first data segment for the 2nd MY9221 chip
    send16bitData(CmdMode);
    // BLUE segment
    send16bitData(0xFF);    // A3 --> BLUE8
    send16bitData(0);  // B3 --> BLUE7
    send16bitData(0);    // C3 --> BLUE6
    send16bitData(0);  // A2 --> BLUE5
    send16bitData(0xFF);    // B2 --> BLUE4
    send16bitData(10);  // C2 --> BLUE3
    send16bitData(0);    // A1 --> BLUE2
    send16bitData(0);  // B1 --> BLUE1
    // GREEN segment
    send16bitData(0xFF);    // C1 --> GREEN8
    send16bitData(0);    // A0 --> GREEN7
    send16bitData(255);    // B0 --> GREEN6
    send16bitData(0);    // C0 --> GREEN5

    // second data segment for the 1nd MY9221 chip
    send16bitData(CmdMode);
    // GREEN segment
    send16bitData(0);    // A3 --> GREEN4
    send16bitData(0);    // B3 --> GREEN3
    send16bitData(10);    // C3 --> GREEN2
    send16bitData(0);    // A2 --> GREEN1
    // RED segment
    send16bitData(0xFF);    // B2 --> RED8
    send16bitData(0xFF);  // C2 --> RED7
    send16bitData(255);    // A1 --> RED6
    send16bitData(0xFF);  // B1 --> RED5
    send16bitData(0xFF);    // C1 --> RED4
    send16bitData(0);  // A0 --> RED3
    send16bitData(0);    // B0 --> RED2
    send16bitData(255);  // C0 --> RED1

    // disable decoder while updating the current line (E3 = LOW)
    DEC_PORT &=~ _BV(DEC_E3);

    // data transfered and latch it
    latchData();

    // activate the current line
    uint8_t lineBits  = (lineNumber << DEC_A0); // calculate line bits
    DEC_PORT &= ~(0b111 << DEC_A0);             // clear bits in PORT
    DEC_PORT |= lineBits;                       // set new bits in PORT
    
    // enable the decoder  (E3 = HIGH)
    DEC_PORT |= _BV(DEC_E3);
}

ISR(TIMER1_COMPA_vect)
{
    //Md.updateLine(1);
}

MatrixDriver Md;