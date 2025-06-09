#include <DHT.h>
#include <SoftwareSerial.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// === ПИНЫ ===
#define DHTPIN 2          // DHT22 (внутренняя температура)
#define DHTTYPE DHT22     // Модель DHT

#define LIGHT_PIN A0      // Аналоговый вход для датчика света

#define CO2_RX_PIN 10     // RX пин для MH-Z19B (через делитель напряжения!)
#define CO2_TX_PIN 11     // TX пин для MH-Z19B

#define ONE_WIRE_BUS 3    // Пин для DS18B20 (наружная температура)

// === ОБЪЕКТЫ ===
DHT dht(DHTPIN, DHTTYPE);
SoftwareSerial co2Serial(CO2_RX_PIN, CO2_TX_PIN);  // RX, TX
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// === ПЕРЕМЕННЫЕ ===
float indoor_temp = 0;
float outdoor_temp = 0;
int light = 0;
int co2 = 0;

// Интервал обновления данных
unsigned long sendInterval = 5000; // каждые 5 секунд
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(115200);     // Для связи с компьютером
  co2Serial.begin(9600);    // Для связи с MH-Z19B
  dht.begin();
  sensors.begin();

  // Если DS18B20 не найден
  if (!sensors.getAddress(NULL, 0)) {
    Serial.println("DS18B20 не найден!");
  }
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= sendInterval) {
    previousMillis = currentMillis;

    // === СЧИТЫВАНИЕ С ДАТЧИКОВ ===
    indoor_temp = dht.readTemperature();   // °C
    light = analogRead(LIGHT_PIN);         // 0-1023 (аналоговое значение)

    sensors.requestTemperatures();
    outdoor_temp = sensors.getTempCByIndex(0);  // Температура с DS18B20

    co2 = getCO2();  // Чтение CO2 с MH-Z19B

    // === ФОРМИРОВАНИЕ СТРОКИ ДАННЫХ ===
    String dataString = "indoor_temp=" + String(indoor_temp, 1) +
                        ",outdoor_temp=" + String(outdoor_temp, 1) +
                        ",light=" + String(light) +
                        ",co2=" + String(co2);

    // === ОТПРАВКА ДАННЫХ НА КОМПЬЮТЕР ===
    Serial.println(dataString);
  }
}

// === ФУНКЦИЯ ЧТЕНИЯ CO2 С MH-Z19B ===
int getCO2() {
  byte cmd[9] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79};
  byte response[9];

  co2Serial.write(cmd, 9);
  delay(100);

  if (co2Serial.available() >= 9) {
    co2Serial.readBytes(response, 9);
    if (response[0] == 0xFF && response[1] == 0x86) {
      int co2Value = response[2] * 256 + response[3];
      return co2Value;
    }
  }

  return -1; 
}