
/*
  Software serial multple serial test

 Receives from the hardware serial, sends to software serial.
 Receives from software serial, sends to hardware serial.

 The circuit:
 * RX is digital pin 10 (connect to TX of other device)
 * TX is digital pin 11 (connect to RX of other device)

 Note:
 Not all pins on the Mega and Mega 2560 support change interrupts,
 so only the following can be used for RX:
 10, 11, 12, 13, 50, 51, 52, 53, 62, 63, 64, 65, 66, 67, 68, 69

 Not all pins on the Leonardo and Micro support change interrupts,
 so only the following can be used for RX:
 8, 9, 10, 11, 14 (MISO), 15 (SCK), 16 (MOSI).

 created back in the mists of time
 modified 25 May 2012
 by Tom Igoe
 based on Mikal Hart's example

 This example code is in the public domain.

 */



#define MAX_LENGTH_CMD 1024

// known commands
#define C_CMD_INFO "INFO"
#define C_CMD_TIME "TIME"
#define C_CMD_PWR "PWR"
#define C_CMD_RST "RST"


void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(38400);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.println("Starting UART Power Bank emulaor");
}

void loop() { // run over and over

  String buffer = "";
  char bufferOut[MAX_LENGTH_CMD] = "";
  int nbRead = 0;
  char eoc = 0;
  char _car = 0;
  int _delay = 0;
  
  // read command
  if (Serial.available()) {
    nbRead = 0;
    while ((nbRead < MAX_LENGTH_CMD) && (0 == eoc))
    {
      if (Serial.available())
      {
        _car = Serial.read();
        switch(_car)
        {
          case '\n' : ;
          case '\r' : eoc = 1; break;
  
          
          default : buffer += _car;
                    nbRead ++;
                    break;
        }
      }
      
    }

    // Respond
    if (true == buffer.equals(C_CMD_INFO))
    {
      Serial.println("VBAT=4.05 VOUT=5.12 VDC=5.29");
      Serial.println("VIN=39.08 IOUT=2.8 TEMP=031 CHG=1");
      Serial.println("WRN=0 PWR=1");
    }
    else if (true == buffer.startsWith(C_CMD_TIME))
    {
      if (true == buffer.equals(C_CMD_TIME))
      {
        snprintf(bufferOut,MAX_LENGTH_CMD, "%04d-%02d-%02dT%02d:%02d:%02dZ",
              int(random(1900, 2050)),
              int(random(1, 13)),
              int(random(1, 30)),
              int(random(0, 24)),
              int(random(0, 60)),
              int(random(0, 60)));
      }
      else
      {
        buffer.substring(5).toCharArray(bufferOut, MAX_LENGTH_CMD);
      }

      
      Serial.println(bufferOut);
    }
    else if (true == buffer.startsWith(C_CMD_PWR))
    {
      if (true == buffer.equals(C_CMD_PWR))
      {
        Serial.print("OK");
      }
      else
      {
        buffer.substring(4).toCharArray(bufferOut, MAX_LENGTH_CMD);
        sscanf(bufferOut, "%d", &_delay);

        snprintf(bufferOut, MAX_LENGTH_CMD, "VALUE '%d' ", _delay);

        if ((0 <= _delay) && (_delay < 1000))
        {
          Serial.println("OK");
        }
        else
        {
          Serial.println("ERROR");
        }
      }
    }
    else if (true == buffer.startsWith(C_CMD_RST))
    {
      if (true == buffer.equals(C_CMD_RST))
      {
        Serial.print("OK");
      }
      else
      {
        buffer.substring(4).toCharArray(bufferOut, MAX_LENGTH_CMD);
        sscanf(bufferOut, "%d", &_delay);

        snprintf(bufferOut, MAX_LENGTH_CMD, "VALUE '%d' ", _delay);

        if ((0 <= _delay) && (_delay < 1000))
        {
          Serial.println("OK");
        }
        else
        {
          Serial.println("ERROR");
        }
      }
    }
    else 
    {
      Serial.print(buffer);
    }

  
         
  }

}
