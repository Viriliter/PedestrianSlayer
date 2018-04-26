//=====================
//Region Libraries
//=====================
  //some libraries should be downloaded
  //#include <Servo.h>
  //#include <PID_v1.h>
//=====================
//Region Configuration Tab
//=====================
  int redLED = 8;
  int yellowLED = 9;
  int blueLED = 10;

  bool DIRECTION = True;            //set to forward direction
                                    //(false value is backward direction)
  bool ISDIRECTIONCHANGED = False;
  
  //Motor Configuration
  int MOTOR_PIN = 9;
  Servo motor;
  
  //Servo Configuration
  int SERVO_PIN = 10;
  Servo servo;

  //PID Configuration
  //------------------------
  //Define Variables we'll be connecting to
  double Setpoint, Input, Output;
  //Define the aggressive and conservative Tuning Parameters
  double aggKp=4, aggKi=0.2, aggKd=1;
  double consKp=1, consKi=0.05, consKd=0.25;
  
  //Specify the links and initial tuning parameters
  PID motorPID(&Input, &Output, &Setpoint, consKp, consKi, consKd, DIRECT);
  //------------------------
    
  //Light Configuration
  int BRAKE_LIGHT_PIN = 3;
  int LEFT_TURNING_PIN = 4;
  int RIGHT_TURNING_PIN = 5;
  int HIGH_BEAM_PIN = 6;
  
  //Ultrasonic Configuration
  int ULTRAS_TRIG = 7;
  int ULTRA_ECHO = 8;
  
  // MPU6050 Configuration
  int MPU_INT = 2;
  int MPU_SCL = A7;
  int MPU_SCA = A6;
  
  //Serial Configuration
  int BAUD_RATE = 19200;
  int PACKET_SIZE = 8;
//End Region

//Call methods
void serialRead();
void serialWrite();
void HEXClassifier(byte input[]);

void setup() {
  //=====================
  // This is test code:
  //=====================
  pinMode(redLED,OUTPUT);
  pinMode(yellowLED,OUTPUT);
  pinMode(blueLED,OUTPUT);
  Serial.begin(BAUD_RATE);
  //===========================
  //This is actual setup code
  //===========================
  /*Attach motor and servo pins
  motor.attach(MOTOR_PIN);
  servo.attach(SERVO_PIN);
  //turn the PID on
  motorPID.SetMode(AUTOMATIC);
  */
}


//===========================
//Region Serial Communication
//===========================
  void serialRead()
  {  
    if(Serial.available())
    {
      //Reads data from raspberry pi
      byte buffer_read[] = {0,0,0,0,0,0,0,0};
      //delay(10);
      Serial.readBytes(buffer_read,PACKET_SIZE);
      if(buffer_read[0]==0xFE)
      {DataClassifier(buffer_read);}
      else
      {Serial.end();Serial.begin(BAUD_RATE);}
    }
    
  }
  
  void serialWrite(byte data[])
  { 
    //----------------------------
    //Writes data to raspberry pi
    //----------------------------
    if(Serial.available())
    {
      //delay(10);
      PACKET_SIZE = data[1];
      Serial.write(data[],PACKET_SIZE);
      Serial.flush;
    } 
  }
  
  void DataClassifier(byte input[])
  {
    //----------------------------
    //Classify input data to corresponding custom MAVLINK protocole
    //----------------------------
    byte payload;
    //MAVLINK parameters to decode
    if(input[0]==0xFE)//Start Field
    {
      if(input[1]==0x00)//Payload Length
      {
        if(input[2]==0x00)//Packet Seq
        {
          if(input[3]==0xFF)//System ID:Raspberry
          {
            if(input[4]==0xFE)//Component ID:Motor
            {
              if(input[5]==0xFF)//Message ID:Stop
              {
                Serial.println("ACK");
                blinkLEDTest(0);
                //stopMotor();
              }
              else if(input[5]==0xFE)//Message ID:Forward
              {
                Serial.println("ACK");
                blinkLEDTest(1);
                /*
                if(DIRECTION)
                {
                ISDIRECTIONCHANGED=False;
                value = input[6];
                }
                else{DIRECTION=True;ISDIRECTIONCHANGED=True;}
                */
              }
              else if(input[5]==0xFD)//Message ID:Backward
              {
                Serial.println("ACK");
                blinkLEDTest(2);
                /*
                if(!DIRECTION)
                {
                ISDIRECTIONCHANGED=False;
                value = input[6];
                }
                else{DIRECTION=False;ISDIRECTIONCHANGED=TRUE;}
                */
              }
            }
            else if(input[4]==0xFD)//Component ID:Servo
            {
               if(input[5]==0xFF)//Message ID:Angle
              {
                Serial.println("ACK");
                payload = input[6];
              }
              else if(input[5]==0xFE)//Message ID:Default
              {
                Serial.println("ACK");
                payload = input[6];
              }
            }
            else if(input[4]==0xFC)//Component ID:Light
            {
              
            }
          }
        }
      }
    }
  }

  byte mavlink(String componentID,String messageID, long payload)
  {
    //----------------------------
    //It converts payload to byte array according to its component,message IDs
    //----------------------------
    _STARTFIELD = 0xFE;  //Start Field
    _PAYLOADLENGTH = 0x04; //Payload Length Field
    _PACKETSEQUENCE = 0x00;  //Packet Sequence Field
    _CRC = 0xFF; //End Field
    _PAYLOAD = Null;
    // systemID
    _SYSTEMID = 0xFE;
    // componentID
    if(componentID=="MPU_ACCEL")
    {
      _COMPONENTID = 0xFE;
      if(messageID=="X"){_MESSAGEID = 0xFF; _PAYLOAD = payload;}
      else if(messageID=="Y"){_MESSAGEID = 0xFE; _PAYLOAD = payload;}
      else if(messageID=="Z"){_MESSAGEID = 0xFD; _PAYLOAD = payload;}
    }
    else if(componentID=="MPU_ORIENT")
    {
      _COMPONENTID = 0xFD;
      if(messageID=="X"){_MESSAGEID = 0xFF; _PAYLOAD = payload;}
      else if(messageID=="Y"){_MESSAGEID = 0xFE; _PAYLOAD = payload;}
      else if(messageID=="Z"){_MESSAGEID = 0xFD; _PAYLOAD = payload;}
    }
    else if(componentID=="ULTRASONIC")
    {
      _COMPONENTID = 0xFF;
      if(messageID=="DISTANCE"){_MESSAGEID = 0xFF; _PAYLOAD = payload;}
    }
    else if(componentID=="OPTICALNAVIGATOR")	//(It is optional and maybe won't be used.)
    {
      _COMPONENTID = 0xFC;
      if(messageID=="X"){_MESSAGEID = 0xFF ;_PAYLOAD = payload;}
      else if(messageID=="Y"){_MESSAGEID = 0xFE; _PAYLOAD = payload;}
    }
    data = {_STARTFIELD,_PAYLOADLENGTH,_PACKETSEQUENCE,_SYSTEMID,_COMPONENTID,_MESSAGEID,_PAYLOAD,_CRC};
    return data
  }


  void runLED(String command)
  {
    //----------------------------
    //Test run for communication
    //----------------------------
    if(command=="STOP")
    {
      blinkLEDTest(0);
    }
    else if(command=="FORWARD")
    {
      blinkLEDTest(1);
    }
    else if(command=="BACKWARD")
    {
      blinkLEDTest(2);
    }
    
  }
 //End Region




//===========================
//Region Control Methods
//===========================
  void lightControl(int sequence)
  {
    //----------------------------
	//It will control car lights.(It is optional and maybe won't be used.)
	//----------------------------
  }
  

  /* These will probably not used.
	  void motorPID()
	  {
    
	  }
  
	  void servoPID()
	  {
    
	  }
  */


  void motorPWM(int cycle)
  {
    //----------------------------
    //It gets duty cycle as input and converts and writes to esc as PWM value.
    //----------------------------
    //Check direction
    /*
    if(DIRECTION)//Forward direction
    {
      if(ISDIRECTIONCHANGED)
      {
      stopMotor();delay(500);
      //Set motor rotation direction
      }
      //Write the cycle to motor
      motor.writeMicroseconds(cycle);
    }
    else//Backward Direction
    {
      if(ISDIRECTIONCHANGED)
      {
      stopMotor();delay(500);
      //Set motor rotation direction
      }
      //Write the cycle to motor
      motor.writeMicroseconds(cycle);
    }
    */
  }
  
  void servoAngle(int angle)
  {
    //----------------------------
    //Gets angle and writes to servo motor.
    //----------------------------
    //servo.write(angle);
  }

//End Region




//===========================
//Region Sensor
//=========================== 
  double measureDistance()
  {
    //----------------------------
    //Distance is measured and returned as double value using ultrasonic distance sensor.
    //---------------------------- 
  }
  
  void MPU6050()
  {
    //----------------------------
    //Measures acceleration and orientation values from MPU6050.
    //---------------------------- 
  }
//End Region




//===========================
//Region Test
//===========================
void blinkLEDTest(int i)
{
  if(i==0){digitalWrite(redLED,LOW);digitalWrite(yellowLED,LOW);digitalWrite(blueLED,LOW);
            digitalWrite(redLED,HIGH);delay(200);digitalWrite(redLED,LOW);}
  
  if(i==1){digitalWrite(redLED,LOW);digitalWrite(yellowLED,LOW);digitalWrite(blueLED,LOW);
            digitalWrite(yellowLED,HIGH);delay(200);digitalWrite(yellowLED,LOW);}  
  
  if(i==2){digitalWrite(redLED,LOW);digitalWrite(yellowLED,LOW);digitalWrite(blueLED,LOW);
            digitalWrite(blueLED,HIGH);delay(200);digitalWrite(blueLED,LOW);}
}
//End Region

//===========================
// Main Loop
//===========================
void loop() 
{
  //----------------------------
  //It is main loop. It process relevant information as long as arduino runs.
  //----------------------------
  
  //=========================
  //Just for the test
  serialRead();
  delay(5);
  //serialWrite();
  //=========================

  //Take commands from its master over serial
  /*
  serialRead()
  delay(5);
  */
  
  //this is for PID control of the motor
  /*
  Input = analogRead(PIN_INPUT);//PIN_INPUT will either connected
                                //to sensor or gets a variable

  double gap = abs(Setpoint-Input); //distance away from setpoint
  if (gap < 10)
  {  //we're close to setpoint, use conservative tuning parameters
    motorPID.SetTunings(consKp, consKi, consKd);
  }
  else
  {
     //we're far from setpoint, use aggressive tuning parameters
     motorPID.SetTunings(aggKp, aggKi, aggKd);
  }

  motorPID.Compute();
  MotorPWM(Output);
  */  
}
