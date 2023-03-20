import socket

HOST = "192.168.10.14" # IP address of your Raspberry PI
PORT = 65432         # Port to listen on (non-privileged ports are > 1023)
import picar_4wd
import binascii
from gpiozero import CPUTemperature

def move(s):
    power = 20
    speed = 0
    if("87" in s):
        picar_4wd.forward(power)
        speed = power
    elif("83" in s):
        picar_4wd.backward(power)
        speed = -1 * power
    elif("65" in s):
        picar_4wd.turn_left(power)
        speed = 0
    elif("68" in s):
        picar_4wd.turn_right(power)
        speed = 0
    else:
        picar_4wd.stop()
        speed = 0
    return speed



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                list_data=[]
                st = data.decode('ascii')
                speed = str(move(st))
                list_data.append(speed)
                temp = str(CPUTemperature().temperature)
                list_data.append(temp)
                dist = str(picar_4wd.get_distance_at(0))
                list_data.append(dist)
                to_ret = ",".join(list_data)
                data = bytes(to_ret,'UTF-8')
                client.sendall(data)
    except: 
        print("Closing socket")
        client.close()
        s.close()    