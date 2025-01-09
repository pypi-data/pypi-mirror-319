# https://buymeacoffee.com/apintio

import struct
import random
import socket
from iid import HelloWorld

import threading
import websockets
import asyncio


####### IID ###
def say_hello():
    HelloWorld.say_hello()

def bytes_to_int(bytes:bytes):
    value= struct.unpack('<i', bytes)[0]
    return value

def bytes_to_index_integer(bytes:bytes):
    index, value = struct.unpack('<ii', bytes)
    return index, value

def  bytes_to_index_integer_date(bytes:bytes):
    index, value, date = struct.unpack('<iiQ', bytes)
    return index, value, date

def integer_to_bytes(value:int):
    return struct.pack('<i', value)

def index_integer_to_bytes(index:int, value:int):
    return struct.pack('<ii', index, value)

def index_integer_date_to_bytes(index:int, value:int, date:int):
    return struct.pack('<iiQ', index, value, date)

## UDP IID
### SEND UDP IID
class SendUdpIID:
    def __init__(self, ivp4, port):
        self.ivp4 = ivp4
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def push_bytes(self, bytes:bytes):
        self.sock.sendto(bytes, (self.ivp4, self.port))
        
    def push_text(self, text:str):
        self.push_bytes(text.encode('utf-8'))
        
    def push_integer(self, value:int):
        self.push_bytes(integer_to_bytes(value))
        
    def push_index_integer(self, index:int, value:int):
        self.push_bytes(index_integer_to_bytes(index, value))
        
    def push_index_integer_date(self, index:int, value:int, date:int):
        self.push_bytes(index_integer_date_to_bytes(index, value, date))
        
    def push_random_integer(self, index:int, from_value:int, to_value:int):
        value = random.randint(from_value, to_value)
        self.push_index_integer(index, value)
        
    def push_random_integer_100(self, index:int):
        self.push_random_integer(index, 0, 100)
        
    def push_random_integer_int_max(self, index:int):
        self.push_random_integer(index, -2147483647, 2147483647)


## UDP IID
### RECEIVE UDP IID
class ListenUdpIID:
    def __init__(self, ivp4, port):
        self.ivp4 = ivp4
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ivp4, self.port))
        self.on_receive_integer = None
        self.on_receive_index_integer = None
        self.on_receive_index_integer_date = None
        # Start thread
        self.thread = threading.Thread(target=self.listen)
        self.thread.daemon = True
        self.thread.start()
        
    def listen(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                if data is None:
                    continue
                size = len(data)
                if size == 4:
                    value = bytes_to_int(data)
                    if self.on_receive_integer:
                        self.on_receive_integer(value)
                elif size == 8:
                    index, value = bytes_to_index_integer(data)
                    if self.on_receive_index_integer:
                        self.on_receive_index_integer(index, value)
                elif size == 12:
                    index, value, date = bytes_to_index_integer_date(data)
                    if self.on_receive_index_integer_date:
                        self.on_receive_index_integer_date(index, value, date)
                elif size == 16:
                    index, value, date = bytes_to_index_integer_date(data)
                    if self.on_receive_index_integer_date:
                        self.on_receive_index_integer_date(index, value, date)
            except Exception as e:
                print("Error:", e)
                self.sock.close()
                break
        print("Wait for restart...")
       
       
       
## Websocket IID
### SEND WEBSOCKET IID         
# NOT TESTED YET
class NoAuthWebsocketIID:
    
    def __init__(self, ivp4, port):
        self.ivp4 = ivp4
        self.port = port
        self.uri = f"ws://{self.ivp4}:{self.port}"
        self.on_receive_integer = None
        self.on_receive_index_integer = None
        self.on_receive_index_integer_date = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.connect())
        
    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            await self.listen(websocket)
            
    async def listen(self, websocket):
        async for message in websocket:
            data = message.encode('latin1')
            size = len(data)
            if size == 4:
                value = bytes_to_int(data)
                if self.on_receive_integer:
                    self.on_receive_integer(value)
            elif size == 8:
                index, value = bytes_to_index_integer(data)
                if self.on_receive_index_integer:
                    self.on_receive_index_integer(index, value)
            elif size == 12:
                index, value, date = bytes_to_index_integer_date(data)
                if self.on_receive_index_integer_date:
                    self.on_receive_index_integer_date(index, value, date)
            elif size == 16:
                index, value, date = bytes_to_index_integer_date(data)
                if self.on_receive_index_integer_date:
                    self.on_receive_index_integer_date(index, value, date)
            
 # ## Websocket IID
### RECEIVE WEBSOCKET ECHO IID
# NOT TESTED YET
class NoAuthWebSocketEchoIID:
    def __init__(self, ivp4:str, port:int, bool_print_debug:bool):
        self.ivp4 = ivp4
        self.port = port
        self.bool_print_debug = bool_print_debug
        self.uri = f"ws://{self.ivp4}:{str(self.port)}"
        if self.bool_print_debug:
            print (f"Websocket IID Echo Server: {self.uri}")
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start_server())

    async def start_server(self):
        async with websockets.serve(self.echo, self.ivp4, self.port):
            await asyncio.Future()  # run forever

    async def echo(self, websocket, path):
        if self.bool_print_debug:
            print (f"Websocket IID Echo Server: {self.uri} connected")
        async for message in websocket:
            size = len(message)
            if size == 4 or size == 8 or size == 12 or size == 16:
                if self.bool_print_debug:
                    print (f"Received: {message}")
                await websocket.send(message)
                