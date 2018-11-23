import socket
import sys
from os import scandir, getcwd

def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]
host = '192.168.0.18'
print(host)
port = 50007
BUFFER_SIZE = 1024
file = "recibido2.jpg"

archivos = []
for arc in ls():
    if ".txt" in arc or ".jpg" in arc:
        archivos.append(arc)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("socket creado")
    s.connect((host, port))
    print("conectado")
    mensaje = "<{}> <{}> HELLO <{}>"
    s.send(mensaje.format(port, host, socket.gethostname()))
    s.sendto(mensaje.format(port, host, socket.gethostname()), (host, port))

    print("Que deseas hacer?\n"
          "\t (1) Buscar archivo\n"
          "\t (2) Enviar archivo\n"
          "\t (3) Salir\n")
    opcion = input("Ingrese su opcion: ")
    if opcion == "1":
        pass
    elif opcion == "2":
        pass
    elif opcion == "3":
        sys.exit(0)

    with open(file, "wb") as f:
        BUFFER = s.recv(BUFFER_SIZE)
        while BUFFER:
            f.write(BUFFER)
            BUFFER = s.recv(BUFFER_SIZE)