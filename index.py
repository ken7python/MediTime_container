import config
import requests
import schedule
import time
#import csv
#import pandas as pd
import json

import RPi.GPIO as GPIO
import gpiozero

import sys
import datetime
from playsound import playsound
from i2clcda import *

address = config.get_address()
port_dict = config.get_port_config()
LINE_taken = config.get_LINE_taken()

start_button_port = config.startButtonPort()
end_button_port = config.endButtonPort()

GPIO.setmode(GPIO.BCM)
for day,pin in port_dict.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(start_button_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(end_button_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
"""
GPIO.setup(port_dict["Sunday_port"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(port_dict["Monday_port"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(port_dict["Tuesday_port"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(port_dict["Wednesday_port"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(port_dict["Thursday_port"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(port_dict["Friday_port"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(port_dict["Saturday_port"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
"""
def send_line_notify(notification_message):
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {LINE_taken}'}
    data = {'message':notification_message}
    requests.post(line_notify_api, headers = headers, data = data)
def send_message(label):
    send_line_notify(f"{label}のお薬を飲んでください")

#send_line_notify("test")
def request_hukuyouTime():
    response = requests.get(address + "/hukuyouTime")
    print("request_hukuyouTime")
    return response.json()

def request_hukuyouHistory():
    response = requests.get(address + "/hukuyou")
    print("request_hukuyouTime")
    return response.json()["hukuyouHistory"]
"""
global hukuyouTime
hukuyouTime = request_hukuyouTime()["hukuyouTime"]
global valid
valid = request_hukuyouTime()["valid"]
"""

tasks = []
def cancel_tasks():
    for task in tasks:
        schedule.cancel_job(task)
    print("cancel_tasks")

class task():
    def __init__(self,label,day_of_week,day_number):
        self.label = label
        self.time = time
        self.day_of_week = day_of_week
        self.day_number = day_number
    def hukuyou_check(self):
        history = [item for item in hukuyouHistory if (item["date"] == time.strftime("%Y/%m/%d") and item["label"] == self.label and item["type"] == "label" ) ]
        #print(history)
        if (len(history) > 0 ):
            print(self.label + "は服用済みです")
            return True
        else: 
            return False
        '''
        for item in hukuyouHistory:
            print(item)
            date = item["date"]
            day_of_week = item["day_of_week"]
            label = item["label"]
            type = item["type"]
            if (date == time.strftime("%Y/%m/%d") and label == self.label):
                ....
        '''
        
        """
        df = pd.read_csv(config.get_history_file_path())
        df = df[df["date"] == time.strftime("%Y/%m/%d")]
        df_label = df[df["label"] == self.label]
        
        #print(df_label )
        #print(self.day_of_week)
        if (df_label["label"].count() != 0 ):
            df_week = df_label[df_label["day_of_week"] == self.day_of_week]
            #print(df_week.count() )
            if df_week["day_of_week"].count() != 0:
                print(f"{self.day_of_week}の{self.label}は取り消しました")
                return True
            else:
                return False
        else:
            return False
        
        """
        
    def same_week_day(self):
        week = datetime.date.today().weekday()
        if week == self.day_number:
            return True
        else:
            return False
def set_tasks():
    cancel_tasks()
    """
    for v in valid:
        print(v)
    """
    for time in hukuyouTime:
        #print(time)
        label = time["label"]
        valid_now = [v for v in valid if v["label"]== label][0]["hukuyouTime"] == 1
        #print(valid_now)
        #print(time["Sunday"])
        """
        tasks.append(schedule.every().sunday.at(time["Sunday"]).do(send_message,label))
        tasks.append(schedule.every().monday.at(time["Monday"]).do(send_message,label))
        tasks.append(schedule.every().tuesday.at(time["Tuesday"]).do(send_message,label))
        tasks.append(schedule.every().wednesday.at(time["Wednesday"]).do(send_message,label))
        tasks.append(schedule.every().thursday.at(time["Thursday"]).do(send_message,label))
        tasks.append(schedule.every().friday.at(time["Friday"]).do(send_message,label))
        tasks.append(schedule.every().saturday.at(time["Saturday"]).do(send_message,label))
        """
        if valid_now:
            print(label + "の通知はオンになっています")
            Sunday_task = task(label,"Sunday",6)
            Monday_task = task(label,"Monday",0)
            Tuesday_task = task(label,"Tuesday",1)
            Wednesday_task = task(label,"Wednesday",2)
            Thurs_task = task(label,"Thursday",3)
            Friday_task = task(label,"Friday",4)
            Saturday_task = task(label,"Saturday",5)
            
            if Sunday_task.same_week_day():
                if (not Sunday_task.hukuyou_check() ) and time["Sunday"] != "":
                    print("日曜日をタスクに追加します")
                    tasks.append(schedule.every().sunday.at(time["Sunday"]).do(send_message,label))
            if Monday_task.same_week_day():
                if (not Monday_task.hukuyou_check() ) and time["Monday"] != "":
                    print("月曜日をタスクに追加します")
                    tasks.append(schedule.every().monday.at(time["Monday"]).do(send_message,label))
            if Tuesday_task.same_week_day():
                if (not Tuesday_task.hukuyou_check() ) and time["Tuesday"] != "":
                    print("火曜日をタスクに追加します")
                    tasks.append(schedule.every().tuesday.at(time["Tuesday"]).do(send_message,label))
            if Wednesday_task.same_week_day():
                if (not Wednesday_task.hukuyou_check() ) and time["Wednesday"] != "":
                    print("水曜日をタスクに追加します")
                    tasks.append(schedule.every().wednesday.at(time["Wednesday"]).do(send_message,label))
            if Thurs_task.same_week_day():
                if (not Thurs_task.hukuyou_check() ) and time["Thursday"] != "":
                    print("木曜日をタスクに追加します")
                    tasks.append(schedule.every().thursday.at(time["Thursday"]).do(send_message,label))
            if Friday_task.same_week_day():
                if (not Friday_task.hukuyou_check() ) and time["Friday"] != "":
                    print("金曜日をタスクに追加します")
                    tasks.append(schedule.every().friday.at(time["Friday"]).do(send_message,label))
            if Saturday_task.same_week_day():
                if (not Saturday_task.hukuyou_check() ) and time["Saturday"] != "":
                    print("土曜日をタスクに追加します")
                    tasks.append(schedule.every().saturday.at(time["Saturday"]).do(send_message,label))
        else:
            print(label + "の通知はオフになっています")
    print("set_tasks")
    #print(tasks)
    #print(tasks)
# ボタン押し / 離し 動作確認用コード
"""
def check_history(value):# データーベースから取り込むべき
    with open(config.get_history_file_path(),"r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            if row[0] == value[0] and row[1] == value[1] and row[2] == value[2]:
                return True
    return False
"""
class ButtonAndHistory():
    def __init__(self,weekday,day_number):
        self.weekday = weekday
        self.day_number = day_number
        self.LastStatus = False
        self.SwitchStatus = False
        self.port = port_dict[self.weekday + "_port"]
        if (self.port == 0):
            self.button = None
        else:
            self.button = gpiozero.Button(self.port)
    def append_history(self):
        data = {
            "date": time.strftime("%Y/%m/%d"),
            "label": config.get_label(),
            "day_of_week": self.weekday,
        }
        print(data)
        """
        with open(config.get_history_file_path(),"a") as f:
            writer = csv.writer(f)
            value = [time.strftime("%Y/%m/%d"),config.get_label(),self.weekday]
            if not check_history(value):
                writer.writerow(value)
        """
        json_data = json.dumps(data)
        response = requests.post(
            address + "/hukuyou",
            data = json_data,
            headers={"Content-Type": "application/json"}
        )
    def get_same_week_day(self):
        week = datetime.date.today().weekday()
        if week == self.day_number:
            return True
        else:
            return False
    def check_button(self):
        if (self.button == None):
            self.SwitchStatus = False
        else:
            self.SwitchStatus = self.button.is_pressed#GPIO.input(self.port)
        #print(self.SwitchStatus)
        if self.LastStatus != self.SwitchStatus:
            if self.SwitchStatus == 1:
                print(f"{self.weekday}のボタンが押された")
                if self.get_same_week_day():
                    self.append_history()
                    update_tasks()
                    return "Success"
                else:
                    return "Failed"
        self.LastStatus = self.SwitchStatus
def update_tasks():
    print("update_task in " + str(datetime.datetime.now() ))
    global hukuyouTime
    global valid
    global hukuyouHistory
    hukuyouTime = request_hukuyouTime()["hukuyouTime"]
    valid = request_hukuyouTime()["valid"]
    hukuyouHistory = request_hukuyouHistory()
    set_tasks()
update_tasks()
schedule.every(30).seconds.do(update_tasks)
week_switchs = [ButtonAndHistory("Sunday",6),ButtonAndHistory("Monday",0),ButtonAndHistory("Tuesday",1),ButtonAndHistory("Wednesday",2),ButtonAndHistory("Thursday",3),ButtonAndHistory("Friday",4),ButtonAndHistory("Saturday",5)]

start_button = gpiozero.Button(start_button_port)
end_button = gpiozero.Button(end_button_port)
lcd_init()

working = False
days3 = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
def main():
    global working
    while True:
        if start_button.is_pressed and not working:
            v = request_hukuyouTime()["valid"]
            for i in v:
                if i["label"] == config.get_label():
                    hukuyou_valid = i["hukuyouTime"] == 1
            if hukuyou_valid:
                print("Start")
                working = True
                lcd_string("Working",LCD_LINE_1)
                send_line_notify("メディタイム開始しました")
                playsound("start.mp3")
            else:
                print("通知を有効化する必要があります")
                playsound("error2.mp3")
        elif end_button.is_pressed and working:
            print("End")
            working = False
            lcd_string("",LCD_LINE_1)
            send_line_notify("メディタイム終了しました")
            playsound("end.mp3")
        if working:
            schedule.run_pending()
            results = []
            for switch in week_switchs:
                results.append(switch.check_button())
                if "Success" in results:
                    print("Success")
                elif "Failed" in results:
                    print("Failed")
                    playsound("error.mp3")
        dt_now = datetime.datetime.now()
        week_str = days3[dt_now.weekday()]
        dt_str = dt_now.strftime(f'%m/%d {week_str} %H:%M')
        lcd_string(dt_str,LCD_LINE_2)
        time.sleep(0.2)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # ピンの設定を初期化
        GPIO.cleanup()
        sys.exit()
    finally:
        lcd_byte(0x01, LCD_CMD)
#次回

