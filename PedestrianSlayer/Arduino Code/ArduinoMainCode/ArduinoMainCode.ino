//=====================
//Region Libraries
//=====================
  //some libraries should be downloaded
  #include <Servo.h>
  #include <PID_v1.h>
//=====================
//Region Configuration Tab
//=====================
  const int redLED = 8;
  const int yellowLED = 9;
  const int blueLED = 10;
  const int redLED2 = 7;

  bool DIRECTION = true;            //set to forward direction
                                    //(false value is backward direction)
  bool ISDIRECTIONCHANGED = false;
  
  //Motor Configuration
  const int MOTOR_PIN = 9;
  Servo motor;
  
  //Servo Configuration
  const int SERVO_PIN = 10;
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
  const int BRAKE_LIGHT_PIN = 3;
  const int LEFT_TURNING_PIN = 4;
  const int RIGHT_TURNING_PIN = 5;
  const int HIGH_BEAM_PIN = 6;
  
  /*
   * It is moved to Raspberry Pi
  //Ultrasonic Configuration
  const int ULTRAS_TRIG = 7;
  const int ULTRA_ECHO = 8;
  */
  
  // Speed Sensor Configuration
  int SPEED_INT = 2;
  volatile int SPEED_IMPULSE;
  
  
  //Serial Configuration
  const int BAUD_RATE = 19200;
  int PACKET_SIZE = 8;
//End Region

//Declare methods
void serialRead();
void serialWrite(byte data[]);
void HEXClassifier(byte input[]);
byte mavlink(String componentID,String messageID, long payload);

void setup() {
  //=====================
  // This is test code:
  //=====================
  pinMode(redLED,OUTPUT);
  pinMode(yellowLED,OUTPUT);
  pinMode(blueLED,OUTPUT);
  pinMode(redLED2,OUTPUT);
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
//Region Test
//===========================
void blinkLEDTest(int i)
{
  if(i==0){digitalWrite(redLED,LOW);digitalWrite(yellowLED,LOW);digitalWrite(blueLED,LOW);
            digitalWrite(redLED,HIGH);delay(200);digitalWrite(redLED,LOW);
            //byte speed_data = mavlink("SPEEDSENSOR","V",(float)4.0);
            //serialWrite(speed_data);delay(200);
            }
  
  if(i==1){digitalWrite(redLED,LOW);digitalWrite(yellowLED,LOW);digitalWrite(blueLED,LOW);
            digitalWrite(yellowLED,HIGH);delay(200);digitalWrite(yellowLED,LOW);}  
  
  if(i==2){digitalWrite(redLED,LOW);digitalWrite(yellowLED,LOW);digitalWrite(blueLED,LOW);
            digitalWrite(blueLED,HIGH);delay(200);digitalWrite(blueLED,LOW);}
}

//===========================
//End Region
//===========================

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
      
      Serial.flush();
      PACKET_SIZE = sizeof(data);//Get length of the transmitted data
      Serial.write(data,PACKET_SIZE);
      delay(10);
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
                blinkLEDTest(0);
                //stopMotor();
              }
              else if(input[5]==0xFE)//Message ID:Forward
              {
                blinkLEDTest(1);

                if(DIRECTION)
                {
                  ISDIRECTIONCHANGED=false;
                  payload = input[6];
                  
                  forwardMotor(payload);
                }
                else
                {
                  DIRECTION=true;
                  ISDIRECTIONCHANGED=true;
                }                
              }
              else if(input[5]==0xFD)//Message ID:Backward
              {
                blinkLEDTest(2);
                
                if(!DIRECTION)
                {
                  ISDIRECTIONCHANGED=false;
                  payload = input[6];
                  
                  backwardMotor(payload);
                }
                else{DIRECTION=false;ISDIRECTIONCHANGED=true;}
                
              }
            }
            else if(input[4]==0xFD)//Component ID:Servo
            {
               if(input[5]==0xFF)//Message ID:Angle
              {
                payload = input[6];
                servoAngle(payload);
              }
              else if(input[5]==0xFE)//Message ID:Default
              {
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
    byte _STARTFIELD = 0xFE;  //Start Field
    byte _PAYLOADLENGTH = 0x04; //Payload Length Field
    byte _PACKETSEQUENCE = 0x00;  //Packet Sequence Field
    byte _COMPONENTID = 0x00;
    byte _MESSAGEID = 0x00;
    byte _PAYLOAD = 0x00;
    byte _CRC = 0xFF; //End Field
    // systemID
    byte _SYSTEMID = 0xFE;
    // componentID
    if(componentID=="MPU_ACCEL")
    {
      byte _COMPONENTID = 0xFE;
      if(messageID=="X"){_MESSAGEID = 0xFF;_PAYLOAD = payload;}
      else if(messageID=="Y"){_MESSAGEID = 0xFE;_PAYLOAD = payload;}
      else if(messageID=="Z"){_MESSAGEID = 0xFD;_PAYLOAD = payload;}
    }
    else if(componentID=="MPU_ORIENT")
    {
      byte _COMPONENTID = 0xFD;
      if(messageID=="X"){_MESSAGEID = 0xFF;_PAYLOAD = payload;}
      else if(messageID=="Y"){_MESSAGEID = 0xFE;_PAYLOAD = payload;}
      else if(messageID=="Z"){_MESSAGEID = 0xFD;_PAYLOAD = payload;}
    }
    else if(componentID=="ULTRASONIC")
    {
      byte _COMPONENTID = 0xFF;
      if(messageID=="DISTANCE"){_MESSAGEID = 0xFF; _PAYLOAD = payload;}
    }
    else if(componentID=="SPEEDSENSOR")  //(It is optional and maybe won't be used.)
    {
      byte _COMPONENTID = 0xFC;
      if(messageID=="V"){_MESSAGEID = 0xFF ;_PAYLOAD = payload;}
    }
    int data_length = int(_PAYLOADLENGTH)+7;
    byte data[data_length] = {_STARTFIELD,_PAYLOADLENGTH,_PACKETSEQUENCE,_SYSTEMID,_COMPONENTID,_MESSAGEID,_PAYLOAD,_CRC};
    return data[data_length];
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
//===========================
//End Region
//===========================



//===========================
//Region Control Methods
//===========================
  void lightControl(int sequence)
  {
    //----------------------------
  //It will control car lights.(It is optional and maybe won't be used.)
  //----------------------------
  }

  void forwardMotor(int payload)
  {
    //Map duty cycle to PWM range
    int targetPWM = map(payload, 0, 100, 1400, 1250);
    
    //Get angular speed of the wheel
    //w_wheel = ;
    /*
     double gap = abs(w_target-w_wheel); //distance away from setpoint
    if (gap < 10)
    { 
      //we're close to setpoint, use conservative tuning parameters
      motorPID.SetTunings(consKp, consKi, consKd);
    }
    else
    {
       //we're far from setpoint, use aggressive tuning parameters
       motorPID.SetTunings(aggKp, aggKi, aggKd);
    }
  
    motorPID.Compute();
    motorPWM(PWM,1)*/
    motorPWM(targetPWM,1);
  }

  void backwardMotor(int payload)
  {


    //Get angular speed of the wheel
    double w_wheel = 0;
    double w_target = 0;

    
    double gap = abs(w_target-w_wheel); //distance away from setpoint
    if (gap < 10)
    { 
      //we're close to setpoint, use conservative tuning parameters
      motorPID.SetTunings(consKp, consKi, consKd);
    }
    else
    {
       //we're far from setpoint, use aggressive tuning parameters
       motorPID.SetTunings(aggKp, aggKi, aggKd);
    }
    double PWM=0;
    motorPID.Compute();
    motorPWM(PWM,0);
  }

  void startMotor(int m_direction)
  {
    if(m_direction)   // from 0 direction to 1
    {
      for(int i=1400 ; i>=1340 ; i-=10)
      {
        motorPWM(i,1);
        delay(8);
      }
    }
    else if(m_direction)  // from 1 direction to 0
    
    {
      for(int i=1400 ; i<=1460 ; i+=10)
      {
        motorPWM(i,1);
        delay(8);
      }
    }
  }
  
  void stopMotor()
  {
    motorPWM(1400,1);
  } 

  void motorPWM2(int w_target)
  {
  /*This methpd gets target and actual angular velocity fo the car. Then, converts to PWM value. 
  */
    int w_wheel=0;
    double gap = abs(w_target-w_wheel); //distance away from setpoint
    if (gap < 10)
    { 
      //we're close to setpoint, use conservative tuning parameters
      motorPID.SetTunings(consKp, consKi, consKd);
    }
    else
    {
       //we're far from setpoint, use aggressive tuning parameters
       motorPID.SetTunings(aggKp, aggKi, aggKd);
    }
  
    motorPID.Compute();
    MotorPWM(Output,1);
  }
  
  void motorPWM(int pwm, bool direction)
  {
    //----------------------------
    //It gets duty cycle as input and converts and writes to esc as PWM value.
    //----------------------------
    
    //Check directions
    if(DIRECTION)//Forward direction
    {
      if(ISDIRECTIONCHANGED)//If direction is changed
      {
        //Stop the motor for a while
        stopMotor();delay(1500);
        //Set motor rotation direction
      }
        //Map angular velocity to PWM range
        int targetPWM = map(cycle, 0, 100, 1400, 1550);
        //Write the cycle to motor
        motor.writeMicroseconds(targetPWM);
    }
    else//Backward Direction
    {
      if(ISDIRECTIONCHANGED)//If direction is changed
      {
        //Stop the motor for a while
        stopMotor();delay(1500);
        //Set motor rotation direction
      }
        //Map angular velocity to PWM range
        int targetPWM = map(cycle, 0, 100, 1400, 1550);
        //Write the cycle to motor
        motor.writeMicroseconds(targetPWM);
    }
    
  }
  
  void servoAngle(int angle)
  {
    //----------------------------
    //Gets angle and writes to servo motor.
    //----------------------------
    //servo.write(angle);
  }
//===========================
//End Region
//===========================



//===========================
//Region Sensor
//=========================== 
  /*
  void MPU6050()
  {
    //----------------------------
    //Measures acceleration and orientation values from MPU6050.
    //---------------------------- 
  }*/


  void speedSensor()
  {

  }
//===========================
//End Region
//===========================


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
