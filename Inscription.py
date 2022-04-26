import socket
import json

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
        print(response)
        s.close()
        return True
    else:
        s.close()
        print(response)
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
            print(rep_ping)
        if msg_prof['request'] == 'play':
            state = [black,white]
            the_move_played= input(int("Sélectionner une case pour jouer: "))
            prof.send(json.dumps(rep_coup).encode())
            print(rep_coup)
        prof.close()

def jouer(joueur):
    if client(joueur) == True:
        server(joueur)
        
jouer(Inscri1)
jouer(Inscri2)