'''Encadrer le jeu avec une classe'''
from random import random
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
        '''fonction pour afficher le damier''' 
        le = 'Légende: 1={}, 2={}'.format(self.joueurs[0], self.joueurs[1])
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
        ch = (le + '\n    '+'-'*35 + ''.join(s) +
              '\n--|'+'-'*35+'\n  | 1   2   3   4   5   6   7   8   9')
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
        """Pour jouer le meilleur coup automatique"""

        #Les possibilités de mouvement d'un joueur selon l'état du jeu
        self.graphe = construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murs['horizontaux'],
            self.murs['verticaux']
            )

        if not joueur in {1, 2}:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
        if self.partie_terminée() is not False:
            raise QuoridorError("La partie est déjà terminée.")

        def placer_mur_devant(joueur, a):
            """fonction pour placer un mur devant le joueur adversaire"""
            
            if a[2][0]-a[1][0] == 0:
                #Pour savoir si le chemin le plus court est vertical
                em = [a[2][0]]
                if a[2][0] == 9:
                    #pour ne pas que le mur sort du damier
                    em = [8]
                if a[2][1]-a[1][1] == -1:
                    #pour mettre le mur en bas du joueur lorsqu'il doit déscendre
                    em.insert(1, a[2][1]+1)
                else:
                    #Pour mettre le mur en haut du joueur lorsqu'il doit monter
                    em.insert(1, a[2][1]) 

                ori = 'horizontal'
            if a[2][1]-a[1][1] == 0:
            #Pour savoir si le chemin le plus court est horizontal
                em = [a[2][1]]
                if a[2][1] == 9:
                    #Pour ne pas que le mur sorte du damier
                    em = [8]

                if a[2][0]-a[1][0] == -1:
                    #Pour mettre le mur à gauche lorsque le chemin le plus court est à gauche
                    em.insert(0, a[2][0]+1)
                else:
                    #Pour mettre le mur à droite lorsque le chemin le plus court est à droite
                    em.insert(0, a[2][0])
                ori = 'vertical'
                Quoridor.placer_mur(self, joueur, em, ori)

        possibilité = [1, 2]
        possibilité.remove(joueur)
        adversaire = possibilité[0]
        #L'adversaire prend le numero restant entre 1 et 2

        chemin = nx.shortest_path(self.graphe, self.joueurs[joueur - 1]['pos'], f'B{joueur}')[0]
        chemin_adversaire = nx.shortest_path(self.graphe, self.joueurs[adversaire - 1]['pos'], f'B{adversaire}')[0]
        if len(chemin) <= len(chemin_adversaire):

            if random() <= 0.1*self.joueurs[joueur - 1]['mur']-0.1:
                #fonction qui place des murs aléatoirement mais proportionnelement au nombres de murs restants
                #il restera cepedant toujours un mur pour le garder en cas où l'adversaire allait gagner
                placer_mur_devant(joueur, chemin_adversaire)
            else:
                #Avancer le jeton vers son but
                Quoridor.déplacer_jeton(self, joueur, chemin[1])    


        if len(chemin_adversaire) == 2:
            #toujours placer un mur devant l'adversaire lorsqu'il est à un déplacement de gagner
            placer_mur_devant(joueur, chemin_adversaire)

        else:
            #Si le chemin de l'adversaire est plus court que le nôtre, on place un mur devant celui-ci
            placer_mur_devant(joueur, chemin_adversaire)


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
                self.murs['horizontaux'].remove(position)
                raise QuoridorError("Le joueur 1 est enfermé! Shame on you.")
            elif nx.has_path(self.graphe, self.joueurs[1]['pos'], 'B2') is False:
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
                self.murs['verticaux'].remove(position)
                raise QuoridorError("Le joueur 1 est enfermé! Shame on you.")
            elif nx.has_path(self.graphe, self.joueurs[1]['pos'], 'B2') is False:
                self.murs['verticaux'].remove(position)
                raise QuoridorError("Le joueur 2 est enfermé! Shame on you.")

