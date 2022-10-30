import socket
import time
import os
import threading
import configuraciones
import RoundRobinn

def proxy():
  sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sockets.bind((configuraciones.HOST, configuraciones.PUERTO))
  sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  print(f'Escuchando peticiones en el puerto {configuraciones.PUERTO}')
  sockets.listen(5)

  while True:
    try:
      conectado, direccion = sockets.accept()
      Uconectado = f'Usuario conectado {direccion} con : {conectado}'
      print(Uconectado)
      loggin(Uconectado)
      thread = threading.Thread(target = multiUsuario, args = (conectado, direccion))
      thread.start()
    except:
      print("Coneccion terminada")
      break
  sockets.close()

def multiUsuario(conectado, direccion):
  contenidoHttp = ''
  while True:
    try:
      contenidoHttp1 = conectado.recv(configuraciones.TAMAÑO)
      print(f'Solicitud del usuario : {contenidoHttp1}')
      if contenidoHttp1 != b'':
        contenidoHttp = contenidoHttp1.decode()
        print(contenidoHttp)
        solicitud = contenidoHttp.split('\n')[0]
        loggin(solicitud)
        print(f'solicitud : {solicitud}')
        coneccionInstancia(conectado, contenidoHttp1, solicitud)
      else:
        break
    except:
      print("en el except")
      break
  #conectado.close()

def coneccionInstancia(conectado, contenidoHttp, solicitud):
  socketN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  solicitud1 = solicitud.split(' ')[1]
  solicitud1 = solicitud1.replace("/", '')
  solicitud1 = solicitud1.replace(":", '')
  solicitud1 = solicitud1 + '.txt'
  
  nombreArchivos = os.listdir('cache/')
  contadorCache = 0

  if solicitud1 in nombreArchivos:
    tiempoFinal = time.time()
    with open(f'cache/{solicitud1}', 'rb') as archivo:
      tiempoArchivo = archivo.readline().decode()
    tiempoTotal = tiempoFinal - float(tiempoArchivo)
    if tiempoTotal >= 60:
      print("elminando el archivo")
      os.remove(f'cache/{solicitud1}')
      contadorCache = 0
    else:
      contadorCache = 1
  else:
    contadorCache = 0

  if contadorCache == 1:
    print("entro en el cache")
    with open(f'cache/{solicitud1}', 'rb') as archivo:
      datosCache = archivo.readlines()[1:]
    datosCache = b''.join(datosCache)
    envioDataCliente(conectado, datosCache)
    socketN.close()
  else:
    RoundRobin = RoundRobinn.roundRobin()
    print(RoundRobin)
    socketN.connect((RoundRobin, configuraciones.PUERTOI))
    print(contenidoHttp)
    socketN.sendall(contenidoHttp)
    print("consultando a la intancia")
    
    while True:
      rInstancia = []
      datos = socketN.recv(configuraciones.TAMAÑO)
      rInstancia.append(datos)
      while len(datos) != 0:
        datos = socketN.recv(configuraciones.TAMAÑO)
        rInstancia.append(datos)
      rInstancia = b''.join(rInstancia)
      
      if len(rInstancia) != 0:
        tiempoInicial = time.time()
        cache(solicitud, rInstancia, tiempoInicial)
        envioDataCliente(conectado, rInstancia)
        break
      else:
        print("no se recibieron datos de la instancia")
        break
    socketN.close()

def envioDataCliente(conectado, rInstancia):
  conectado.sendall(rInstancia)
  print("datos enviados al cliente")

def loggin(texto):
  f = open ('loggin.txt','a')
  texto = texto + '\n'
  f.write(texto)
  f.close()

def cache(solicitud, response, tiempo):
  solicitud = (solicitud).split(' ')[1]
  solicitud = solicitud.replace("/", '')
  solicitud = solicitud.replace(":", '')
  f = open(f'cache/{solicitud}.txt', 'ab')
  f.write(str(tiempo).encode() + '\n'.encode())
  f.write(response)
  f.close()

if __name__ == "__main__":
  proxy()