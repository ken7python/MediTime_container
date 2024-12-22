# 必要なモジュールのインポート
import RPi.GPIO as GPIO
import time
import sys

# ポート番号の定義
Sw_GPIO = 26

# GPIOの設定
GPIO.setmode(GPIO.BCM)
# GPIO26を入力モードに設定してプルダウン抵抗を有効にする
GPIO.setup(Sw_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # GPIO26の入力を読み取る
        switchStatus = GPIO.input(Sw_GPIO)
        print(switchStatus)
        # スイッチが押下された時に”pressed”と出力
        if switchStatus == GPIO.HIGH:
            print("pressed")
        else:
            print("not pressed")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()