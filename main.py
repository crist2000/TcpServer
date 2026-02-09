import socket
import threading
import ctypes  # An included library with Python install.

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


#bind_ip = "127.0.0.1"
bind_ip = "10.5.11.28"
bind_port = 500

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
# we tell the server to start listening with
# a maximum backlog of connections set to 5
server.listen(5)

print(f"[+] Listening on port {bind_ip} : {bind_port}")

def responce_check(resp):
    if "Error" in resp:
        return True
    else:
        return False

#client handling thread
def handle_client(client_socket):
    #printing what the client sends
    request = client_socket.recv(1024)
    str = f"{request}"
    print(f"[+] Recieved: {request}")

    if responce_check(str):
        Mbox('Your title', "Alert!!!", 1)

    #sending back the packet
    client_socket.send("Ping recevied".encode())
    client_socket.close()

while True:
    # When a client connects we receive the client socket into the client variable, and the remote connection details into the addr variable
    client, addr = server.accept()
    print(f"[+] Accepted connection from: {addr[0]}:{addr[1]}")
    #spin up our client thread to handle the incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()