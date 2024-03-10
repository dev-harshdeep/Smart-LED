int ldrPin = A0; // Connect the LDR to analog pin A0
int ledPin = 10;

void setup()
{
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    if (Serial.available() > 0)
    {
        String command = Serial.readStringUntil('\n');

        if (command.startsWith("PIN_ON"))
        {
            digitalWrite(ledPin, HIGH);
        }
        else if (command.startsWith("PIN_OFF"))
        {
            digitalWrite(ledPin, LOW);
        }
    }

    // Read the analog value from the LDR
    int ldrValue = analogRead(ldrPin);

    // Send the LDR value through the serial connection
    Serial.print("LDR_VALUE:");
    Serial.println(ldrValue);

    delay(1000); // Adjust the delay based on your requirements
}
