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

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
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
            raise QuoridorError("L'argument 'joueurs' n'est pas un itérable.")
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
            for i in enumerate(joueurs):
                if not 0 <= i[1]['murs'] <= 10:
                    raise QuoridorError("Le nombre de murs à placer est entre 0 et 10.")
                if not 1 <= i[1]['pos'][0] <= 9 or not 1 <= i[1]['pos'][1] <= 9:
                    raise QuoridorError("La position d'un joueur n'est pas valide!")
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
                    raise QuoridorError("Il y a un mur dont la position est invalide")
            for i in enumerate(murs['verticaux']):
                if not 2 <= i[1][0] <= 9 or not 1 <= i[1][1] <= 8:
                    raise QuoridorError("Il y a un mur dont la position est invalide")
            self.murs = murs

        #Nombre maximal de murs en circulation
        if self.joueurs[0]['murs'] + self.joueurs[1]['murs'] + len(self.murs['horizontaux']) + len(self.murs['verticaux']) != 20:
            raise QuoridorError("Nombre total de murs invalide (seul nombre autorisé: 20).")

        #Les possibilités de mouvement d'un joueur selon l'état du jeu
        self.graphe = 'oui'

    def __str__(self):
        '''fonction pour afficher le damier''' 
        le = 'Légende: 1={}, 2={}'.format(self.joueurs[0]['nom'], self.joueurs[1]['nom'])
        gb = []
        for i in range(9):
            f1 = [' ', ' ', '.', ' ']*9 + ['|']
            f1[0] = f'\n{i+1} |'
            gb += [f1]
            hb = [' ']*36 + ['|']
            hb[0] = '\n  |'
            gb += [hb]
        ve = self.murs['verticaux']
        ho = self.murs['horizontaux']
        pos1 = self.joueurs[0]['pos']
        pos2 = self.joueurs[1]['pos']
        for i in range(len(ve)):
            for j in range(3):
                gb[ve[i][1]*2 - 2+j][ve[i][0]*4 -4] = '|'
        for i in range(len(ho)):
            for j in range(7):
                gb[ho[i][1]*2 - 3][ho[i][0]*4 - 3 + j] = '-'
        gb[pos1[1]*2 - 2][pos1[0]*4 - 2] = '1'
        gb[pos2[1]*2 - 2][pos2[0]*4 - 2] = '2'
        s = []
        gb.reverse()
        for i in range(17):
            s += ''.join(gb[i+1])
        ch = le + '\n    ' + '-'*35 + ''.join(s) + '\n--|' + '-'*35 + '\n  | 1   2   3   4   5   6   7   8   9'
        return ch      


    def déplacer_jeton(self, joueur, position):
        '''Pour déplacer un jeton à une position'''

        #Les possibilités de mouvement d'un joueur selon l'état du jeu
        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murs['horizontaux'],
            self.murs['verticaux']
            )

        #Contraintes et déplacement du jeton
        if joueur not in [1, 2]:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
        if not (1 <= position[0] <= 9 and 1 <= position[1] <= 9):
            raise QuoridorError("Cette position n'existe pas sur le plateau de jeu.")
        if position not in list(self.graphe.successors(self.joueurs[joueur - 1]['pos'])):
            raise QuoridorError("Cette position est invalide pour l'état actuel du jeu.")

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

        if joueur not in [1, 2]:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
        if self.partie_terminée() is not False:
            raise QuoridorError("La partie est déjà terminée.")
        
        #Stratégie du meilleur coup
        if joueur == 1:
            cheminC1 = nx.shortest_path(self.graphe, self.joueurs[0]['pos'], 'B1')
            cheminC2 = nx.shortest_path(self.graphe, self.joueurs[1]['pos'], 'B2')
            if cheminC1
        
        if joueur == 2:
            cheminC2 = nx.shortest_path(self.graphe, self.joueurs[1]['pos'], 'B2')
            cheminC1 = nx.shortest_path(self.graphe, self.joueurs[0]['pos'], 'B1')
        
        self.déplacer_jeton(joueur, chemin[1])


    def partie_terminée(self):
        '''Pour arrêter la partie si elle est terminée'''
        if self.joueurs[0]['pos'][1] == 9:
            return 'Le gagnant est {}'.format(self.joueurs[0]['nom'])
        if self.joueurs[1]['pos'][1] == 1:
            return 'Le gagnant est {}'.format(self.joueurs[1]['nom'])
        if self.joueurs[0]['pos'][1] != 9 and self.joueurs[1]['pos'][1] != 1:
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
        if joueur not in {1, 2}:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
        if self.joueurs[joueur - 1]['murs'] == 0:
            raise QuoridorError("Tu as déjà placé tous tes murs :'(")
        self.joueurs[joueur - 1]['murs'] -= 1


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
                self.murs['horizontaux'].remove(position)
                raise QuoridorError("Le joueur 1 est enfermé! Shame on you.")
            if nx.has_path(self.graphe, self.joueurs[1]['pos'], 'B2') is False:
                self.murs['horizontaux'].remove(position)
                raise QuoridorError("Le joueur 2 est enfermé! Shame on you.")

        #Placement d'un mur vertical
        elif orientation == 'vertical':
            #S'assurer que le mur peut être placé d'après les dimensions du board
            if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                raise QuoridorError('Tu ne peux pas placer un mur à cet endroit')

            #S'assurer que ce nouveau mur vertical ne croise pas un autre mur
            if (position[0] - 1, position[1] + 1) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            if (position[0], position[1] - 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            if position in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            if (position[0], position[1] + 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')

            self.murs['verticaux'].append(position)

            #S'assurer que les joueurs ne sont pas enfermés
            if nx.has_path(self.graphe, self.joueurs[0]['pos'], 'B1') is False:
                self.murs['verticaux'].remove(position)
                raise QuoridorError("Le joueur 1 est enfermé! Shame on you.")
            if nx.has_path(self.graphe, self.joueurs[1]['pos'], 'B2') is False:
                self.murs['verticaux'].remove(position)
                raise QuoridorError("Le joueur 2 est enfermé! Shame on you.")
    