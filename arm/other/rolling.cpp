#include <Arduino.h>
#include <Servo.h>

Servo base_mount;  // create servo object to control a servo
int base_pin = 9;
int pos = 0;    // variable to store the servo position

int count, total = 0;
int rolling[10]; // Rolling average things
float avg;

int anVal = 0; // Analog read value

void setup() {
		Serial.begin(9600);
		base_mount.attach(base_pin);

		// Initialize the rolling average list as zero list
		for(count = 0; count < 10; count++) {
				rolling[count] = 0;
		}
		count = 0;
}

void loop() {
		anVal = analogRead(A0);
		total -= rolling[count];
		total += anVal;
		rolling[count] = anVal;
		avg = total/10.0;
		Serial.println(anVal);
		count = (count+1)%10;
}
