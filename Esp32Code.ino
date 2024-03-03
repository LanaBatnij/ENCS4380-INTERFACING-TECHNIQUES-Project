#include <L298NX2.h>

#define enA 12
#define in1 14
#define in2 27
#define Lc1 25
#define Lc2 26

#define enB 15
#define in3 2
#define in4 0
#define Rc1 4
#define Rc2 16

#define irFront 21
#define irLeft 13
#define irRight 22

#define trigPinUSLeft 17    // Trigger for ultrasonic left
#define echoPinUSLeft 5    // Echo for ultrasonic left

#define trigPinUSRight 18    // Trigger for ultrasonic right
#define echoPinUSRight 19    // Echo for ultrasonic right

unsigned short rightMotorSpeed = 110, leftMotorSpeed = 110;

boolean leftWall = false, rightWall = false, frontWall = false;

volatile int rightEncoder = 0;
volatile int leftEncoder = 0;

L298N myLeftMotor(enA, in1, in2);
L298N myRightMotor(enB, in3, in4);

double getDistace(int trigPin, int echoPin){
    double cm ;
  
    //The sensor is triggered by a HIGH pulse of 10 or more microseconds.
    //Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
      
    //Read the signal from the sensor: a HIGH pulse whose
    //duration is the time (in microseconds) from the sending
    //of the ping to the reception of its echo off of an object.
    
    double duration = pulseIn(echoPin, HIGH);
    //Convert the time into a distance
    cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
    return cm;
}

void setup() {
  Serial.begin(115200); //start serial communication
  pinMode(irFront, INPUT);
  pinMode(irLeft, INPUT);
  pinMode(irRight, INPUT);

  pinMode(trigPinUSLeft, OUTPUT);
  pinMode(echoPinUSLeft, INPUT); 

  pinMode(trigPinUSRight, OUTPUT);
  pinMode(echoPinUSRight, INPUT);

  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(Rc1), changeRight, CHANGE);
  attachInterrupt(digitalPinToInterrupt(Lc1), changeLeft, CHANGE);

  /*myRightMotor.setSpeed(rightMotorSpeed);
  myLeftMotor.setSpeed(leftMotorSpeed);
  myRightMotor.forward();
  myLeftMotor.forward();*/
}

void loop() {
  /*int irValue = digitalRead(irFront);
  Serial.print("IR Sensor Value sensor front: ");
  Serial.println(irValue);

  int irValue2 = digitalRead(irLeft);
  Serial.print("IR Sensor Value sensor left: ");
  Serial.println(irValue2);

  int irValue3 = digitalRead(irRight);
  Serial.print("IR Sensor Value sensor right: ");
  Serial.println(irValue3);
  Serial.println();

  delay(1000);*/

  myRightMotor.setSpeed(rightMotorSpeed);
  myLeftMotor.setSpeed(leftMotorSpeed);
  myRightMotor.forward();
  myLeftMotor.forward();
  
  calibrate();

  leftWall = wallLeft();
  rightWall = wallRight();
  frontWall = wallFront();

  if (leftWall && rightWall && frontWall) {
    delay(400);
    turnLeft();
    turnLeft();
    moveForward();
  } else if (leftWall && !rightWall && frontWall) {
    turnRight();
    moveForward();
  } else if(!leftWall && rightWall && frontWall){
    delay(400);
    turnLeft();
    moveForward();
  } else if(!leftWall && rightWall && !frontWall){
    moveForwardNoCalibration();
    turnLeft();
    moveForward();
  } else if(!leftWall && !rightWall && frontWall){
    delay(400);
    turnLeft();
    moveForward();
  } else if (!leftWall && !rightWall && !frontWall) {
    moveForwardNoCalibration();
    turnLeft();
    moveForward();
  }
}

void changeRight(){
  rightEncoder++;
}

void changeLeft(){
  leftEncoder++;
}

//detect if there is a wall to the front
boolean wallFront() {
    return digitalRead(irFront) == 0;
}

//detect if there is a wall to the left
boolean wallLeft() {
    return digitalRead(irLeft) == 0;
}

//chack if there is a wall to the right
boolean wallRight() {
    return digitalRead(irRight) == 0;
}

void moveForward(){
    myRightMotor.setSpeed(120);
    myLeftMotor.setSpeed(120);
    myRightMotor.forward();
    myLeftMotor.forward();
    leftEncoder = 0;
    while(leftEncoder <= 133){ // here
      calibrate();
    }
}
 
void moveForwardNoCalibration(){
    myRightMotor.setSpeed(rightMotorSpeed);
    myLeftMotor.setSpeed(leftMotorSpeed);
    myRightMotor.forward();
    myLeftMotor.forward();
    leftEncoder = 0;
    while(leftEncoder <= 130);
}

void turnLeft() { 
  myRightMotor.stop();
  myLeftMotor.stop();
  delay(1500);
  myRightMotor.setSpeed(200);
  myLeftMotor.setSpeed(200);
  myRightMotor.forward();
  myLeftMotor.backward();
  rightEncoder = 0;
  while(rightEncoder <= 52);
  myRightMotor.stop();
  myLeftMotor.stop();
  delay(1000);
}

void turnRight() {
  myRightMotor.stop();
  myLeftMotor.stop();
  delay(1500);
  myRightMotor.setSpeed(200);
  myLeftMotor.setSpeed(200);
  myLeftMotor.forward();
  myRightMotor.backward();
  leftEncoder = 0;
  while(leftEncoder <= 48);
  myRightMotor.stop();
  myLeftMotor.stop();
  delay(1000);
}

void calibrate() {
  double leftUSDistance = getDistace(trigPinUSLeft, echoPinUSLeft);
  double RightUSDistance = getDistace(trigPinUSRight, echoPinUSRight);

  double variableToWallDistance = 3.3;
  double variableToWallDistanceL = 3.3;

  if (leftUSDistance <= variableToWallDistanceL) {
    myRightMotor.setSpeed(rightMotorSpeed);
    myLeftMotor.setSpeed(leftMotorSpeed);
    myRightMotor.backward();
    myLeftMotor.forward();

    while (leftUSDistance <= variableToWallDistanceL) {
      leftUSDistance = getDistace(trigPinUSLeft, echoPinUSLeft);
    }
  } else if (RightUSDistance <= variableToWallDistance) {
    myRightMotor.setSpeed(rightMotorSpeed);
    myLeftMotor.setSpeed(leftMotorSpeed);
    myRightMotor.forward();
    myLeftMotor.backward();

    while (RightUSDistance <= variableToWallDistance) {
      RightUSDistance = getDistace(trigPinUSRight, echoPinUSRight);
    }
  } else {
    
  myRightMotor.setSpeed(rightMotorSpeed);
  myLeftMotor.setSpeed(leftMotorSpeed);
  myRightMotor.forward();
  myLeftMotor.forward();
  }
}
