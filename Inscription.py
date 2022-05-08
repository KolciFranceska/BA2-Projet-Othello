from cgitb import reset
from random import choice
import socket
import json
import threading
from unicodedata import name
import copy
import game2

serverAddress = ('localhost',3000)
with open('Joueur1.json') as file:  #lire les infos des deux joueurs
    Inscri1 = file.read()
with open('Joueur2.json') as file:  #pas besoin du deuxième joueur pour l'exam
    Inscri2 = file.read()

def client(Joueur):
    s = socket.socket()                             #création d'un socket
    s.connect((serverAddress))                      #on se connecte
    s.send(Joueur.encode())                         #on envoie nos infos
    response = json.loads(s.recv(2048).decode())    #on reçoit un fichier json en réponse, pour le transformer en dico python on utilise loads
    if  response == {"response": "ok"}:
        print(json.loads(Joueur)['name'], response) #voir le ping du prof
        s.close()
        return True                                 #pour continuer à écouter le server
    else:
        s.close()
        print(json.loads(Joueur)['name'], response)
        return False

def server(Joueur):
    s2 = socket.socket()                                    #créer un socket pour envoyer des msg
    serverAddress2 = ('0.0.0.0',json.loads(Joueur)['port']) #attention, cette fois-ci on envoie et écoute sur le port du joueur
    s2.bind(serverAddress2)                                 #socket en mode serveur
    s2.listen()                                             #en mode écoute pour lire ce qu'on nous envoie
    rep_ping = {"response": "pong"}

    best_bords1 = [0,7,63,56]                               #on considère que ce sont les meilleurs bords stratégiques
    best_bords2=[1,8,6,15,48,57,55,62]                      #puis ceux-là les deuxièmes meilleurs
    bords= [2,3,4,5,23,31,35,47,61,60,59,58,40,31,24,16]    #et ainsi de suite
    bords_int = [18,19,20,21,29,37,45,44,43,42,34,26]
    liste_vide =[]                                          #on en aura besoin pour envoyer un seul élément vu qu'on a plusieurs conditions

    the_move_played = int                                   #les msg qu'on va envoyer au prof
    rep_coup = {
   "response": "move",
   "move": the_move_played,
   "message": str}

    while True:                                             #important pour écouter et envoyer sans arrêt
        prof, address = s2.accept()                         #j'accepte la connexion du prof pour qu'il m'envoie des msg
        msg_prof= json.loads(prof.recv(2048).decode())      #je reçois son msg
        print(msg_prof)
        if msg_prof == {"request": "ping"}:                 #pour répondre au ping du prof
            prof.send(json.dumps(rep_ping).encode())        #convertit le dico python en fichier json
            print(json.loads(Joueur)['name'], rep_ping)     
        if msg_prof['request'] == 'play':                   #quand le prof me dmd de jouer un move
            print(possibleMoves(msg_prof['state']))         #pour voir ma liste de coup possible dans le terminal
            if len(possibleMoves(msg_prof['state'])) != 0 : #si je peux jouer un coup : je n'envoie pas de None

                for elem in possibleMoves(msg_prof['state']):                                  #je parcours les moves possibles
                    if len(liste_vide)==0:                                                     #j'utilise cette liste pour envoyer qu'un seul coup et pas plusieurs sinon == bug
                        if elem in best_bords1:                                                #je vérifie si j'ai pas un best_bords1 psq stratégiquement je les préfère
                            liste_vide.append(elem)
                            rep_coup['move']= elem                                             #je le mets dans mon dico
                            rep_coup['message']=str(rep_coup['move'])                          #le msg que je vais envoyer dans le jeu = mon move
                            prof.send(json.dumps(rep_coup).encode())                           #j'envoie tout cela au prof
                            print(json.loads(Joueur)['name'] + ': ' + str(rep_coup['move']))

                for elem in possibleMoves(msg_prof['state']):
                    if len(liste_vide)==0:
                        if elem in best_bords2:                                                #même chose ici pour best_bords2 
                            liste_vide.append(elem)
                            rep_coup['move']= elem
                            rep_coup['message']=str(rep_coup['move'])
                            prof.send(json.dumps(rep_coup).encode())
                            print(json.loads(Joueur)['name'] + ': ' + str(rep_coup['move'])) 

                for elem in possibleMoves(msg_prof['state']):
                    if len(liste_vide)==0:
                        if elem in bords:                                                      #et ainsi de suite, je le fais dans l'ordre
                            liste_vide.append(elem)                                            #càd : best_bords1, best_bords2, bords, bords_int puis random
                            rep_coup['move']= elem
                            rep_coup['message']=str(rep_coup['move'])
                            prof.send(json.dumps(rep_coup).encode())
                            print(json.loads(Joueur)['name'] + ': ' + str(rep_coup['move']))

                for elem in possibleMoves(msg_prof['state']):
                    if len(liste_vide)==0:
                        if elem in bords_int:
                            liste_vide.append(elem)
                            rep_coup['move']= elem
                            rep_coup['message']=str(rep_coup['move'])
                            prof.send(json.dumps(rep_coup).encode())
                            print(json.loads(Joueur)['name'] + ': ' + str(rep_coup['move']))

                for elem in possibleMoves(msg_prof['state']):
                    if len(liste_vide)==0:
                        if elem not in (best_bords1 and best_bords2 and bords_int and bords): #donc ici si je n'ai pas de bords dispo, je choisis aléatoirement
                            liste_vide.append(choice(possibleMoves(msg_prof["state"])))
                            rep_coup['move']= choice(possibleMoves(msg_prof["state"]))
                            rep_coup['message']=str(rep_coup['move'])
                            prof.send(json.dumps(rep_coup).encode())
                            print(json.loads(Joueur)['name'] + ': ' + str(rep_coup['move']))

            if len(possibleMoves(msg_prof['state'])) == 0:                                     #par contre si ma liste de coup possible est vide, je renvoie None
                liste_vide.append(1)
                rep_coup['move'] = None
                prof.send(json.dumps(rep_coup).encode())
                print(json.loads(Joueur)['name'] + ': ' + str(rep_coup['move']))
        liste_vide.clear()                                                                     #j'efface la liste qui me sert à renvoyer un seul coup à chaque fois

        prof.close()

directions = [                         #code du prof que je vais essayer d'expliquer...
    ( 0,  1),                          #nous prenons les différentes directions possibles qu'on peut faire sur le board
    ( 0, -1),
    ( 1,  0),
    (-1,  0),
    ( 1,  1),
    (-1,  1),
    ( 1, -1),
    (-1, -1)
]

def add(p1, p2):
    l1, c1 = p1                        #position des deux joueurs p1 et p2 leur ligne et colonne
    l2, c2 = p2
    return l1 + l2, c1 + c2

def coord(index):                       
    return index // 8, index % 8       #va nous servir à avoir le numéro de ligne et de colonne
                                       #si on donne le numéro de la case == index
def index(coord):
    l, c = coord
    return l*8+c

def isInside(coord):
    l, c = coord
    return 0 <= l < 8 and 0 <= c < 8

def walk(start, direction):
    current = start
    while isInside(current):
        current = add(current, direction)
        yield current

def isGameOver(state):
    playerIndex = state['current']          #index des deux joueurs
    otherIndex = (playerIndex+1)%2

    res = False
    if len(possibleMoves(state)) == 0:
        state['current'] = otherIndex       #l'autre joueur doit jouer si le premier n'a plus de moves
        if  len(possibleMoves(state)) == 0:
            res = True
    state['current'] = playerIndex
    return res

def willBeTaken(state, move):
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    if not (0 <= move < 64):                                                      #si on sort du board, c'est mauvais
        raise game2.BadMove('Your must be between 0 inclusive and 64 exclusive')

    if move in state['board'][0] + state['board'][1]:
        raise game2.BadMove('This case is not free')

    board = []
    for i in range(2):
        board.append(set((coord(index) for index in state['board'][i])))

    move = coord(move)

    cases = set()
    for direction in directions:
        mayBe = set()
        for case in walk(move, direction):
            if case in board[otherIndex]:
                mayBe.add(case)
            elif case in board[playerIndex]:
                cases |= mayBe
                break
            else:
                break

    if len(cases) == 0:
        raise game2.BadMove('Your move must take opponent\'s pieces')
    
    return [index(case) for case in cases]

def possibleMoves(state):                #renvoie une liste de coups possibles
    print(state)
    res = []
    for move in range(64):
        try:
            willBeTaken(state, move)
            res.append(move)
        except game2.BadMove:
            pass
    return res

def Othello(players):
    # 00 01 02 03 04 05 06 07
    # 08 09 10 11 12 13 14 15
    # 16 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30 31
    # 32 33 34 35 36 37 38 39
    # 40 41 42 43 44 45 46 47
    # 48 49 50 51 52 53 54 55
    # 56 57 58 59 60 61 62 63

    state = {
        'players': players,
        'current': 0,
        'board': [
            [28, 35],
            [27, 36]
        ]
    }

    def next(state, move):                        #renvoie l'état suivant par rapport au move qu'on envoie
        newState = copy.deepcopy(state)
        playerIndex = state['current']
        otherIndex = (playerIndex+1)%2

        if len(possibleMoves(state)) > 0 and move is None:
            raise game2.BadMove('You cannot pass your turn if there are possible moves')

        if move is not None:
            cases = willBeTaken(state, move)

            newState['board'][playerIndex].append(move)

            for case in cases:
                newState['board'][otherIndex].remove(case)
                newState['board'][playerIndex].append(case)
            
        newState['current'] = otherIndex

        if isGameOver(newState):
            if len(newState['board'][playerIndex]) > len(newState['board'][otherIndex]):
                winner = playerIndex
            elif len(newState['board'][playerIndex]) < len(newState['board'][otherIndex]):
                winner = otherIndex
            else:
                raise game2.GameDraw(newState)
            raise game2.GameWin(winner, newState)
        
        return newState

    return state, next

Game = Othello

while True :
    if client(Inscri1)==True:
        server(Inscri1)