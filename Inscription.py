import socket
import json

serverAddress = ('localhost',3000)
with open('Inscription.json') as file:
        strJson = file.read()

def client():
    s = socket.socket()
    s.connect((serverAddress))
    s.send(strJson.encode())
    response = json.loads(s.recv(2048).decode()) #on reçoit un fichier json en réponse, pour le transformer en dico python on utilise loads
    if  response == {"response": "ok"}:
        print(response)
        s.close()
        return True
    else:
        s.close()
        print(response)
        return False

def server():
    s2 = socket.socket()
    serverAddress2 = ('0.0.0.0',json.loads(strJson)['port'])
    s2.bind(serverAddress2)
    s2.listen()
    msg_perso = {"response": "pong"}
    
    while True:
        prof, address = s2.accept()
        msg_prof= json.loads(prof.recv(2048).decode())
        print(msg_prof)
        if msg_prof == {"request": "ping"}:
            # pas besoin car deja co s2.connect(serverAddress)
            prof.send(json.dumps(msg_perso).encode()) #convertit le dico python en fichier json
            print(msg_perso)

        prof.close()

if client() == True:
    server()