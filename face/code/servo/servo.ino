/*
  # Face tracking using arduino - Code #
  # Code by Harsh Dethe
  # 09 Sep 2018.
*/

#include<Servo.h>

Servo servoVer; //Vertical Servo
Servo servoHor; //Horizontal Servo

int x;
int y;

int prevX;
int prevY;

int servoX = 100;
int servoY = 20;

void setup()
{
  Serial.begin(9600);
  servoVer.attach(5); //Attach Vertical Servo to Pin 5
  servoHor.attach(6); //Attach Horizontal Servo to Pin 6
  servoVer.write(servoY);
  servoHor.write(servoX);
}

void Pos()
{
  int xMin = 0;
  int xMax = 179;
  int yMin = 20;
  int yMax = 90;
  int xMiddle = (xMin + xMax) / 2;
  int yMiddle = (yMin + yMax) / 2;



  //  servoX = map(x, 0, 640, xMin, xMax);
  //  servoY = map(y, 0, 480, yMax, yMin);

  if (x == 320 && y == 240) {
    servoX = xMiddle;
    servoY = yMiddle;
  }

  if (x < 320) {
    servoX--;
    if (servoX < xMin) {
      servoX = xMin;
    }
  } else if (x > 320) {
    servoX++;
    if (servoX > xMax) {
      servoX = xMax;
    }
  }

  if (y < 240) {
    servoY++;
    if (servoY > yMax) {
      servoY = yMax;
    }
  } else if (y > 240) {
    servoY--;
    if (servoY < yMin) {
      servoY = yMin;
    }
  }

  servoX = min(servoX, xMax);
  servoX = max(servoX, xMin);
  servoY = min(servoY, yMax);
  servoY = max(servoY, yMin);

  servoHor.write(servoX);
  servoVer.write(servoY);
  delay(1);
}

void loop()
{
  if (Serial.available() > 0)
  {
    if (Serial.read() == 'X')
    {
      x = Serial.parseInt();
      if (Serial.read() == 'Y')
      {
        y = Serial.parseInt();
        Pos();
        delay(1);
      }
    }
    while (Serial.available() > 0)
    {
      Serial.read();
    }
  }
}
