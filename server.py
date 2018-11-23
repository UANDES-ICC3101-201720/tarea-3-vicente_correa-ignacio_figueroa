import socket  # Import socket module

HOST = socket.gethostbyname(socket.gethostname())
PORT = 50007
BUFFER_SIZE = 1024
FILE = "example.txt"
online = []
class client:
    def __init__(self):
        self.ip = ""
        self.conn = ""
        self.port = ""
        self.files = []

clientePrueba = client()
clientePrueba.ip = "192.168.0.31"
clientePrueba.port = "45678"
clientePrueba.files=["Foto1.jpg", "Foto2.jpg", "Prueba.txt"]
sockets = []
with socket.socket() as s:
    online.append(clientePrueba)

    s.bind((HOST, PORT))
    s.listen(5)
    cliente = client()

    cliente.conn, addr = s.accept()

    received = cliente.conn.recv(BUFFER_SIZE).decode()
    received = received.split(" ")
    cliente.port = received[0][1:-1]
    print (received)
    cliente.ip = received[1][1:-1]
    online.append(cliente)
    message = "<{}> HOW ARE U, GIVE ME YOUR FILENAMES <{}>".format(PORT, cliente.ip)
    sent = cliente.conn.send(message.encode())
    file = cliente.conn.recv(BUFFER_SIZE)
    while file:
        cliente.files.append(file.decode())
        sent = cliente.conn.send("OK".encode())
        file = cliente.conn.recv(BUFFER_SIZE)
        print(file.decode())
        if file.decode() == "FINISH":
            break
    while True:
        received = cliente.conn.recv(BUFFER_SIZE).decode()
        if "IM SEARCHING" in received:
            cliente.conn.send("OK ILL SEARCH".encode())
            file = received.split(" ")[2]
            encountered = False
            for c in online:
                if file in c.files:
                    cliente.conn.send("{} HAS IT".format(c.ip).encode())
                    encountered = True
                    response = cliente.conn.recv(BUFFER_SIZE).decode()
                    if response == "OK, TELL ME MORE":
                        continue
                    else:
                        print("error")
                        break

            if not encountered:
                cliente.conn.send("NO ONE HAS IT :(".encode())
            else:
                cliente.conn.send("THATS ALL FOLK".encode())
        if "I DONT NEED U ANYMORE" in received:
            online.remove(cliente)
            cliente.conn.send("OK, BAI {}".format(cliente.ip).encode())
            s.close()


