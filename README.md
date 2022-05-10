# Projet BA2 Othello 


__Auteur :__   

  Françeska Kolçi 195387 
   
  Aouragh Ibrahim 20187 

 

Bonjour à tous,  

Dans le cadre du cours d’informatique en 2Bac à l’Ecam, nous avons dû créer une intelligence artificielle qui sera évaluée lors d’un tournoi de classe.  Notre I.A est capable de jouer au jeu Othello de manière autonome et intelligente.  Si vous ne connaissez pas le jeu Othello, nous vous invitons à aller regarder cette vidéo: [e-genieclimatique](https://www.youtube.com/watch?v=Z5EN-cbgo-4&feature=emb_imp_woyt).    

 

# Déroulement du tournoi  

Avant de commencer à analyser notre code, nous allons vous expliquez comment va se dérouler ce tournoi.  Les élèves devront s’inscrire au serveur du professeur. Dès que deux élèves seront inscrits, le serveur lancera les matchs.  Lors des matchs, le serveur ne cessera de demander aux I.A des élèves quel coup ils veulent jouer.  Ces échanges se feront à travers des fichiers JSON.  Pour toute autre information, nous avons invitons à lire le Read ME et le code du professeur : [e-genieclimatique](https://github.com/qlurkin/PI2CChampionshipRunner). 

 

# Notre code  

Découvrons ensemble les différentes parties de notre code:    
  1. Joueur1.json et joueur2.json    
  2. Insciption.py    
  3. Random.py  
  4. Game2.py  

 
## *1) Joueur1.json et joueur2.json*   

Ces fichiers sont ceux que nous utilisons afin de communiquer avec le serveur du prof.  Evidemment, nous n’aurons pas besoin du joueur2 lors du tournoi, nous l’utilisons juste pour nos tests.  Ces fichiers JSON sont structurés de cette manière :  

{ 

    "request": "subscribe",  
    "port": 8888,  
    "name": "Frann",  
    "matricules": ["195387"]  
 } 

Ces informations vont être envoyées au prof et grâce à cet envoi, nous saurons qui joue et quel coup la personne joue.  

 

## *2) Inscription.py*  

Inscription.py est note code principal.  En effet, c’est dans ce code que nous communiquons au serveur, établissons les coups possibles et notre stratégie, étudions les éventuelles « Bad move » et peaufinons quelques détails.  

Evidemment, toutes nos définitions ne seront pas expliquées sur le « Read me ».  Toutefois, nous vous invitons à lire les commentaires associés à nos fonctions.    

La connexion au serveur se fait au moyen de deux fonctions : « client(joueur) et server(joueur) ».  La fonction client est celle que nous allons utiliser afin de pouvoir se connecter au serveur du prof.  La fonction server va pouvoir être utiliser afin d’envoyer des informations aux serveur et écouter en permanence sur le port du joueur.  

Après s’être connecté au serveur du prof, nous avons créé une fonction « possibleMoves » qui nous renvoi sous forme de liste tous les coups possibles que nous pouvons jouer.  Notre avons ensuite créé plusieurs listes de cases que nous considérons comme étant les meilleures à jouer.   Nous mettons dans l’ordre les moves du plus important au moins important qu’on privilégie pour notre stratégie : nous sélectionnons d’abord un élément de la liste « Best_bords1 »,  s’il n’y en a pas alors on cherche une move dans la liste « Best_bords2 », même chose s’il n'y a toujours pas de moves à faire dans ces cases-là, on choisit la liste « Bords Int ».  
Et enfin si nous n’avons toujours pas de moves figurant dans une de ces listes, nous choisissons un élément Random de nos moves possibles.

Pour résumer, notre stratégie consiste à parcourir tous les coups possibles et choisir la meilleure d’entre-elle, selon nos critères.  

## *3) Random.py*  
Cette partie de code nous sert à perfectionner notre stratégie. En effet, ce sont des matchs qui se disputent contre notre I.A et un Random. 

## *4) Game2.py*  
Ce code veille au bon déroulement de la partie et du respect des règles. Notamment à ne pas faire de « Bad move » ou d’erreur. 

# Les bibliothèques utilisées  

Nous avons utilisé plusieurs bibliothèques afin de faire notre projet.  Nous avons importé les sockets pour la création du serveur, JSON pour créer nos fichiers qui communique avec le serveur du prof et random pour pouvoir jouer aléatoirement.

 
