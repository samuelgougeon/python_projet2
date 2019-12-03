class QuoridorError(Exception):
    pass


class Quoridor():
    
    def __init__(self, joueurs, murs=None):

            #Erreurs à soulever
        if not isinstance(joueurs, iter):
            raise QuoridorError("Ton argument 'joueurs' n'est pas un itérable.")
        if len(joueurs) > 2:
            raise QuoridorError("On ne veut jouer qu'à deux joueurs.")
        
        
        
        
            #Si 'joueurs' est un itérable de dictionnaires
        if type(joueurs[0]) == dict and type(joueurs[1]) == dict:
            if 0 > joueurs[0]['murs'] > 10 or 0 > joueurs[1]['murs'] > 10:
                raise QuoridorError('le nombre de murs diposnible pour un joueur est négatif ou suppérieur à 0')
            self.joueurs = joueurs
            
        elif type(joueurs[0]) == str and type(joueurs[1]) == str:
            self.joueurs = [
                {'nom': joueurs[0], 'murs': 10, 'pos': (5, 1)},
                {'nom': joueur[1], 'murs': 10, 'pos': (5, 9)},
            ],
            
                
            
        if murs != None:
            self.murs = murs
                
            if type(murs) != dict:
                raise QuoridorError("Ton argument 'murs' n'est pas un dictionnaire.")
            if joueurs[0]['murs'] + joueurs[1]['murs'] + len(murs['horizontaux']) + len(murs['verticaux']) != 20:
                raise QuoridorError("Il y a plus de 20 murs (nombre max autorisé) dans le jeu")
                
            for i in enumerate(murs['horizontaux']):
                if not 1 <= i[1][0] <= 8 or not 2 <= i[1][1] <= 9:
                    raise QuoridorError("Position de mur invalide")
            for i in enumerate(murs['verticaux']):
                if not 2 <= i[1][0] <= 9 or not 1 <= i[1][1] <= 8:
                    raise QuoridorError("Position de mur invalide")
        else:
            self.murs = {'horizontaux': [],
            'verticaux': []}        

        

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie. 
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """
        '''fonction pour afficher le damier'''
        u1 = self.joueurs[0]['nom']
        u2 = self.joueurs[1]['nom']
        le = f'Légende: 1={u1}, 2={u2}'
        gb = []
        for i in range(9):
            f1 = [' ', ' ', '.', ' ']*9 + ['|']
            f1[0] = f'\n{i+1}  |'
            gb += [f1]
            hb = [' ']*36 + ['|']
            hb[0] = '\n   |'
            gb += [hb]
        ve = self.murs['verticaux']
        ho = self.murs['horizontaux']
        pos1 = self.joueurs[0]['pos']
        pos2 = self.joueurs[1]['pos']
        for i in range(len(ve)):
            for j in range(3):
                gb[ve[i][1]*2 - 2+j][ve[i][0]*4 - 4] = '|'
        for i in range(len(ho)):
            for j in range(7):
                gb[ho[i][1]*2 - 3][ho[i][0]*4 - 3 + j] = '-'
        gb[pos1[1]*2 - 2][pos1[0]*4 - 2] = '1'
        gb[pos2[1]*2 - 2][pos2[0]*4 - 2] = '2'
        s = []
        gb.reverse()
        for i in range(17):
            s += ''.join(gb[i+1])
        print(le + '\n    '+'-'*35 + ''.join(s) +
              '\n --|'+'-'*35+'\n   | 1   2   3   4   5   6   7   8   9')
            
            





    
    def déplacer_jeton(self, joueur, positionJ):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """
        if joueur != 1 or joueur != 2:
            raise QuoridorError('Le joueur doit être définit entre 1 et 2')
        elif 1 > positionJ[0] > 10 or 1 > positionJ[1] > 10:
            raise QuoridorError("La position n'est pas comprise entre 1 et 9 pour x et y")
        NETWORKX


    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }
        
        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée 
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est 
        associée à sa position sur le damier. Une position est représentée par un tuple 
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel 
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un 
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """

    def partie_terminée(self):
        if self.joueurs[0]['pos'][1] == 9:
            return f'Le gagant est {self.joueurs[0]['nom']}'
        elif self.joueurs[1]['pos'][1] == 1:
            return f'Le gagant est {self.joueurs[1]['nom']}'
        else:
            return False 

    def placer_mur(self, joueur, positionM, orientation):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un mur occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises Quor   """
        if joueur != 1 and joueur != 2:
            raise QuoridorError('Numéro du joueur requis entre 1 et 2')
        
        for i in self.murs['horizontaux']
        if positionM == 
        elif for i in self.murs['horizontaux'] == positionM or for i in self.murs['verticaux']:
            raise QuoridorError('la position de ce mur est déja occupé')
        
        
        if self.joueurs[joueur - 1]['murs'] == 0:
            raise QuoridorError('le nombre de murs restant est nul')
        if joueur == 1:
            self.joueurs[0]['murs'] -= 1
        if joueur == 2:
            self.joueurs[1]['murs'] -= 1

        if orientation == 'horizontal':
            if 1 > positionM[0] > 8 or 2 > positionM[1] > 9:
                raise QuoridorError('La position est invalide pour cette orientation')
            for i in self.murs['horizontaux']:
                if i == positionM or (i[0] - 1, i[1]) == positionM or (i[0] + 1, i[1]) == positionM:
                    raise QuoridorError('un mur est déja placé pour cette position')
            for i in self.murs['verticaux']:
                if (i[0] + 1, i[1] - 1) == positionM:
                    raise QuoridorError('un mur est déja placé pour cette position')
            self.murs['horizontaux'].append(positionM)

        if orientation == 'vertical':
            if 2 > positionM[0] > 9 or 1 > positionM[1] > 8:
                raise QuoridorError('La position est invalide pour cette orientation')
            for i in self.murs['verticaux']:
                if i == positionM or (i[0], i[1] - 1) == positionM or (i[0], i[1] + 1) == positionM:
                    raise QuoridorError('un mur est déja placé pour cette position')
            for i in self.murs['horizontaux']:
                if (i[0] - 1, i[1] + 1) == positionM:
                    raise QuoridorError('un mur est déja placé pour cette position')
            self.murs['verticaux'].append(positionM)

        if not nx.has_path(graphe, self.murs[0]['pos'], 'B1') or not nx.has_path(graphe, self.murs[1]['pos'], 'B2'):
            if orientation = 'horizontal':
                self.murs['horizontaux'].remove(positionM)
                raise QuoridorError('la position du mur emprisonne un joueur')
            if orientation = 'vertical':
                self.murs['verticaux'].remove(positionM)
                raise QuoridorError('la position du mur emprisonne un joueur')


           



    