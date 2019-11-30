'''Encadrer le jeu avec une classe'''

import networkx

class QuoridorError(Exception):
    '''Pour pouvoir utiliser toutes les méthodes de la classe 'Exception'
        sous le nom 'QuoridorError' '''

class Quoridor:
    '''Pour encadrer le jeu'''
    def __init__(self, joueurs, murs=None):

        #Erreurs à soulever
        if not isinstance(joueurs, iter):
            raise QuoridorError("Ton argument 'joueurs' n'est pas un itérable.")
        if len(joueurs) > 2:
            raise QuoridorError("On ne veut jouer qu'à deux joueurs.")
        
        #Si 'joueurs' est un itérable de strings
        elif isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.joueurs = [
                {'nom': joueurs[0], 'murs': 10, 'pos': (5, 1)},
                {'nom': joueurs[1], 'murs': 10, 'pos': (5, 9)},
            ]
            
        #Si 'joueurs' est un itérable de dictionnaires
        if isinstance(joueurs[0], dict) and isinstance(joueurs[1], dict):
            self.joueurs = joueurs
            for i in joueurs:
                if not 0 <= joueurs[i]['murs'] <= 10:
                    raise QuoridorError("Le nombre de murs à placer est entre 0 et 10.")
                if not 1 <= joueurs[i]['pos'][0] <= 9 or not 1 <= joueurs[i]['pos'][1] <= 9:
                    raise QuoridorError("La position que tu essaies d'entrer n'est pas valide!")
                
            
        #Si les murs existent
        if murs is not None: 
            if not isinstance(murs, dict):
                raise QuoridorError("Ton argument 'murs' n'est pas un dictionnaire.")
            
            self.murs = murs
            
            if self.joueurs[0]['murs'] + self.joueurs[1]['murs'] + len(self.murs['horizontaux']) + len(self.murs['verticaux']) != 20:
                raise QuoridorError("Nombre total de murs invalide (seul nombre autorisé: 20).")
                
            for i in enumerate(murs['horizontaux']):
                if not 1 <= i[1][0] <= 8 or not 2 <= i[1][1] <= 9:
                    raise QuoridorError("Position de mur invalide")
            for i in enumerate(murs['verticaux']):
                if not 2 <= i[1][0] <= 9 or not 1 <= i[1][1] <= 8:
                    raise QuoridorError("Position de mur invalide")
        
        #Si les murs n'existent pas encore
        else:
            self.murs = {'horizontaux': [], 'verticaux': []}
            
   
    def __str__(self):
        pass
            
    def déplacer_jeton(self, joueur, position):
        '''Pour déplacer un jeton à une position'''
        for i in enumerate(position):
            if not 1 <= i[1] <= 9:
                raise QuoridorError("La position n'existe pas sur le plateau de jeu")
        if not joueur in {1, 2}:
            raise QuoridorError("Le numéro du joueur n'est pas 1 ou 2.")
        else:
            self.joueurs[joueur - 1]['pos'] = position
            
        
        
            
        '''raises QuoridorError: si la position est invalide pour l'état actuel du jeu'''
        #Somehow checker avec le networkx si la position demandée ici correspond aux possibilités actuelles de mouvement du joueur.    
    
    
    def état_partie(self):
        
        
        
        dico = {
                    'joueurs': [
                        {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                        {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
                    ],
                    'murs': {
                        'horizontaux': [...],
                        'verticaux': [...],
                    } 
                }       
        return dico
        
        
    