import socket
import sys
from os import scandir, getcwd

def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]
host = '192.168.0.31'
print(host)
port = 50007
BUFFER_SIZE = 1024
file = "recibido2.jpg"
address = (host, port)

archivos = []
for arc in ls():
    if ".txt" in arc or ".jpg" in arc:
        archivos.append(arc)
print(archivos)
with socket.socket() as s:
    print("socket creado")
    s.connect(address)
    print("conectado")
    mensaje = "<{}> <{}> HELLO <{}>" # my port, my ip, server ip
    s.send(mensaje.format(port, socket.gethostbyname(socket.gethostname()), host).encode())
    respuesta = s.recv(BUFFER_SIZE).decode()
    print(respuesta)
    if str(respuesta).__contains__("HOW ARE U"):
        print("Bien, el formato del mensaje es valido")
    else:
        print("Error, el formato del mensaje es invalido")
    for file in archivos:
        print(file)
        s.send(file.encode())
        ok = s.recv(BUFFER_SIZE).decode()
        if ok == "OK":
            continue
        else:
            print("Error en confirmacion de recivo de archivo")
            break
    s.send("FINISH".encode())

    while True:
        print("Que deseas hacer?\n"
              "\t (1) Buscar archivo\n"
              "\t (2) Enviar archivo\n"
              "\t (3) Salir")
        opcion = input("Ingrese su opcion: ")
        if opcion == "1":
            ips_con_archivo = []
            file_name = input("Ingrese el nombre del archivo que busca: ")
            s.send("IM SEARCHING {}".format(file_name).encode())

            respuesta1 = s.recv(BUFFER_SIZE).decode()
            print(respuesta1)
            respuesta = s.recv(BUFFER_SIZE).decode()
            encontrado = True
            while respuesta:
                print(respuesta)
                if str(respuesta).__contains__("NO ONE HAS IT :("):
                    encontrado = False
                    break
                elif str(respuesta).__contains__("THATS ALL FOLK"):
                    break
                else:
                    ips_con_archivo.append(respuesta.split(" ")[0])
                    s.send("OK, TELL ME MORE".encode())
                    respuesta = s.recv(BUFFER_SIZE).decode()
            print()
            if encontrado:
                print("Direcciones IP que tienen el archivo buscado:")
                for i in range(len(ips_con_archivo)):
                    print("\t({}) {}".format(i + 1, ips_con_archivo[i]))
                ip_elegido = input("Elige una direccion IP de donde quieres descargar el archivo: ")
                print("elegiste la ip {}".format(ips_con_archivo[int(ip_elegido) - 1]))
                print()


        elif opcion == "2":
            pass
        elif opcion == "3":
            sys.exit(0)


