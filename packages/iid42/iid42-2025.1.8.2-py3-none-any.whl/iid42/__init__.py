# https://buymeacoffee.com/apintio

import struct
import random
import socket
import threading
import websockets
import asyncio
import time
import ntplib

####### IID ###

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
    return struct.pack('<iiQ', index, value, int(date))

def text_shortcut_to_bytes(text:str):
    try:
        if text.startswith("i:"):
            integer = int(text.split(":")[1])
            return integer_to_bytes(integer)
        elif text.startswith("ii:"):
            index, integer = text.split(":")[1].split(",")
            return index_integer_to_bytes(int(index), int(integer))
        elif text.startswith("iid:"):
            index, integer, delay = text.split(":")[1].split(",")
            return index_integer_date_to_bytes(int(index), int(integer), int(delay))
        else:
            while "  " in text:
                text = text.replace("  ", " ")
            tokens : list = text.replace(",", " ").split(" ")
            size = len(tokens)
            if size == 1:
                integer = int(text)
                return integer_to_bytes(integer)
            elif size == 2:
                index = int(tokens[0])
                integer = int(tokens[1])
                return index_integer_to_bytes(index, integer)
            elif size == 3:
                index = int(tokens[0])
                integer = int(tokens[1])
                delay = int(tokens[2])
                return index_integer_date_to_bytes(index, integer, delay)
            else:
                integer = int(text)
                return integer_to_bytes(integer)
    except Exception as e:
        print("Error", e)    
    return None
        
   
class NtpOffsetFetcher:
    
    def fetch_ntp_offset_in_milliseconds( ntp_server):
        try:
            c = ntplib.NTPClient()
            response = c.request(ntp_server)
            return response.offset*1000
        except Exception as e:
            print(f"Error NTP Fetch: {ntp_server}", e)
            return 0
    
    
## UDP IID
### SEND UDP IID
class SendUdpIID:
    
    def __init__(self, ivp4, port, use_ntp:bool):
        self.ivp4 = ivp4
        self.port = port
        self.ntp_offset_local_to_server_in_milliseconds=0
        
        if use_ntp:
            self.fetch_ntp_offset()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        
    def push_integer_as_shorcut(self, text:str):
        bytes = text_shortcut_to_bytes(text)
        if bytes:
            self.sock.sendto(bytes, (self.ivp4, self.port))
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
        
    def fetch_ntp_offset(self, ntp_server="be.pool.ntp.org"):        
        self.set_ntp_offset_tick(NtpOffsetFetcher.fetch_ntp_offset_in_milliseconds(ntp_server))
        print (f"NTP Offset: {self.ntp_offset_local_to_server_in_milliseconds}")

    def set_ntp_offset_tick(self, ntp_offset_local_to_server:int):
        self.ntp_offset_local_to_server_in_milliseconds=ntp_offset_local_to_server
    
    def push_index_integer_date_local_now(self, index:int, value:int):
        date = int(time.time())
        self.push_index_integer_date(index, value, date)
        
    def push_index_integer_date_ntp_now(self, index:int, value:int):
        date = int(time.time()) + self.ntp_offset_local_to_server_in_milliseconds
        self.push_index_integer_date(index, value, date)
   
    def push_index_integer_date_ntp_in_milliseconds(self, index:int, value:int, milliseconds:int):
        date = int(time.time()) + self.ntp_offset_local_to_server_in_milliseconds + milliseconds/1000
        self.push_index_integer_date(index, value, date)
        
   
    def push_index_integer_date_ntp_in_seconds(self, index:int, value:int, seconds:int):
        self.push_index_integer_date_ntp_in_milliseconds(index, value, seconds*1000)



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
                