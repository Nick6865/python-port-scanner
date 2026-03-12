import socket
import pyfiglet

#new:
import concurrent.futures
#can i use from multiprocessing import Pool? (saw it on stack overflow)

ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

target = input("Where to go boss: ")
target_ip = socket.gethostbyname(target)

#co 65535 cong ma nhieu qua nen chi lay 1025 cong thoi hoac chay tu 70 len 90

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
        except:
            pass
    
    s.close()
    
ports_to_scan = range(1,1025) #can i really scan all 65535 ports
### in theory i can do it, but the big leauges like google, facebook and their ddos system will identify me as their opp

print(f"Scanning {target_ip}...\n")

#executor will hire 100 workers to work and use map to guide them
with concurrent.futures.ThreadPoolExecutor(max_workers = 100) as executor:
    executor.map(scan_port, ports_to_scan)
    
print("Scan completed!!")