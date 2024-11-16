import os
from dotenv import load_dotenv

load_dotenv()
def get_address():
    print("address config set")
    #return "http://192.168.1.25:3000"
    #return "http://192.168.1.16:3000"
    return "http://192.168.1.200:3000"
"""
def get_port_config():
    sunday_port = 17
    monday_port = 27
    tuesday_port = 22
    wednesday_port = 23
    thursday_port = 24
    friday_port = 25
    saturday_port = 5
    print("port config set")
    return {"Sunday_port": sunday_port,"Monday_port": monday_port, "Tuesday_port": tuesday_port, "Wednesday_port": wednesday_port, "Thursday_port": thursday_port, "Friday_port": friday_port, "Saturday_port": saturday_port,}
"""
def get_LINE_taken():
    return os.environ["LINE_TAKEN"]
def get_history_file_path():
    return "hukuyouHistory.csv"
"""
def get_label():
    return '夜'
"""
def startButtonPort():
    return 26
def endButtonPort():
    return 20
def request_headers():
    return {"Content-Type": "application/json; charset=UTF-8"}

class Port:
    def __init__(self,label,sunday_port,monday_port,tuesday_port,wednesday_port,thursday_port,friday_port,saturday_port):
        self.label = label
        self.sunday_port = sunday_port
        self.monday_port = monday_port
        self.tuesday_port = tuesday_port
        self.wednesday_port = wednesday_port
        self.thursday_port = thursday_port
        self.friday_port = friday_port
        self.saturday_port = saturday_port
    def get_port_config(self):
        print("port config set")
        return {"Sunday_port": self.sunday_port,"Monday_port": self.monday_port, "Tuesday_port": self.tuesday_port, "Wednesday_port": self.wednesday_port, "Thursday_port": self.thursday_port, "Friday_port": self.friday_port, "Saturday_port": self.saturday_port,}
    
ports = [Port("朝",11,4,14,15,18,10,9),Port("昼",17,27,22,23,24,25,5),Port("夜",16,8,7,12,6,13,19)]
def get_ports():
    return ports