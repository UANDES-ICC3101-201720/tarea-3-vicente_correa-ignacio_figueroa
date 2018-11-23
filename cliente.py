import socket
import sys
from os import scandir, getcwd
import _thread
BUFFER_SIZE = 1024

def ls(ruta = getcwd()):
    return [arch.name for arch in scandir(ruta) if arch.is_file()]
def escuchar_siempre():
    print("Inicio de la funcion de thread")
    host = ''
    port = 50008
    address = (host, port)
    with socket.socket() as sn:
        sn.bind(address)
        sn.listen(1)
        conn, addr = sn.accept()
        print("Thread conectado")
        mensaje = conn.recv(BUFFER_SIZE).decode()
        if str(mensaje).__contains__("A LITTLE BIRD"):
            f_name = str(mensaje).split("<")
            f_name = f_name[1].strip(">")
            conn.send("YEP, I GOT I BABE".encode())
            with open(f_name, 'rb') as f:
                data = f.read(BUFFER_SIZE)
                while data:
                    conn.sendall(data)
                    data = f.read(BUFFER_SIZE)

archivos = []
for arc in ls():
    if ".txt" in arc or ".jpg" in arc or ".png" in arc or ".pdf" in arc:
        archivos.append(arc)

try:
    _thread.start_new_thread(escuchar_siempre, ())
except:
    print("Error al crear el thread")
    sys.exit(0)

host = '192.168.0.31'
port = 50007
address = (host, port)

with socket.socket() as s:
    print("Socket creado")
    s.connect(address)
    print("Ya estas conectado al server")
    mensaje = "<{}> <{}> HELLO <{}>" # my port, my ip, server ip
    s.send(mensaje.format(port, socket.gethostbyname(socket.gethostname()), host).encode())
    respuesta = s.recv(BUFFER_SIZE).decode()
    print("Server:", respuesta)
    for file in archivos:
        s.send(file.encode())
        ok = s.recv(BUFFER_SIZE).decode()
        if ok == "OK":
            continue
        else:
            #print("Error en confirmacion de recivo de archivo")
            break
    s.send("FINISH".encode())

    while True:
        print()
        print("Que deseas hacer?\n"
              "\t (1) Buscar archivo\n"
              "\t (2) Salir")
        opcion = input("Ingrese su opcion: ")
        if opcion == "1":
            ips_con_archivo = []
            file_name = input("Ingrese el nombre del archivo que busca: ")
            s.send("IM SEARCHING {}".format(file_name).encode())

            respuesta1 = s.recv(BUFFER_SIZE).decode()
            print("Server:", respuesta1)
            respuesta = s.recv(BUFFER_SIZE).decode()
            encontrado = True
            while respuesta:
                print("Server:", respuesta)
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
                #print("elegiste la ip {}".format(ips_con_archivo[int(ip_elegido) - 1]))

                host2 = ips_con_archivo[int(ip_elegido) - 1]
                port2 = 50008
                address2 = (host2, port2)
                with socket.socket() as s2:
                    s2.connect(address2)
                    print("Conectado al host {}".format(host2))
                    mensaje = "A LITTLE BIRD SAID ME THAT YOU HAVE <{}>".format(file_name)
                    s2.send(mensaje.encode())
                    confirmacion = s2.recv(BUFFER_SIZE).decode()
                    print("Server:", confirmacion)
                    archivo_recibido = file_name
                    with open(archivo_recibido, "wb") as f:
                        buf = s2.recv(BUFFER_SIZE)
                        while buf:
                            f.write(buf)
                            buf = s2.recv(BUFFER_SIZE)
                    s2.send("DOWNLOAD COMPLETE".encode())
                    print("Archivo descargado correctamente")
                    s2.close()
        elif opcion == "2":
            s.send("I DONT NEED U ANYMORE".encode())
            okb = s.recv(BUFFER_SIZE).decode()
            if str(okb).__contains__("BAI"):
                s.close()
            sys.exit(0)


