#include <Arduino.h>
#include <Servo.h>

void innerServoHold(unsigned long holdDuration);
void outerServoHold(unsigned long holdDuration);
void gatherData();
void printData();

Servo servo[2];  // create servo object to control a servo
int base_pin[2] = {9, 10};
int spos[2] = {0,0};    // variable to store the servo position
int a_limit = 90; // Angle limit of the servo
int offset = 45;
unsigned long duration = 50;
bool updated[2] = {false, false};

int count, total = 0;
int rolling[10]; // Rolling average things
float avg;

int anVal = 0; // Analog read value

unsigned long lastTime[2] = {0, 0};
void setup() {
		Serial.begin(9600);
		servo[0].attach(base_pin[0]);
		servo[1].attach(base_pin[1]);

		// Initialize the rolling average list as zero list
		for(count = 0; count < 10; count++) {
				rolling[count] = 0;
		}
		count = 0;
}

void loop() {
		innerServoHold(duration);
		if(updated[0]) {
				spos[0] = (spos[0]+1)%a_limit;
				updated[0] = false;
		}
}

void innerServoHold(unsigned long holdDuration) {
		if (millis() - lastTime[0] < holdDuration * a_limit) {
				servo[0].write(spos[0]+offset);
				outerServoHold(holdDuration);
				if(updated[1]) {
						spos[1] = (spos[1]+1)%a_limit;
						updated[1] = false;
				}
		}
		else {
				printData();
				lastTime[0] = millis();
				updated[0] = true;
		}
}

void outerServoHold(unsigned long holdDuration) {
		if (millis() - lastTime[1] < holdDuration) {
				servo[1].write(spos[1]+offset);
				gatherData();
		}
		else {
				printData();
				lastTime[1] = millis();
				updated[1]=true;
		}
}

void gatherData() {
		anVal = analogRead(A0);
		total -= rolling[count];
		total += anVal;
		rolling[count] = anVal;
		avg = total/10.0;
		// Serial.println(anVal);
		count = (count+1)%10;
}

void printData() {
		String delim = ",";
		String s = spos[0]+delim+spos[1]+delim+avg;
		Serial.println(s);
}
