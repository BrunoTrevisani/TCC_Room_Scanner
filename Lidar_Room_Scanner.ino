#include <ESP32Servo.h>
#include "TFMini.h"

TFMini tfmini;
Servo myServo;

const int DIR = 12;
const int STEP = 14;

bool cicle = true;

// Full step = 200; Eighth = 1600; Sixteenth = 3200
const int  steps_per_rev = 400;

void getTFminiData(int* distance, int* strength)
{
  static int i = 0;
  int j = 0;
  int checksum = 0;
  static int rx[9];
  
  if (Serial2.available())
  {
    rx[i] = Serial2.read();
    if (rx[0] != 0x59)
    {
      i = 0;
    }
    else if (i == 1 && rx[1] != 0x59)
    {
      i = 0;
    }
    else if (i == 8)
    {
      for (j = 0; j < 8; j++)
      {
        checksum += rx[j];
      }
      if (rx[8] == (checksum % 256))
      {
        *distance = rx[2] + rx[3] * 256;
        *strength = rx[4] + rx[5] * 256;
      }
      i = 0;
    }
    else
    {
      i++;
    }
  }
}
 
 
void setup()
{
  myServo.attach(13);
  Serial.begin(115200);       //Initialize hardware serial port (serial debug port)

  // Wait serial port be connected.
  while (!Serial) {
    // Semicolon to compiler not ignore while-loop.
    ;
  };      
  
  Serial.println ("Initializing...");
  Serial2.begin(TFMINI_BAUDRATE);    //Initialize the data rate for the SoftwareSerial port
  tfmini.begin(&Serial2);            //Initialize the TF Mini sensor

  pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);
  digitalWrite(DIR, 0);
}
int direction = 1;
void loop()
{
  if (cicle){
    for (int i = 0; i<steps_per_rev; i++){

      digitalWrite(STEP, HIGH);
      delayMicroseconds(2000);
      digitalWrite(STEP, LOW);
      delayMicroseconds(2000);

      if (direction == 1){
        for(int vertAngle = 2; vertAngle <= 130; vertAngle += 2){
          Execute(i, vertAngle);
        }
        direction = 0;
      }
      else{
        for(int vertAngle = 130; vertAngle > 0; vertAngle -= 2){
          Execute(i, vertAngle);
        }
        direction = 1;
      }


      delay(500);
      cicle = false;
    }
  }
}

void Execute(int i, int vertAngle){
  int printedDistance = 0;
  myServo.write(vertAngle);


  delay(100);

  for (int interaction = 0; interaction < 25; interaction++){
    int strength = 0;
    int distance = 0;
    bool hasWrongRead = false;

    getTFminiData(&distance, &strength);
    while (!distance) { getTFminiData(&distance, &strength); }

    printedDistance = distance;
    hasWrongRead = printedDistance > 1000;

    if (hasWrongRead) {
      Serial.println("Reading error, distance=" + (String)distance);

      while (distance > 1000){
        getTFminiData(&distance, &strength);
      }
    }

    delay(50);
  }

  Serial.println((String)printedDistance + ", " + (String)i + ", " + (String)vertAngle);
}
