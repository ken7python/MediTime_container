import os
from dotenv import load_dotenv

load_dotenv()
def get_address():
    print("address config set")
    #return "http://192.168.1.25:3000"
    #return "http://192.168.1.16:3000"
    return "http://192.168.1.200:3000"
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
def get_LINE_taken():
    return os.environ["LINE_TAKEN"]
def get_history_file_path():
    return "hukuyouHistory.csv"
def get_label():
    return '朝'
def startButtonPort():
    return 26
def endButtonPort():
    return 20
