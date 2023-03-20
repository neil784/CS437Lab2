from bluedot.btcomm import BluetoothServer
from signal import pause

def recieved_handler(data):
    print(data)
    s.send(data)

s = BluetoothServer(recieved_handler)

pause()