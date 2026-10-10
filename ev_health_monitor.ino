#include <OneWire.h>
#include <DallasTemperature.h>

// ---------- Pins ----------
#define TEMP_PIN 4
#define VOLTAGE_PIN 34
#define CURRENT_PIN 35

// ---------- Temperature Sensor ----------
OneWire oneWire(TEMP_PIN);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);

  sensors.begin();
  analogReadResolution(12);

  Serial.println("=================================");
  Serial.println("   EV ELECTRICAL HEALTH MONITOR");
  Serial.println("=================================");
}

void loop() {

  // ---------- Temperature ----------
  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);

  if (temperature == DEVICE_DISCONNECTED_C) {
      Serial.println("ERROR: Temperature sensor disconnected");
      return;
  }

  // ---------- Voltage ----------
  int voltageADC = analogRead(VOLTAGE_PIN);

  // Simulated EV voltage: 300V - 420V
  float voltage = 300.0 + (voltageADC / 4095.0) * 120.0;

  // ---------- Current ----------
  int currentADC = analogRead(CURRENT_PIN);

  // Simulated current: 0A - 100A
  float current = (currentADC / 4095.0) * 100.0;

  // ---------- Power ----------
  float power = voltage * current;

  // ---------- System Status ----------
  String status;

  if (temperature < 45 &&
      voltage >= 330 &&
      voltage <= 420 &&
      current <= 80) {

    status = "NORMAL";
  }
  else {

    status = "ALERT";
  }

  // ---------- Send structured data ----------
Serial.print(temperature, 2);
Serial.print(",");
Serial.print(voltage, 2);
Serial.print(",");
Serial.print(current, 2);
Serial.print(",");
Serial.print(power, 2);
Serial.print(",");
Serial.println(status);

  delay(2000);
}