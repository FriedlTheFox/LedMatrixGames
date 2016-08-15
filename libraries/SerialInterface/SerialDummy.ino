byte byteRead;

void setup()
{
	// init serial port
	Serial.begin(9600);
	// init led matrix and clear buffer
}

void loop() 
{
	
  if (Serial.available()) {
    /* read the most recent byte */
    byteRead = Serial.read();
    /*ECHO the value that was read, back to the serial port. */
    Serial.write(byteRead);
  }

}
