import gpiozero
import time

# GPIO3番に接続しているボタンを監視
button = gpiozero.Button(26 )

while True:
    if button.is_pressed:
        print("pressed")
    else:
        print("no pressed")
    time.sleep(0.2)

