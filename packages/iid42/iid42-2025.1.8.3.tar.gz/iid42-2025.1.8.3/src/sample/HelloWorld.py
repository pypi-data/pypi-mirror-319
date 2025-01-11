
# pip install iid42 --break-package-system

"""
python -m build
pip install .\dist\iid42-2025.1.8.2-py3-none-any.whl --force-reinstall

pip install --upgrade twine
python -m twine upload dist/*
pip install iid42 --force-reinstall

"""
import socket
import iid42

def hello_world():
    print("Hello, World!")
    
def push_my_first_iid():
    print("Push My First IID")
    target = iid42.SendUdpIID("127.0.0.1",3615,True)
    target.push_integer(42)
    target.push_index_integer(0,2501)
    target.push_index_integer_date_ntp_now(1,1001)
    target.push_index_integer_date_ntp_in_milliseconds(2,2001,1000)
    
    
def console_loop_to_push_iid_local():
    console_loop_to_push_iid_with_params("127.0.0.1",3615)
    
def console_loop_to_push_iid_ddns(target_ddns:str):
    port = 3615
    ipv4 = socket.gethostbyname(target_ddns)
    console_loop_to_push_iid_with_params(ipv4,port)
    
 
def console_loop_to_push_iid_apintio():
    """
    This allows to twitch play in python when EloiTeaching is streaming with UDP activated.
    
    """
    # NOTE: UDP on APINT.IO is only available on port 3615 when a Twitch Play is occuring
    # See Py Pi apintio for ddns name and tools
    console_loop_to_push_iid_ddns("apint-gaming.ddns.net")
    # See no-ip.com for creating a ddns name for your own IP address
 

def console_loop_to_push_iid_with_params(ivp4:str, port:int):
    print("Console Loop To Push IID")
    target= iid42.SendUdpIID(ivp4, port,True)
    print ("Enter 'exit' to stop")
    print ("i: 42 (For integer)")
    print ("ii: 0, 42 (For index integer)")
    print ("iid: 5, 1000, 50 (Push inex 5 integer 1000 to press with a delay request of 50ms)")
    print ("iid: 5, 2000, 500 (Push inex 5 integer 2000 to release with a delay request of 500ms)")
    
    while True:
        text= input("Enter IID Text: ")
        target.push_integer_as_shorcut(text)    
    
if __name__ == "__main__":
    push_my_first_iid()
    console_loop_to_push_iid_apintio()
    