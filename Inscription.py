import socket
import json
import threading
from unicodedata import name
import copy
from game import game

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
   "message": str}

    while True:
        prof, address = s2.accept()
        msg_prof= json.loads(prof.recv(2048).decode())
        print(msg_prof)
        if msg_prof == {"request": "ping"}:
            prof.send(json.dumps(rep_ping).encode()) #convertit le dico python en fichier json
            print(json.loads(Joueur)['name'], rep_ping)
        if msg_prof['request'] == 'play':
            rep_coup['move']= int(input(json.loads(Joueur)['name'] + " sélectionnez une case pour jouer: "))
            rep_coup['message']=str(rep_coup['move'])
            prof.send(json.dumps(rep_coup).encode())
            print(rep_coup)
        prof.close()

directions = [
    ( 0,  1),
    ( 0, -1),
    ( 1,  0),
    (-1,  0),
    ( 1,  1),
    (-1,  1),
    ( 1, -1),
    (-1, -1)
]

def add(p1, p2):
    l1, c1 = p1
    l2, c2 = p2
    return l1 + l2, c1 + c2

def coord(index):
    return index // 8, index % 8

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
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    res = False
    if len(possibleMoves(state)) == 0:
        state['current'] = otherIndex
        if  len(possibleMoves(state)) == 0:
            res = True
    state['current'] = playerIndex
    return res

def willBeTaken(state, move):
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    if not (0 <= move < 64):
        raise game.BadMove('Your must be between 0 inclusive and 64 exclusive')

    if move in state['board'][0] + state['board'][1]:
        raise game.BadMove('This case is not free')

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
        raise game.BadMove('Your move must take opponent\'s pieces')
    
    return [index(case) for case in cases]

def possibleMoves(state):
    res = []
    for move in range(64):
        try:
            willBeTaken(state, move)
            res.append(move)
        except game.BadMove:
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

    def next(state, move):
        newState = copy.deepcopy(state)
        playerIndex = state['current']
        otherIndex = (playerIndex+1)%2

        if len(possibleMoves(state)) > 0 and move is None:
            raise game.BadMove('You cannot pass your turn if there are possible moves')

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
                raise game.GameDraw(newState)
            raise game.GameWin(winner, newState)
        
        return newState

    return state, next

Game = Othello

if __name__ == '__main__':
    state, next = Game(['LUR', 'HSL'])

    move = 26

    print(next(state, move))


def jouer():
    if client(Inscri1) == True:
        server(Inscri1)

thread = threading.Thread(target = jouer, daemon = True)
thread.start()
while True :
    if client(Inscri2)==True:
        server(Inscri2)