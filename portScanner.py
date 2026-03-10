import socket
import pyfiglet

ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

target = input("Where to go boss: ")
target_ip = socket.gethostbyname(target)

#co 65535 cong ma nhieu qua nen chi lay 1025 cong thoi hoac chay tu 70 len 90

for i in range (70, 90):
    port = i
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(0.25)

    result = s.connect_ex((target_ip, port))

    if(result == 0):
        print(f"Connect success!! Port {port} is open")
        try:
            s.send(b"WhoAreYou\r\n")
            
            message = s.recv(1024)
            #they send boring stuff so no need            
            #print(f"{message} said: {message.decode().strip()}") 
        except:
            print("This guy is tuff, no respone!")
        
    #else: print(f"ERROR! Portal {port} closed")
    s.close()