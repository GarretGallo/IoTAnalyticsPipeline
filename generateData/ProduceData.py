import json
import boto3
import random
import uuid
from faker import Faker
from time import sleep
from datetime import datetime, timedelta

fake = Faker()

LOCATIONS = {
    "Area 1": ["6378 Edge O Grove Cir, Orlando, FL 32819",
               "6125 St Ives Blvd, Orlando, FL 32819",
               "6301 Parson Brown Dr, Orlando, FL 32819"],
    "Area 2":["7608 Ferrara Ave, Orlando, FL 32819",
              "7469 Kingspointe Pkwy, Orlando, FL 32819",
              "5256 International Dr, Orlando, FL 32819"],
    "Area 3": ["1891 4th St, Orlando, FL 32824",
               "304 Palmetto St, Orlando, FL 32824",
               "300 Tradeport Dr, Orlando, FL 32824"],
    "Area 4": ["1250 N Alafaya Trail, Orlando, FL 32828",
               "1700 Woodbury Road, Orlando, FL 32828",
               "12900 Science Dr, Orlando, FL 32826"],
    "Area 5": ["7501 W Colonial Dr, Orlando, FL 32818",
               "6651 Old Winter Garden Rd, Orlando, FL 32835",
               "6234 W Colonial Dr, Orlando, FL 32808"],
    "Area 6": ["290 Holden Ave, Orlando, FL 32839",
               "5529 Hansel Ave, Orlando, FL 32809",
               "531 Kenmore Cir, Orlando, FL 32839"],
    "Area 7": ["520 Lake Como Cir, Orlando, FL 32803",
               "2320 E Robinson St, Orlando, FL 32803",
               "1501 Noble Pl, Orlando, FL 32801"]
}

current_ts = datetime(2020, 1, 1)
def next_timestamp():
    global current_ts
    ts = current_ts
    current_ts += timedelta(seconds=30)
    return ts.isoformat()

def battery_simulation():
    value = 100
    while True:
        yield round(value, 2)
        step = random.uniform(0.00025, 0.000347)
        value -= step
        if value <= 0:
            value = 100
battery = battery_simulation()

def calibration_simulation():
    value = 30
    while True:
        yield round(value, 0)
        step = random.uniform(0.00025, 0.000347)
        value -= step
        if value <= 0:
            value = 30
calibration = calibration_simulation()

def data_generator(monitorNum, location):
    monitorNum = monitorNum
    location = location
    h2sReading = random.randint(0, 15)
    temperatureMH = random.randint(25, 105)
    humidity = random.randint(20, 40)
    pressure = random.randint(0, 10)
    batteryHealth = next(battery)
    daysUntilCalibration = next(calibration)
    technicalFailure = random.choice(["NO", "YES - MINOR", "YES - MAJOR"])
    timestamp = next_timestamp()

    reading = {
        'monitorNum': monitorNum,
        'location': location,
        'h2sReading': h2sReading,
        'temperatureMH': temperatureMH,
        'humidity': humidity,
        'pressure': pressure,
        'batteryHealth': batteryHealth,
        'daysUntilCalibration': daysUntilCalibration,
        'technicalFailure': technicalFailure,
        'timestamp': timestamp
    }
    return reading

filename = 'Monitor21Data.json'
with open(filename, 'w') as f:
    for _ in range(1051200):
        reading = data_generator(monitorNum=21, location=LOCATIONS["Area 7"][2])
        f.write(json.dumps(reading) + "\n")

print(f"JSON data successfully written to {filename}")