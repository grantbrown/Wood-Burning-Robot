
#include <AFMotor.h>
#include <Stepper.h>
//Define pins for sparkfun driver


#define motorPin1 A3
#define motorPin2 A2
#define MICROSTEPS 8
#define motorSteps 200

AF_Stepper step_motor(200, 1);
AF_DCMotor z_motor(3);

int inByte = 0;         // incoming serial byte
int inX = 0;
int inY = 0;
int maxX = 0;
int maxY = 0;
int cells_burned = 0;


int handshaken = 0;
char inChar;
int X = 0;
int Y = 0;

int led = A0;
int button = A1;

unsigned int maxVal;
unsigned int inInt;
int haveMax = 0;
int nextVal;
int del;

Stepper stepper2(motorSteps, motorPin1,motorPin2); 


void setup()
{
  pinMode(led, OUTPUT);
  pinMode(button, INPUT); 

  // start serial port at 9600 bps:
  step_motor.setSpeed(31);  // 1 rpm  
  stepper2.setSpeed(15);
  z_motor.setSpeed(100);
  z_motor.run(RELEASE);
  Serial.begin(57600);
  establishContact();  // send a byte to establish contact until receiver responds  
}

int go(int x, int y)
{
  return(move_x(x) + move_y(y));
}




int move_x(int x)
{
  int steps = x - X;
  X = x;
  if (steps == 0)
  {
    return(1);
  }
  else if (steps < 0)
  {
    step_motor.step(steps*(-1), BACKWARD, DOUBLE);
  }
  else if (steps > 0)
  {
    step_motor.step(steps, FORWARD, DOUBLE);
  }
  return(1);
}

int move_y(int y)
{
  
  
  int steps = y - Y;
  int dir = (steps > 0) ? 1 : (-1);
  Y = y;
  if (steps == 0)
  {
    return(1);
  }
  else
  {
    for (int i = 0; i < abs(steps); i ++)
    {
      stepper2.step(dir);
      delay(10);
    }
    //Shake
    stepper2.step(dir);
    stepper2.step((-1)*dir);
    stepper2.step(dir);
    stepper2.step((-1)*dir);
    stepper2.step(dir);
    stepper2.step((-1)*dir);

  }
  return(1);
}



int burn(int ms)
{
  if (ms <= 10)
  {
    return(0);
  }
  else
  {
    delay(50);
    for (int i = 0; i < 8; i++)
    {
      z_motor.run(RELEASE);
      delay(4);
      z_motor.run(BACKWARD);
      delay(6);
      
    }
    //delay(ms/13);
    for (unsigned int i = 0; i < (ms/2500)*(ms/2500); i++)
    {
       z_motor.run(BACKWARD);
       delay(1);
       z_motor.run(RELEASE);
       delay(3);
    }
    //delay(ms*ms/50);
    for (int i = 0; i < 20; i++)
    {
      z_motor.run(FORWARD);
      delay(1);
      z_motor.run(RELEASE);
      delay(1);
    }
    
//    z_motor.run(FORWARD);
//    delay(30);
//    z_motor.run(RELEASE);
      return(1);
  }
}


void loop()
{
  
  // if we get a valid byte, read analog ins:
  if (Serial.available() > 0) 
  {
    if (!handshaken)
    {
      handshaken = 1;
      Serial.write("B");
    }
    if (!haveMax)
    {
      haveMax = 1;
      inInt = Serial.parseInt();
      maxVal = inInt;
      Serial.print("Setting maximum to: ");
      Serial.print(inInt);
      Serial.println(". Done");
      Serial.println("X");
      maxX = Serial.parseInt();
      Serial.println("Y");
      maxY = Serial.parseInt();
      //Move around the periphs
      move_x(maxX);
      move_y(maxY);
      move_x(0);
      move_y(0);
      Serial.println("N");
      
      
      /*
      Serial.print(", breaks will be: ");
      for (int i = 0; i < 20; i++)
      {
        Serial.print(i*(inInt/20));
        Serial.print(",");
      }
      */

      
    }
  }  
   if (haveMax)
  {
    if (digitalRead(button) == HIGH | cells_burned > 0)
    {
      cells_burned += 1;
      Serial.println("N");
      inInt = Serial.parseInt();
      Serial.println("X");
      inX = Serial.parseInt();
      Serial.println("Y");
      inY = Serial.parseInt();
      move_x(inX);
      //X = inX;
      //if (Y != inY)
      //{
      //  move_x(0);
      //}
      move_y(inY);
      //Y = inY;
      digitalWrite(led,HIGH);
      if (inInt == 0)
      {
        delay(0);
      }
      else
      {
        unsigned int del = 0;
        int flash = 0;
        for (int i = 0; i < 50; i++)
        {
          if (inInt < i*(maxVal/50))
          {
            // delay(del);
            flash = 1;
            break;
          }
          del += maxVal/50;
        }
        burn(del);
      }
      digitalWrite(led, LOW);  
      


      /*step_motor.step(20, FORWARD, DOUBLE); */
    }
  }
}


void establishContact() {
  while (Serial.available() <= 0) {
    Serial.write('A');   // send a capital A
    delay(100);
  }
}

