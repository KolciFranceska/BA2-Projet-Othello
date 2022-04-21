import socket
import json
from game import Othello

serverAddress = ('localhost',3000)
with open('Inscription.json') as file:
        strJson = file.read()
lives = 3
list_of_errors = []
state_of_the_game = ""
the_move_played = ""


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
    rep_ping = {"response": "pong"}
    choix_coup = int(input("Jouer un coup (taper 1) ou abandonner (taper 2) : "))
    msg_coup = {
   "request": "play",
   "lives": 3,
   "errors": list_of_errors,
   "state": state_of_the_game
}
    rep_coup = {
   "response": "move",
   "move": the_move_played,
   "message": "Fun message"
}
    while True:
        prof, address = s2.accept()
        msg_prof= json.loads(prof.recv(2048).decode())
        print(msg_prof)
        if msg_prof == {"request": "ping"}:
            prof.send(json.dumps(rep_ping).encode()) #convertit le dico python en fichier json
            print(rep_ping)
        if msg_prof == msg_coup:
            if choix_coup == 1:
                prof.send(json.dumps(rep_coup).encode())
                print(rep_coup)
            if choix_coup == 2:
                prof.send(json.dumps(rep_coup).encode())
                print(rep_coup)
            else :
                print("Veuillez retaper le bon chiffre svp.")

        prof.close()


if client() == True:
    server()