// Translating button clicks into morse code

#include <LiquidCrystal.h> // So we can use LCD to display the word
LiquidCrystal lcd(7, 8, 9, 10, 11, 12); // digital pins we're connecting to LCD

const int button1 = 2;
const int button2 = 3;
const int potentiometer = A0;
const int ledPin = 5;
volatile int chars = 0; // # chars in current letter
volatile int letters = 0; // # letters in word
bool left = false; // initializing state variables for each 3 stages of the potentiometer so we can track when we change states
bool middle = false;
bool right = false;
int currentLetter[4]; // string w/ every button press that we translate to a letter; max len 4 
char currentWord[32]; // string w/ every letter input; max length of 32
unsigned long lastDebounceTime = 0; // so we can debounce the button
unsigned long debounceDelay = 100;

void setup() {

	Serial.begin(9600);
	Serial.println("Beginning now");
  lcd.begin(16, 2); // set up the LCD's number of columns and rows:
	pinMode(button1, INPUT);
	pinMode(button2, INPUT);
  pinMode(ledPin, OUTPUT);
	attachInterrupt(digitalPinToInterrupt(button1), button1Pushed, RISING); // button1Pushed() occurs if button 1 goes from LOW --> HIGH
	attachInterrupt(digitalPinToInterrupt(button2), button2Pushed, RISING); // button2Pushed() occurs if button 2 goes from LOW --> HIGH
}

void loop() {
	int pwm = analogRead(potentiometer); // get potentiometer reading
	Serial.print("Potentiometer reading: ");
	Serial.println(pwm);
	if (pwm > 900) { // Zone 1
		left = true;
		if (middle == true || right == true) { // This means we changed zones
			Serial.println("Word stopped");
			middle = false;
			right = false;
      for (int i = 0; i < letters; i++) { // Print word to serial monitor
        Serial.println(currentWord[i]);
      }
      for (int i = 0; i < letters; i++) { // Print word to LCD
        lcd.print(currentWord[i]);
      }
      
		}
	}
	else if (pwm < 100) { // Zone 3
		right = true;
		if (left == true || middle == true) { // This means we changed zones
			if (chars == 0) {
			// Word start zone
			Serial.println("Word start");
			}
			// Letter start zone
			Serial.println("Letter start");
			left = false;
			middle = false;
      digitalWrite(ledPin, HIGH); // turn on LED
		}
	}
	else { // Zone 2
		middle = true;
		if (left == true || right == true) { // This means we changed zones
			// Letter stop zone
			Serial.println("Letter stop");
			left = false;
			right = false;
      digitalWrite(ledPin, LOW); // turn off LED
      
      // If there's less than 4 inputs, fill them with 0's to act as null chars
      while (chars < 4) {
        currentLetter[chars] = 0;
        chars++;
      }

      for (int i = 0; i < 4; i++) {
        Serial.println(currentLetter[i]); // Print out our array to serial monitor
      }
      char letter;

      // Compare our string to morse code and see what letter it is
      if (currentLetter[0] == 1) { // Codes that start wtih dot
        if (currentLetter[1] == 1) { // Dot, dot
          if (currentLetter[2] == 1) { // Dot, dot, dot
            if (currentLetter[3] == 1) { // Dot, dot, dot, dot
              letter = 'h';
            }
            else if (currentLetter[3] == 2) { // Dot, dot, dot, dash
              letter = 'v';
            }
            else { // Dot, dot, dot
              letter = 's';
            }
          }
          else if (currentLetter[2] == 2) { // Dot, dot, dash
            if (currentLetter[3] == 1) { // Dot, dot, dash, dot
              letter = 'f';
            }
            else if (currentLetter[3] == 0) { // Dot, dot, dash
              letter = 'u';
            }
          }
          else { // Dot, dot
            letter = 'i';
          }
        }
        else if (currentLetter[1] == 2) {  // Dot, dash
          if (currentLetter[2] == 1) { // Dot, dash, dot
            if (currentLetter[3] == 1) { // Dot, dash, dot, dot
              letter = 'l';
            }
            else if (currentLetter[2] == 0) { // Dot, dash, dot
              letter = 'r';
            }
          }
          else if (currentLetter[2] == 2) { // Dot, dash, dash
            if (currentLetter[3] == 1) { // Dot, dash, dash, dot
              letter = 'p';
            }
            else if (currentLetter[3] == 2) { // Dot, dash, dash, dash
              letter = 'j';
            }
            else { // Dot, dash, dash
              letter = 'w';
            }
          }
          else { // Dot, dash
            letter = 'a';
          }
        }
        else {  // Dot. 
          letter = 'e';
        }
      }
      else { // Codes that start with dash
        if (currentLetter[1] == 1) { // Dash, dot
          if (currentLetter[2] == 1) { // Dash, dot, dot
            if (currentLetter[3] == 1) { // Dash, dot, dot, dot
              letter = 'b';
            }
            else if (currentLetter[3] == 2) { // Dash, dot, dot, dash
              letter = 'x';
            }
            else { // Dash, dot, dot
              letter = 'd';
            }
          }
          else if (currentLetter[2] == 2) { // Dash, dot, dash
            if (currentLetter[3] == 1) { // Dash, dot, dash, dot
              letter = 'c';
            }
            else if (currentLetter[3] == 2) { // Dash, dot, dash, dash
              letter = 'y';
            }
            else { // Dash, dot, dash
              letter = 'k';
            }
          }
          else { // Dash, dot
            letter = 'n';
          }
        }
        else if (currentLetter[1] == 2) { // Dash, dash
          if (currentLetter[2] == 1) { // Dash, dash, dot
            if (currentLetter[3] == 1) { // Dash, dash, dot, dot
              letter = 'z';
            }
            else if (currentLetter[3] == 2){ // Dash, dash, dot, dash
              letter = 'q';
            }
            else { // Dash, dash, dot
              letter = 'g';
            }
          }
          else if (currentLetter[2] == 2) { // Dash, dash, dash
            letter = 'o';
          }
          else { // Dash, dash
            letter = 'm';
          }
        }
        else {
          letter = 't'; // Dash
        }
      }

      currentWord[letters] = letter; // append word array with the letter we just determined
      letters++;
      for (int i = 0; i < 4; i++) {
        currentLetter[i] = 0; // Reset currentLetter array
      }
      chars = 0; // Reset character counter
		}
	}
  Serial.println("You have 5 seconds to move the dial.");
	delay(5000); // 5 second delay between reads to give us time to move the dial to where we want it
}
void button1Pushed() {
  if (millis() - lastDebounceTime > debounceDelay) { // Debounce the button
    if (right == true) { // make sure we're in zone 3
      Serial.println("Button 1 pushed");
      currentLetter[chars] = 1; // append letter string with a 1
      Serial.println(currentLetter[chars]);
      chars++;
	  }
    lastDebounceTime = millis();
  }
}
void button2Pushed() {
  if (millis() - lastDebounceTime > debounceDelay) { // Debounce the button
    if (right == true) { // make sure we're in zone 3
      Serial.println("Button 2 pushed");
      currentLetter[chars] = 2; // append letter string with a 2
      Serial.println(currentLetter[chars]);
      chars++;
    }
    lastDebounceTime = millis();
  }
}