import socket
import time

host = "0.0.0.0"
port = 1377
clients = []
clients_data = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)
counter=0
quitting = False
print("Server Started")
while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
            clients_data.append(data)
            for client in clients:
                s.sendto(("new len:" + str(len(clients)) + str(clients_data)).encode(), client)
            print(time.ctime(time.time()) + str(addr) + " : : " + "Joined and his message is :" + str(data))

        else:
            if data.decode()=='finish':
                counter+=1
                if counter==len(clients):
                    tmp=clients[:]
                    clients.clear()
                    data='restart'.encode()
                    print(data,tmp)
                    for client in tmp:
                        s.sendto(data, client)
            else:
                for client in clients:
                    s.sendto(data, client)
    except:
        pass
s.close()
