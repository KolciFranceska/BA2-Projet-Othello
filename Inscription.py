import socket
import json
import threading
from unicodedata import name

serverAddress = ('localhost',3000)
with open('Joueur1.json') as file:
    Inscri1 = file.read()
with open('Joueur2.json') as file:
    Inscri2 = file.read()


def client(Joueur):
    s = socket.socket()
    s.connect((serverAddress))
    s.send(Joueur.encode())
    response = json.loads(s.recv(2048).decode()) #on reçoit un fichier json en réponse, pour le transformer en dico python on utilise loads
    if  response == {"response": "ok"}:
        print(json.loads(Joueur)['name'], response)
        s.close()
        return True
    else:
        s.close()
        print(json.loads(Joueur)['name'], response)
        return False

def server(Joueur):
    s2 = socket.socket()
    serverAddress2 = ('0.0.0.0',json.loads(Joueur)['port'])
    s2.bind(serverAddress2)
    s2.listen()
    rep_ping = {"response": "pong"}

    the_move_played = int
    list_of_errors = []
    state = {
    "players": [],
    "current": 0,
    "board":[]}

    msg_coup = {
   "request": "play",
   "lives": 3,
   "errors": list_of_errors,
   "state": state}

    rep_coup = {
   "response": "move",
   "move": the_move_played,
   "message": "Fun message"}

    black = []
    white = []
    while True:
        prof, address = s2.accept()
        msg_prof= json.loads(prof.recv(2048).decode())
        print(msg_prof)
        if msg_prof == {"request": "ping"}:
            prof.send(json.dumps(rep_ping).encode()) #convertit le dico python en fichier json
            print(json.loads(Joueur)['name'], rep_ping)
        if msg_prof['request'] == 'play':
            state = [black,white]
            rep_coup['move']= int(input("Sélectionner une case pour jouer: "))
            prof.send(json.dumps(rep_coup).encode())
            print(rep_coup)
        prof.close()

def jouer():
    if client(Inscri1) == True:
        server(Inscri1)

thread = threading.Thread(target = jouer, daemon = True)
thread.start()
while True :
    if client(Inscri2)==True:
        server(Inscri2)