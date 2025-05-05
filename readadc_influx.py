import piplates.ADCplate as ADC
import os
import yaml
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.expanduser('~'),'config.yaml')
with open(CONFIG_PATH) as file:
    CONFIG:dict = yaml.safe_load(file)

ADDRESSES = CONFIG['adc_addresses']
INFLUX_CLIENT = InfluxDBClient(CONFIG['influx_url'],
                               token=CONFIG['influx_token'],
                               org=CONFIG['influx_org'])
WRITE_API = INFLUX_CLIENT.write_api(write_options=SYNCHRONOUS)
BUCKET = 'test_data'

CHANNELS = ['S0','S1','S2','S3','S4','S5','S6','S7','D0','D1','D2','D3','I0','I1','I2','I3']

def push_influx(label:str, metric:str, value:float, time:datetime):
    point = Point('test_measurement').tag('DeviceName',label).field(metric,value).time(time.astimezone())
    WRITE_API.write(BUCKET, record=point)

if __name__ == '__main__':
    while True:
        t = datetime.now()
        for address in ADDRESSES:
            values = ADC.getADCall(address)
            for value, channel in zip(values, CHANNELS):
                push_influx('-'.join([str(address),channel]), 'adc_measurement', value, t)