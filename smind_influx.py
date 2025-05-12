import os
import megaind
import yaml
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time

CONFIG_PATH = os.path.join(os.path.expanduser('~'),'config.yaml')
with open(CONFIG_PATH) as file:
    CONFIG:dict[int,list[int]] = yaml.safe_load(file)

measurements:dict[int,list[float]] = {}

INFLUX_CLIENT = InfluxDBClient(CONFIG['influx_url'],
                               token=CONFIG['influx_token'],
                               org=CONFIG['influx_org'])
WRITE_API = INFLUX_CLIENT.write_api(write_options=SYNCHRONOUS)
BUCKET = 'test_data'

def push_influx(label:str, metric:str, value:float, time:datetime):
    point = Point('test_measurement').tag('DeviceName',label).field(metric,value)#.time(time.astimezone())
    WRITE_API.write(BUCKET, record=point)

def main():
    while True:
        t = datetime.now()
        for addr in CONFIG['smind_addresses']:
            for i in range(4):
                measurement = megaind.get4_20In(addr,i+1)
                push_influx('-'.join([str(addr),str(i+1)]),'Ind_Current',measurement,t)

if __name__ == '__main__':
    if len(CONFIG['smind_addresses']) > 0:
        main()