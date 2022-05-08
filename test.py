from random import choice

bords = [1,2,3,4,5,6]
best_bords = [9,10,7]
ma_liste = [1,2,3,9,10,11,8,0]
liste_vide = []

for elem in ma_liste:
    if len(liste_vide)==0:
        if elem in best_bords:
            liste_vide.append(elem)
            print(elem)

for elem in ma_liste:
    if len(liste_vide)==0:
        if elem in bords :
            liste_vide.append(elem)
            print(elem)

for elem in ma_liste:
    if len(liste_vide)==0:
        if elem not in (best_bords and bords):
            liste_vide.append(elem)    
            print(choice(ma_liste))

# Dans ce cas-ci je veux que le code me print 9
# Mais ça me print 4 psq il fait pas le tour de toute ma liste