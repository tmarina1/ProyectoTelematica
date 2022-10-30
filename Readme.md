# PIBL

## Tabla de contenidos

[INTRODUCCIÓN](#INTRODUCCIÓN)  
[DESARROLLO](#DESARROLLO)  
[Lenguajes y programas](#Lenguajes-y-programas)  
[Uso y creación](#Uso-y-creación)  
[Archivo configuraciones.py](#Archivo-configuraciones)  
[Archivo RoundRobinn.py](#Archivo-RoundRobinn)  
[Archivo proxy.py](#Archivo-proxy)  
[funciones](#funciones)

[CONCLUSIONES](#CONCLUSIONES)  
[DESARROLLADO POR](#DESARROLLADO-POR)  
[REFERENCIAS](#REFERENCIAS)

# INTRODUCCIÓN

Este proyecto está basado en una arquitectura cliente/servidor utilizando la API sockets, haciendo uso de la técnica del multi hilo, usando un algoritmo balanceador de carga llamado round-robbin, un registro de cache y creando un proxy inverso.

Basado en lo anteriormente mencionado, el algoritmo balanceador de
carga 'round-robin', se encarga de determinar cuál servidor dentro de un conjunto de servidores usar para recibir las peticiones entrantes realizadas por parte de los clientes, luego por cada petición realizada, el servidor debe devolver una respuesta al proxy que luego la enviara al cliente.

El proxy inverso implementado se encarga de interceptar las peticiones del cliente y la envía al servidor anteriormente asignado por el round-robbin que cuenta con la capacidad de procesar esa información para luego ser recibida por el proxy y enviársela al cliente.

# DESARROLLO

## Lenguajes y programas

El lenguaje de programación que usamos fue Python debido a la capacidad y el manejo que tiene de los hilos, hace que sea un poco más sencillo de entender la técnica y la aplicabilidad, Ademas de contar con un garbage colector que facilita el uso e interación con el lenguaje de programación.

El programa que usamos es Visual Studio Code porque tiene muy buenas extensiones las cuales hacen que codificar sea más cómodo y tiene muy buen manejo de las ejecuciones de múltiples lenguajes.

## Uso y creación

En este creamos 3 archivos.py.

- Para la configuración que trae la conexión con el servidor, un archivo llamado configuraciones.py.
- Para el proxy inverso encargado de la comunicación cliente/servidor, un archivo llamado proxy.py.
- Para el round-robin encargado de balancear la carga, un archivo llamado RoundRobinn.py.

### Archivo configuraciones

En este archivo asignamos como variables las necesarias para configurar la conexión con el servidor, pasándole los puertos del usuario y las instancias, el formato correspondiente, un tamaño para el buffer y el host del cliente.

```python

PUERTO = 8080
PUERTOI = 80
HOST = '127.0.0.1'
FORMATO = 'utf-8'
TAMAÑO = 4050

```

### Archivo RoundRobinn

En este archivo nos encargamos de la creación de todo el algoritmo de round-robin para balancear la carga entre los servidores como sigue:

```python
def roundRobin():
  listaInstancias = ['18.234.185.41', '44.204.176.223', '43.204.172.225']

  with open("robin.txt", 'r') as f:
    i = f.readline()
    f.close()

  if i == '0':
    i = int(i) + 1
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[0]
  elif i == '1':
    i = int(i) + 1
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[1]
  elif i == '2':
    i = 0
    A = open ('robin.txt','w')
    A.write(str(i))
    A.close()
    return listaInstancias[2]

if __name__ == "__main__":
  roundRobin()

```

En resumen lo que hace es guardar los servidores en un arreglo, luego abrir y crear un archivo txt llamado robin.txt, dentro de este tiene un numero 0, luego se comprueba que numero tiene ese archivo en caso de ser 0, lo modifica a 1, y trae la posición 0 del arreglo anteriormente creado es decir el primer servidor, luego como el archivo tiene un 1, al leerlo, modifica el valor a 2, y trae la posición 1 del arreglo anteriormente creado es decir el segundo servidor, y por ultimo lee en el robin.txt un 2, lo que hace es modificarlo nuevamente a 0, y leer la tercera posición del arreglo, es decir, el tercere servidor, y así sucesivamente ya que nuevamente está en cero.

En otras palabras, cada que se hace una nueva petición asigna de 1 en 1 cada servidor.

### Archivo proxy

En este archivo nos encargamos de la comunicación cliente/servidor, haciendo uso también de los anteriores 2 archivos.py creados.

En este caso debemos hacer las siguientes importaciones:

```python
import socket
import time
import os
import threading
import configuraciones
import RoundRobinn
```

- La librería de sockets, para la creación de los sockets que sirven para realizar las conexiones del proxy con el cliente y con los servidores.
- La librería de tiempo para calcular cuánto tiempo se debe almacenar la cache.
- La librería del sistema operativo, para el manejo de los ficheros y rutas.
- La librería de threading para permitir el uso de varios clientes en la parte del servidor (multi hilo).
- Hacemos llamado de los dos archivos.py anteriormente creados que son configuraciones.py y RoundRobinn.py.

Luego se hace la creación de las funciones

#### Funciones:

- Creamos la función proxy() encargada de crear el socket para los clientes, además de escuchar las peticiones de los clientes en el host y puerto que se le indique en el archivo configuraciones.py y de crear el hilo con el que se permitirá la conexión y manejo de múltiples usuarios.

```python
def proxy():
  sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sockets.bind((configuraciones.HOST, configuraciones.PUERTO))
  sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #configurar el tipo de socket
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
```

- Esta función permite conectar múltiples usuarios al servidor al mismo tiempo, como también es el encargado de recibir la petición del usuario y de enviar dicha petición al siguiente método que es el encargado de la conexión con la instancia.

```python
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
```

- La siguiente función se encarga de conectarse con la instancia dependiendo del servidor que le arroje el balanceador de carga, enviarle a la instancia la petición del usuario y recibir la respuesta que esta lede para así posteriormente enviarle dicha respuesta al usuario. Además crear y almacenar datos en la cache, almacenando el tiempo en ese instante y la respuesta recibió de la instancia, para que así si el usuario realiza la misma petición el proxy no le deba preguntar a la instancia si no que pueda consultar los archivos generados por la cache y tomar la información que solicita el usuario de estos, por ultimo verifica si la cache ya lleva demasiado tiempo de existencia mediante un delta de tiempo, de ser el caso elimina el archivo de la cache y recure a preguntarle a la instancia por la petición del usuario.

```python
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
```

- El siguiente método es el encargado de enviarle los datos obtenidos ya sea por la consulta a la instancia o por la consulta en la cache al usuario.

```python
def envioDataCliente(conectado, rInstancia):
  conectado.sendall(rInstancia)
  print("datos enviados al cliente")
```

- El siguiente método es el encargado de crear un log de lo que ocurre entre el servidor y los clientes que se conectaron, es decir un registro de los usuarios conectados y de las peticiones que estos realizan, guardando así un archivo llamado loggin.txt con la información anteriormente mencionada.

```python
def loggin(texto):
  f = open ('loggin.txt','a')
  texto = texto + '\n'
  f.write(texto)
  f.close()
```

- Esta función es la encargada de crear el archivo de cache, para administrarlo luego en la función de coneccionInstancia(), lo que hace es almacenar un archivo con la información que el proxy recibe de la instancia y con el tiempo de cuándo se creó para luego poder hacer la eliminación de la cache si se da el caso.

```python
def cache(solicitud, response, tiempo):
  solicitud = (solicitud).split(' ')[1]
  solicitud = solicitud.replace("/", '')
  solicitud = solicitud.replace(":", '')
  f = open(f'cache/{solicitud}.txt', 'ab')
  f.write(str(tiempo).encode() + '\n'.encode())
  f.write(response)
  f.close()
```

- Por último para su ejecución final se hace llamado al proxy en un main, para que funcione de la manera que se requiere.

```python
if __name__ == "__main__":
  proxy()
```

# CONCLUSIONES

- Logramos entender el funcionamiento y cómo hacer uso de los sockets, como escuchar, conectar, recibir y demás funcionalidades de los sockets.
- Aprendimos cómo crear un proxy inverso, su aplicabilidad y cómo se usarlo de intermediario en la conexión entre cliente/servidor.
- Logramos entender el funcionamiento del algoritmo de balanceo de carga round robin y la importancia de tener un balanceador de carga a la hora de realizar consultas en servidores.
- Entendimos el funcionamiento e importancia de una cache, ya que permite la consulta rapida de información que fue previamente consultada.
- Logramos apreciar la importancia de eliminar la cache después de un tiempo determinado, debido a que la información contenida en las páginas puede cambiar en poco tiempo por lo cual de no eliminar la cache cada cierto tiempo estaríamos mostrándole al usuario datos erróneos.
- Entendimos la importancia de un log, para así tener todas las peticiones y respuestas entre los clientes y el servidor, para manejar de manera más sencilla algunos posibles errores y estar al tanto de lo que ocurre entre las comunicaciones entre las entidades.
- Hubo muy buen trabajo en equipo y buena coordinación, por lo que la práctica se pudo hacer y entender de manera clara.

# DESARROLLADO POR

[Tomás Marín Aristizabal](https://github.com/tmarina1),
[Juan Andrés Vera Álvarez](https://github.com/Vera3588),
[Samuel Salazar Salazar](https://github.com/ssalazar11)

# REFERENCIAS

[TCP Sockets](https://realpython.com/python-sockets/#tcp-sockets)
[Solicitudes HTTP](https://unipython.com/solicitudes-http-en-python-con-requests/)
[Sockets server](https://docs.python.org/es/3/library/socketserver.html)
[Timer functions](https://www.delftstack.com/es/howto/python/python-timer-functions/)
[OS module](https://www.tutorialsteacher.com/python/os-module#:~:text=The%20OS%20module%20in%20Python,with%20the%20underlying%20operating%20system)
