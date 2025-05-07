import os
import sm_tc
import yaml
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time

CONFIG_PATH = os.path.join(os.path.expanduser('~'),'config.yaml')
with open(CONFIG_PATH) as file:
    CONFIG:dict[int,list[int]] = yaml.safe_load(file)

smtcs:dict[int,sm_tc.SMtc] = {}
for addr in CONFIG['smtc_addresses']:
    smtcs[addr] = sm_tc.SMtc(addr)

INFLUX_CLIENT = InfluxDBClient(CONFIG['influx_url'],
                               token=CONFIG['influx_token'],
                               org=CONFIG['influx_org'])
WRITE_API = INFLUX_CLIENT.write_api(write_options=SYNCHRONOUS)
BUCKET = 'test_data'

def push_influx(label:str, metric:str, value:float, time:datetime):
    point = Point('test_measurement').tag('DeviceName',label).field(metric,value).time(time.astimezone())
    WRITE_API.write(BUCKET, record=point)

def main():
    while True:
        t = datetime.now()
        for addr in CONFIG['smtc_addresses']:
            for i in range(8):
                temp = smtcs[addr].get_temp(i+1)
                push_influx('-'.join([str(addr),str(i+1)]),'Temperature',temp,t)

if __name__ == '__main__':
    if len(CONFIG['smtc_addresses']) > 0:
        main()