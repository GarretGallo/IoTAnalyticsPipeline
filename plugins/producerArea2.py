import random
from datetime import datetime, timedelta

from confluent_kafka import Producer
from faker import Faker
import boto3
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("ProducerArea2")

fake = Faker()
logger = logging.getLogger(__name__)

def get_secret(secret_name, region_name="us-east-1"):
    session = boto3.session.Session(region_name=region_name)
    client = session.client('secretsmanager', )
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        logger.error(f"Secret retrieval error: {e}")
        raise

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Delivery failed: {err}")
    else:
        logger.info(
            f"Message delivered to {msg.topic()} [partition {msg.partition()}] at offset {msg.offset()}")

class ProducerArea2:
    def __init__(self):
        secrets = get_secret('gasMonitorSecrets')
        kafka_config = {
            "bootstrap.servers": secrets['KAFKA_BOOTSTRAP_SERVER'],
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": secrets['KAFKA_SASL_USERNAME'],
            "sasl.password": secrets['KAFKA_SASL_PASSWORD'],
            "group.id": "airflow_log_indexer",
        }

        def create_kafka_producer(config):
            return Producer(config)

        self.producer = create_kafka_producer(kafka_config)
        self.topic = 'area2'

        self.locationMonitor4 = "7608 Ferrara Ave, Orlando, FL 32819"
        self.locationMonitor5 = "7469 Kingspointe Pkwy, Orlando, FL 32819"
        self.locationMonitor6 = "5256 International Dr, Orlando, FL 32819"

        self.current_ts = datetime(2020, 1, 1)
        self.battery = self.battery_simulation()
        self.calibration = self.calibration_simulation()

    def next_timestamp(self):
        ts = self.current_ts
        self.current_ts += timedelta(seconds=30)
        return ts.isoformat()

    def battery_simulation(self):
        value = 100
        while True:
            yield round(value, 2)
            step = random.uniform(0.00025, 0.000347)
            value -= step
            if value <= 0:
                value = 100

    def calibration_simulation(self):
        value = 30
        while True:
            yield round(value, 0)
            step = random.uniform(0.00025, 0.000347)
            value -= step
            if value <= 0:
                value = 30

    def generateMonitorData(self, monitorNum: int, location: str):
        h2sReading = random.randint(0, 25)
        temperatureMH = random.randint(25, 105)
        humidity = random.randint(20, 60)
        pressure = random.randint(0, 10)
        batteryHealth = next(self.battery)
        daysUntilCalibration = next(self.calibration)
        technicalFailure = random.choice(["NO", "YES - MINOR", "YES - MAJOR"])
        timestamp = self.next_timestamp()

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

    def produce_data(self, monitorNum: int, location: str):
        for _ in range(1000):
            reading = self.generateMonitorData(monitorNum, location)
            payload = json.dumps(reading).encode('utf-8')
            try:
                self.producer.produce(
                    self.topic,
                    payload,
                    callback=delivery_report
                )
                self.producer.poll(0)
                self.producer.flush()
            except Exception as e:
                logger.error(f"Failed to produce log: {e}")

    def produceDataMonitor4(self, **context):
        self.produce_data(4, self.locationMonitor4)

    def produceDataMonitor5(self, **context):
        self.produce_data(5, self.locationMonitor5)

    def produceDataMonitor6(self, **context):
        self.produce_data(6, self.locationMonitor6)

def produceDataMonitor4(**context):
    ProducerArea2().produceDataMonitor4(**context)


def produceDataMonitor5(**context):
    ProducerArea2().produceDataMonitor5(**context)


def produceDataMonitor6(**context):
    ProducerArea2().produceDataMonitor6(**context)

#Test
"""if __name__ == "__main__":
    fake = ProducerArea2()
    for i in range(10):
        print(fake.generateMonitorData(4, "Area 2"))"""