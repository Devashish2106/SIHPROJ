int soilPin = A0;   // Soil moisture sensor connected to A0
int relayPin = 8;   // Relay control pin

void setup() {
  pinMode(soilPin, INPUT);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);
  Serial.begin(9600);
}

void loop() {
  int soilValue = analogRead(soilPin); // Read soil moisture value
  Serial.println(soilValue);

  if (soilValue < 500) {
    // Soil is dry, open the valve (adjust the threshold as needed)
    digitalWrite(relayPin, HIGH);
    delay(5000);
  } else {
    // Soil is wet, close the valve
    digitalWrite(relayPin, LOW);
    delay (5000);
  }

  delay(1000); // Delay for 1 second before the next reading
}
