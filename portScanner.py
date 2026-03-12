import socket
import pyfiglet
import concurrent.futures
import argparse #now i can use it in terminal no need to run file any more
#new:
import time

            #CONTROL PANEL
parser = argparse.ArgumentParser(description="Python Port Scanner V3 by Nick")
#.add_argument to set Flags
parser.add_argument("-t", "--target", help="Target's IP", required=True)
#-t abbreviation for t, --target is full name, required=True forces user to type!

parser.add_argument("-p", "--ports", default="1-1024")
#default if user forgot to type anything

parser.add_argument("-w", "--workers", type=int, default=100)
#turn strings into int i guess?

args = parser.parse_args()

            #PRINT BANNER
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

            #INPUT HANDLING
try:
    target_ip = socket.gethostbyname(args.target)
except socket.gaierror:
    print(f"The domain {args.target} is incorrect or does not exist. Please check again!")
    exit()

#handling the -p
try:
    start_port, end_port = map(int, args.ports.split('-'))
    ports_to_scan = range(start_port, end_port +1)
except ValueError:
    print("Syntax Error! Please type again")
    print(r'"Start"-"End" example: -p 1-1000')
    exit()

            #ENGINE
#use func to guide workers
def scan_port(port):
    global target_ip # use target ip globally
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.25)
    
    result = s.connect_ex((target_ip, port))
     
    if result == 0: #connect success
        print(f"Connect success!! Port {port} is open")
        try:
            s.send(b"WhoAreYou\r\n") # \r moves the cursor back to the start
            message = s.recv(1024) #1024 characters
            print("Sending a message to server...\n")
            print(f"Port {port}'s respond: {message.decode('utf-8').strip()}\n")
            #converts byte string (message) to a Unicode string using UTF8 encoding and removes leading whitespace
        except:
            pass
    
    s.close()
    
#can i really scan all 65535 ports
### in theory i can do it, but the big leauges like google, facebook and their ddos system will identify me as their opp

print("-" * 50 + "\n")
print(f"Scanning {target_ip}...\n")
print(f"Scanning from port {start_port} to port {end_port}")
print(f"{args.workers} are working")
print("-" * 50 + "\n")

#add a timer
start_time = time.time()

#executor will hire 100 workers to work and use map to guide them
with concurrent.futures.ThreadPoolExecutor(max_workers = args.workers) as executor:
    executor.map(scan_port, ports_to_scan)
    
end_time   = time.time()
    
print(f"Scan completed in {end_time - start_time:.2f} seconds!!")