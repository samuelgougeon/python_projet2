'''Encadrer le jeu avec une classe'''

import networkx_utile

class QuoridorError(Exception):
    '''Pour pouvoir utiliser toutes les méthodes de la classe 'Exception'
        sous le nom 'QuoridorError' '''

class Quoridor:
    '''Pour encadrer le jeu'''
    def __init__(self, joueurs, murs=None):

        #Erreurs de base à soulever
        if not isinstance(joueurs, iter):
            raise QuoridorError("Ton argument 'joueurs' n'est pas un itérable.")
        if len(joueurs) > 2:
            raise QuoridorError("On ne veut jouer qu'à deux joueurs.")
        
        #Si 'joueurs' est un itérable de strings
        if isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.joueurs = [
                {'nom': joueurs[0], 'murs': 10, 'pos': (5, 1)},
                {'nom': joueurs[1], 'murs': 10, 'pos': (5, 9)},
            ]
            
        #Si 'joueurs' est un itérable de dictionnaires
        if isinstance(joueurs[0], dict) and isinstance(joueurs[1], dict):
            for i in joueurs:
                if not 0 <= joueurs[i]['murs'] <= 10:
                    raise QuoridorError("Le nombre de murs à placer est entre 0 et 10.")
                if not 1 <= joueurs[i]['pos'][0] <= 9 or not 1 <= joueurs[i]['pos'][1] <= 9:
                    raise QuoridorError("La position que tu essaies d'entrer n'est pas valide!")
            self.joueurs = joueurs
            
            
        #Si les murs n'existent pas encore
        if murs is None:
            self.murs = {'horizontaux': [], 'verticaux': []}
            
        #Si les murs existent
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
            
            if self.joueurs[0]['murs'] + self.joueurs[1]['murs'] + len(self.murs['horizontaux']) + len(self.murs['verticaux']) != 20:
                raise QuoridorError("Nombre total de murs invalide (seul nombre autorisé: 20).")
        
            
   
    def __str__(self):
        pass
            
    def déplacer_jeton(self, joueur, position):
        '''Pour déplacer un jeton à une position'''
        
        #Les possibilités de mouvement
        graphe1 = networkx_utile.construire_graphe(
        [joueur['pos'] for joueur in self.joueurs], 
        self.murs['horizontaux'],
        self.murs['verticaux'])
        
        #Contraintes et déplacement du jeton
        if joueur in {1, 2}:
            if 1 <= position[0] <= 9 or 1 <= position[1] <= 9:
                if position in list(graphe1.successors(self.joueurs[joueur - 1]['pos'])):
                    self.joueurs[joueur - 1]['pos'] = position
                else:
                    raise QuoridorError("Tu ne peux pas aller là!")
            else:
                raise QuoridorError("Cette position n'existe pas!")
        else:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
        
        
    def état_partie(self):
        return {'joueurs': self.joueurs, 'murs': self.murs}


    def partie_terminée(self):
        if self.joueurs[0]['pos'][1] == 9:
            return f'Le gagnant est {self.joueurs[0]['nom']}'
        elif self.joueurs[1]['pos'][1] == 1:
            return f'Le gagnant est {self.joueurs[1]['nom']}'
        else:
            return False 


    def placer_mur(self, joueur, positionM, orientation):
        '''Pour placer un mur à une position'''
        
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
            if not 1 <= positionM[0] <= 8 or not 2 <= positionM[1] <= 9:
                raise QuoridorError('Tu ne peux pas placer un mur à cet endroit')
            
            #S'assurer que ce nouveau mur horizontal ne croise pas un autre mur
            if tuple(positionM[0] + 1, positionM[1] - 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(positionM[0] + 1, positionM[1]) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif positionM in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(positionM[0] - 1, positionM[1]) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')    
            else:
                self.murs['horizontaux'].append(positionM)
                
                
        #Placement d'un mur vertical    
        elif orientation == 'vertical':
            #S'assurer que le mur peut être placé d'après les dimensions du board
            if not 2 <= positionM[0] <= 9 or not 1 <= positionM[1] <= 8:
                raise QuoridorError('Tu ne peux pas placer un mur à cet endroit')
            
            #S'assurer que ce nouveau mur vertical ne croise pas un autre mur
            if tuple(positionM[0] - 1, positionM[1] + 1) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(positionM[0], positionM[1] - 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif positionM in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(positionM[0], positionM[1] + 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            else:
                self.murs['verticaux'].append(positionM)
                
                