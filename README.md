# usage-cube

透過 Serial 將 Claude API 用量數據傳送到 Arduino，即時顯示在 LCD 或 OLED 上。

## 硬體接線

兩種版本都使用 I2C，接法相同：

| Arduino | 顯示器 |
|---------|--------|
| A4 (SDA) | SDA |
| A5 (SCL) | SCL |
| 5V | VCC |
| GND | GND |

- LCD 版本：I2C 位址 `0x27`
- OLED 版本：I2C 位址 `0x3C`

## Serial 通訊格式

鮑率：**9600**，每筆資料以換行符結尾。

### LCD (`lcd/main.ino`)

```
<5h_percent>,<7d_percent>\n
```

範例：
```
42,87
```

### OLED (`oled/oled_128x64.ino`)

```
<5h_percent>,<7d_percent>,<5h_secs>,<7d_secs>\n
```

| 欄位 | 說明 |
|------|------|
| `5h_percent` | 5 小時用量百分比（0–100）|
| `7d_percent` | 7 天用量百分比（0–100）|
| `5h_secs` | 距離 5H 重置的剩餘秒數 |
| `7d_secs` | 距離 7D 重置的剩餘秒數 |

後兩個欄位可省略，省略時顯示 `now`。

範例：
```
42,87,3600,86400
```

## 用 Python 發送更新

```python
import serial
import time

ser = serial.Serial('COM3', 9600)  # Windows：COM3、Linux/Mac：/dev/ttyUSB0
time.sleep(2)  # 等待 Arduino 重置

five_hour_pct = 42
seven_day_pct = 87
five_hour_secs = 3600
seven_day_secs = 86400

line = f"{five_hour_pct},{seven_day_pct},{five_hour_secs},{seven_day_secs}\n"
ser.write(line.encode())
ser.close()
```

安裝依賴：
```bash
pip install pyserial
```

## 持續更新

若要定期推送，可用迴圈或 cron job 呼叫上方腳本。Arduino 收到相同數值時不會重繪畫面，僅在數值變動時更新。
