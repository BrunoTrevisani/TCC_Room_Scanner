#include <Arduino.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include "TFMini.h"
#include <ESP32Servo.h>

TFMini tfmini;
Servo myServo;

const int DIR = 12;
const int STEP = 14;
int strength = 0;
int distance = 0;

// Full step = 200; Eighth = 1600; Sixteenth = 3200
const int  steps_per_rev = 1600;
bool cicle = true;
bool servoDirection = 1;

// Reads the serial buffer and converts the bytes into distance in cm and a signal strength scalar
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

// Thread that will continuously execute the motors movement and write the data
void taskFunction(void *pvParameters) {
  if (cicle){
    for (int step = 0; step < steps_per_rev; step++){
      digitalWrite(STEP, HIGH);
      delayMicroseconds(2000);
      digitalWrite(STEP, LOW);
      delayMicroseconds(2000);

      if (servoDirection){
        for(int vertAngle = 12; vertAngle <= 148; vertAngle += 2){
          WriteData(vertAngle, step);
        }
        servoDirection = 0;
      }
      else{
        for(int vertAngle = 148; vertAngle > 12; vertAngle -= 2){
          WriteData(vertAngle, step);
        }
        servoDirection = 1;
      }
    }
    
    cicle = false;
  }

  vTaskDelete(NULL);
}

void setup() {
  myServo.attach(13);
  Serial.begin(115200);

  // Wait serial port be connected.
  while (!Serial) {
    // Semicolon to compiler not ignore while-loop.
    ;
  }  
  
  Serial.println ("Initializing TF Mini...");
  //Initialize the data rate for the SoftwareSerial port
  Serial2.begin(TFMINI_BAUDRATE);  
  //Initialize the TF Mini sensor  
  tfmini.begin(&Serial2);            

  // Set outputs
  pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);

  // Set default direction for step motor
  digitalWrite(DIR, HIGH);

  getTFminiData(&distance, &strength);

  xTaskCreate(
    taskFunction,          // Thread function
    "Task",                // Thread name
    10000,                 // Thread stack size
    NULL,                  // Thread parameter (not used)
    1,                     // Thread priority 
    NULL                   // Thread handle (not used)
  );
}

void loop() {
  // Main thread will continuously consume the input buffer
  if (cicle)
    getTFminiData(&distance, &strength);
}

void WriteData(int vertAngle, int stepMotor){
  myServo.write(vertAngle);
  delay(300);
  Serial.println((String)distance + "," + (String)stepMotor + "," + (String)vertAngle);
}
