import socket
from threading import Thread


SERVER_HOST="0.0.0.0"
SERVER_PORT=1234

separator_token="<SEP>"

client_sockets=set()
s=socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((SERVER_HOST,SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")





def listen_for_client(cs):
    while True:
        try:
            msg= cs.recv(1024).decode()
            #message = s.recv(1024).decode()
            print("\n" + msg)
        except Exception as e:
            print(f"[!] error:{e}")
            client_sockets.remove(cs)
        else:
            msg =msg.replace(separator_token,": ")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    client_socket, client_address= s.accept()

    #date_now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #to_send=f"{date_now}: {name}{separator_token}{to_send}"
    #s.send(to_send.encode())
    print(f"[+] {client_address} connected")
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client,args=(client_socket,))
    t.daemon=True
    t.start()


for cs in client_sockets:
    cs.close()
s.close()