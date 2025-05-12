import os
import lib16univin
import yaml
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

SOCKET_PATH = '/tmp/smadc.sock'

CONFIG_PATH = os.path.join(os.path.expanduser('~'),'config.yaml')
with open(CONFIG_PATH) as file:
    CONFIG:dict[int,list[int]] = yaml.safe_load(file)

smadcs:dict[int,lib16univin.SM16univin] = {}

for addr in CONFIG['smadc_addresses']:
    smadcs[addr] = lib16univin.SM16univin(addr)

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
        for addr in CONFIG['smtc_addresses']:
            for i in range(16):
                voltage = smadcs[addr].get_u_in(i+1)
                push_influx('-'.join([str(addr),str(i+1)]),'adc_measurement',voltage,t)

if __name__ == '__main__':
    if len(CONFIG['smadc_addresses']) > 0:
        main()