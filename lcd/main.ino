#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

int fiveHour = -1;
int sevenDay = -1;
int prevFiveHour = -1;
int prevSevenDay = -1;

byte fullBlock[8] = {
  B11111, B11111, B11111, B11111,
  B11111, B11111, B11111, B11111
};

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.createChar(0, fullBlock);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("5H[          ]  ");
  lcd.setCursor(0, 1);
  lcd.print("7D[          ]  ");
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    int comma = line.indexOf(',');
    if (comma > 0) {
      int five = line.substring(0, comma).toInt();
      int seven = line.substring(comma + 1).toInt();
      if (five != prevFiveHour) {
        updateBar(0, five);
        prevFiveHour = five;
      }
      if (seven != prevSevenDay) {
        updateBar(1, seven);
        prevSevenDay = seven;
      }
    }
  }
}


  void updateBar(int row, int percent) {
    if (percent > 99) percent = 99;
    int totalBars = 10;
    int filled = (percent * totalBars) / 100;

    lcd.setCursor(3, row);
    for (int i = 0; i < totalBars; i++) {
      if (i < filled) lcd.write(byte(0));
      else            lcd.print(" ");
    }

    lcd.setCursor(14, row);
    if (percent >= 10) { lcd.print(percent); }
    else               { lcd.print(" "); lcd.print(percent); }
  }