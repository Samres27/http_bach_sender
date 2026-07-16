import socket
import ssl
import gzip
import zlib
import brotli
import zstandard as zstd
import lzma
import bz2
import re

import socket
import ssl
import re

def enviarPeticiones(lista):
    patron = r'^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$'
    listaSessiones = {}
    respuestas=[]
    for x in lista:
        https = x.https
        dominio_limpio = x.dominio.replace("http://", "").replace("https://", "")
        splitDominio = dominio_limpio.split(":")
        
        if len(splitDominio) > 1: 
            puerto = int(splitDominio[1].split("/")[0])
        else:
            puerto = 443 if https else 80
        host_str = splitDominio[0].split("/")[0]
        coincidencia = re.search(patron, host_str)
        if coincidencia:
            host = coincidencia.group()
        else:
            host = host_str 

        # --- LÓGICA DE CONEXIÓN ---
        if not (x.dominio in listaSessiones):
            sock = socket.create_connection((host, puerto))
            if https:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host) 
            listaSessiones[x.dominio] = sock
            conexion = sock
        else:
            conexion = listaSessiones[x.dominio]
        a,b=enviarPeticion(conexion, x.peticion)
        respuestas.append({"nro":x.nroPeticion,"resp":a,"status":b})
    for conexion_abierta in listaSessiones.values():
        conexion_abierta.close()

    return respuestas
def enviarPeticion(sock,request):
    sock.sendall(request.encode())
    response = b""
    header= b""
    body= b""
    while  True:
        try:
            chunk = sock.recv(1024)
            
            ssplit=chunk.split(b"\r\n\r\n")
            header=ssplit[0]+b'\r\n\r\n'
            body=ssplit[1]

            # Iteramos hasta conseguir el header: Content-Length
            for x in header.split(b'\r\n'):
                if b"Content-Length" in x:
                    ConLen=int(x.split(b':')[1])
                    if ConLen>len(body):
                        resBody=sock.recv(ConLen-len(body))
                        body=body+resBody
                        break
            response1 += chunk
            if not chunk:
                break
            break  # Esto es solo para demostración, realmente deberíamos leer toda la respuesta.
        except socket.timeout:
            break

    for x in header.split(b"\r\n"):
        
        if b'Content-Encoding' in x:
            text_encode=x.split(b":")[1].strip()
            print("header enter" + text_encode.decode(errors="replace"))
            match text_encode:
                case b"gzip":
                    body=gzip.decompress(body)
                case b"deflate":
                    body=zlib.decompress(body)
                case b"br":
                    print("-"*20+"llamada br")
                    body=brotli.decompress(body)  
                case b"zstd":
                    dctx = zstd.ZstdDecompressor()
                    body = dctx.decompress(body)
                case b"bz2":
                    body = bz2.decompress(body)
                case b"lzma":
                    body=lzma.decompress(body) 
                case b"xz":
                    body=lzma.decompress(body) 
                    
    return header+b'\r\n\r\n'+body, re.search(rb'HTTP/\d\.\d (\d{3})', header)

