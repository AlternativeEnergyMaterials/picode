import piplates.ADCplate as ADC
import socket
import os
import yaml

SOCKET_PATH = '/tmp/readadc.sock'

CONFIG_PATH = os.path.join(os.path.expanduser('~'),'config.yaml')
with open(CONFIG_PATH) as file:
    config:dict = yaml.safe_load(file)

def handle_command(command):
    if "get_measurement" in command:
        address = command.split()[1]
        channel = command.split()[2]
        return str(ADC.getADC(int(address),channel))+'\n'
    else:
        return "Unknown command\n"

def run_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    #Create a Unix socket
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(SOCKET_PATH)
    server_socket.listen(1)

    print("Server listening...")

    while True:
        conn, _ = server_socket.accept()
        try:
            command = conn.recv(1024).decode('utf-8')
            if command:
                response = handle_command(command)
                conn.sendall(response.encode('utf-8'))
        finally:
            conn.close()

if __name__ == "__main__":
    # for address in config['adc_addresses']:
        # ADC.setMODE(address, 'HIGH')
    #     ADC.setMODE(address, 'ADV')
    #     for channel in range(8):
    #         print('S'+str(channel))
    #         ADC.configINPUT(address, 'S' + str(channel), 8, True)
    #     for channel in range(4):
    #         print('I'+str(channel))
    #         ADC.configINPUT(address, 'I' + str(channel), 8, True)
    run_server()