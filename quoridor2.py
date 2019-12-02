'''Encadrer le jeu avec une classe'''

import networkx as nx

def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    joueurs = list(map(tuple, joueurs))
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    prédécesseurs = list(list(graphe.predecessors(joueur)) for joueur in map(tuple, joueurs))
    successors = list(list(graphe.successors(joueur)) for joueur in map(tuple, joueurs))

    for i, joueur in enumerate(joueurs):

        for prédécesseur in prédécesseurs[i]:
            # retire tous les liens menant à la position d'un joueur
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur_en_ligne = tuple(
                2*joueur[i]-prédécesseur[i] for i in range(len(joueur))
            )

            if successeur_en_ligne in set(successors[i])-set(joueurs):
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur_en_ligne)
            else:
                # ajouter les liens en diagonale
                successeur_diag_1 = tuple(
                    joueur[i]+(joueur[-(i+1)]-prédécesseur[-(i+1)])
                    for i in range(len(joueur))
                )
                if successeur_diag_1 in set(successors[i])-set(joueurs):
                    graphe.add_edge(prédécesseur, successeur_diag_1)
                successeur_diag_2 = tuple(
                    joueur[i]-(joueur[-(i+1)]-prédécesseur[-(i+1)])
                    for i in range(len(joueur))
                )
                if successeur_diag_2 in set(successors[i])-set(joueurs):
                    graphe.add_edge(prédécesseur, successeur_diag_2)


    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe

class QuoridorError(Exception):
    '''Pour pouvoir utiliser toutes les méthodes de la classe 'Exception'
        sous le nom 'QuoridorError' '''

class Quoridor:
    '''Pour encadrer le jeu'''
    
    def __init__(self, joueurs, murs=None):

        #Erreurs de base à soulever
        if not hasattr(joueurs, '__iter__'):
            raise QuoridorError("Ton argument 'joueurs' n'est pas un itérable.")
        if len(joueurs) > 2:
            raise QuoridorError("On ne veut jouer qu'à deux joueurs.")
        
        #Si 'joueurs' est un itérable de strings, créer la liste de dictionnaires
        if isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.joueurs = [
                {'nom': joueurs[0], 'murs': 10, 'pos': (5, 1)},
                {'nom': joueurs[1], 'murs': 10, 'pos': (5, 9)},
            ]
            
        #Si 'joueurs' est un itérable de dictionnaires, les traiter
        if isinstance(joueurs[0], dict) and isinstance(joueurs[1], dict):
            for i in joueurs:
                if not 0 <= joueurs[i]['murs'] <= 10:
                    raise QuoridorError("Le nombre de murs à placer est entre 0 et 10.")
                if not 1 <= joueurs[i]['pos'][0] <= 9 or not 1 <= joueurs[i]['pos'][1] <= 9:
                    raise QuoridorError("La position que tu essaies d'entrer n'est pas valide!")
            self.joueurs = joueurs
            
        #Si les murs n'existent pas encore, créer le dictionnaire
        if murs is None:
            self.murs = {'horizontaux': [], 'verticaux': []}
            
        #Si les murs existent, les traiter
        else:
            if not isinstance(murs, dict):
                raise QuoridorError("Ton argument 'murs' n'est pas un dictionnaire.")
                
            for i in enumerate(murs['horizontaux']):
                if not 1 <= i[1][0] <= 8 or not 2 <= i[1][1] <= 9:
                    raise QuoridorError("Position de mur invalide")
            for i in enumerate(murs['verticaux']):
                if not 2 <= i[1][0] <= 9 or not 1 <= i[1][1] <= 8:
                    raise QuoridorError("Position de mur invalide")
                
            self.murs = murs
        
        #Nombre maximal de murs en circulation
        if self.joueurs[0]['murs'] + self.joueurs[1]['murs'] + len(self.murs['horizontaux']) + len(self.murs['verticaux']) != 20:
            raise QuoridorError("Nombre total de murs invalide (seul nombre autorisé: 20).")
        
        #Les possibilités de mouvement d'un joueur selon l'état du jeu
        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murs['horizontaux'],
            self.murs['verticaux']
            )
            
            
    def __str__(self):
        '''Pour afficher le board'''
        
        def afficher_damier_ascii(dico):
            '''Pour afficher le damier à partir d'un état de jeu'''
            #joueur 1 (personne)
            hauteurp = dico["joueurs"][0]["pos"][1]
            longueurp = dico["joueurs"][0]["pos"][0]
            #joueur 2 (robot)
            hauteurr = dico["joueurs"][1]["pos"][1]
            longueurr = dico["joueurs"][1]["pos"][0]
            #Murs
            murh = dico["murs"]["horizontaux"]
            murv = dico["murs"]["verticaux"]

            #Board vide (en string)

            #Lignes qui changent
            lignes = ''
            for i in range(17):
                if (i+1) % 2 == 1:
                    lignes += str(int(9-0.5*i)) + ' | .' + '   .'*8 + ' |' + '\n'
                else:
                    lignes += ' ' + ' |' + ' '*35 +'|' + '\n'

            #Board modifié (en liste)
            boardm = []
            for ligne in lignes.splitlines():
                boardm.append(list(ligne))

            #Joueurs
            for i in range(9):
                if int(boardm[i*2][0]) == hauteurp:
                    boardm[i*2][longueurp*4] = '1'
                if int(boardm[i*2][0]) == hauteurr:
                    boardm[i*2][longueurr*4] = '2'

            #Murs horizontaux
            for k in range(len(murh)):
                for i in range(9):
                    if int(boardm[i*2][0]) == murh[k][1]:
                        for j in range(7):
                            boardm[(i + 1)*2 - 1][murh[k][0]*4 - 1 + j] = '-'

            #Murs verticaux
            for k in range(len(murv)):
                for i in range(9):
                    if int(boardm[i*2][0]) == murv[k][1]:
                        for j in range(3):
                            boardm[i*2 - j][murv[k][0]*4 - 2] = '|'

            #Board final (en string)
            boardf = ''
            for i in range(len(boardm)):
                lignesf = ''
                for j in range(len(boardm[0])):
                    lignesf += str(boardm[i][j])
                boardf += lignesf + '\n'
            #Autres lignes non modifiées
            legend = 'Légende: 1={}, 2={}\n'.format(dico["joueurs"][0]["nom"], dico["joueurs"][1]["nom"])
            ligne1 = ' '*3 + '-'*35 + '\n'
            lignef = '--|' + '-'*35 + '\n'
            lignef2 = '  |' + ' 1'
            for i in range(8):
                lignef2 += ' '*3 + str(i + 2)
            #Board final
            boardfinal = legend + ligne1 + boardf + lignef + lignef2 +'\n'
            print(boardfinal)

        afficher_damier_ascii(self.état_partie())
            
            
            
    def déplacer_jeton(self, joueur, position):
        '''Pour déplacer un jeton à une position'''
        
        #Les possibilités de mouvement d'un joueur selon l'état du jeu
        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murs['horizontaux'],
            self.murs['verticaux']
            )
        
        #Contraintes et déplacement du jeton
        if not joueur in {1, 2}:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
        if not (1 <= position[0] <= 9 and 1 <= position[1] <= 9):
            raise QuoridorError("Cette position n'existe pas!")
        if position not in list(self.graphe.successors(self.joueurs[joueur - 1]['pos'])):
            raise QuoridorError("Tu ne peux pas aller là!")
        
        self.joueurs[joueur - 1]['pos'] = position
            
            
        
        
    def état_partie(self):
        '''Pour produire le dictionnaire d'état de jeu'''
        return {'joueurs': self.joueurs, 'murs': self.murs}

    def jouer_coup(self, joueur):
        '''Pour jouer le meilleur coup d'un joueur
        (manoeuvre automatisée pas très smat, sans murs)'''
        
        #Les possibilités de mouvement d'un joueur selon l'état du jeu
        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murs['horizontaux'],
            self.murs['verticaux']
            )
        
        if joueur in {1, 2}:
            chemin = nx.shortest_path(self.graphe, self.joueurs[joueur - 1]['pos'], f'B{joueur}')
            options = list(self.graphe.successors(chemin[0]))
            if self.partie_terminée() is False and chemin[1] in options:
                self.déplacer_jeton(joueur, chemin[1])
            else:
                raise QuoridorError("La partie est déjà terminée.")
        else:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")

    def partie_terminée(self):
        '''Pour arrêter la partie si elle est terminée'''
        if self.joueurs[0]['pos'][1] == 9:
            return 'Le gagnant est {}'.format(self.joueurs[0]['nom'])
        elif self.joueurs[1]['pos'][1] == 1:
            return 'Le gagnant est {}'.format(self.joueurs[1]['nom'])
        else:
            return False


    def placer_mur(self, joueur, position, orientation):
        '''Pour placer un mur à une position'''
        
        #Les possibilités de mouvement d'un joueur selon l'état du jeu
        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murs['horizontaux'],
            self.murs['verticaux']
            )
        
        #S'assurer que le numéro de joueur est 1 ou 2 et traiter le nombre de murs en banque.
        if joueur in {1, 2}:
            if self.joueurs[joueur - 1]['murs'] != 0:
                self.joueurs[joueur - 1]['murs'] -= 1
            else:
                raise QuoridorError("Tu as déjà placé tous tes murs :'(")
        else:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
    
        
        #Placement d'un mur horizontal
        if orientation == 'horizontal':
            #S'assurer que le mur peut être placé d'après les dimensions du board
            if not 1 <= position[0] <= 8 or not 2 <= position[1] <= 9:
                raise QuoridorError('Tu ne peux pas placer un mur à cet endroit')
            
            #S'assurer que ce nouveau mur horizontal ne croise pas un autre mur
            if (position[0] + 1, position[1] - 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            if (position[0] + 1, position[1]) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            if position in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            if (position[0] - 1, position[1]) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            
            self.murs['horizontaux'].append(position)
            
            #S'assurer que les joueurs ne sont pas enfermés
            if nx.has_path(self.graphe, self.joueurs[0]['pos'], 'B1') is False:
                raise QuoridorError("Le joueur 1 est enfermé! Shame on you.")
            elif nx.has_path(self.graphe, self.joueurs[1]['pos'], 'B2') is False:
                raise QuoridorError("Le joueur 2 est enfermé! Shame on you.")
                
        #Placement d'un mur vertical
        elif orientation == 'vertical':
            #S'assurer que le mur peut être placé d'après les dimensions du board
            if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                raise QuoridorError('Tu ne peux pas placer un mur à cet endroit')
            
            #S'assurer que ce nouveau mur vertical ne croise pas un autre mur
            if (position[0] - 1, position[1] + 1) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif (position[0], position[1] - 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif position in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif (position[0], position[1] + 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            else:
                self.murs['verticaux'].append(position)
                
            #S'assurer que les joueurs ne sont pas enfermés
            if nx.has_path(self.graphe, self.joueurs[0]['pos'], 'B1') is False:
                raise QuoridorError("Le joueur 1 est enfermé! Shame on you.")
            elif nx.has_path(self.graphe, self.joueurs[1]['pos'], 'B2') is False:
                raise QuoridorError("Le joueur 2 est enfermé! Shame on you.")
