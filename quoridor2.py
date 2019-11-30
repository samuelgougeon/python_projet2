'''Encadrer le jeu avec une classe'''

import networkx as nx
import networkx_utile as nxu

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
        self.graphe = nxu.construire_graphe(
            [joueur['pos'] for joueur in self.joueurs],
            self.murs['horizontaux'],
            self.murs['verticaux']
            )
            
        #S'assurer que les joueurs ne sont pas enfermés par des murs
        if nx.has_path(self.graphe, self.joueurs[0]['pos'], 'B1') is False:
            raise QuoridorError("Le joueur 1 est enfermé! Shame on you.")
        elif nx.has_path(self.graphe, self.joueurs[1]['pos'], 'B2') is False:
            raise QuoridorError("Le joueur 2 est enfermé! Shame on you.")
            
            
    def __str__(self):
        '''Pour afficher le board'''
            
    def déplacer_jeton(self, joueur, position):
        '''Pour déplacer un jeton à une position'''
        
        #Contraintes et déplacement du jeton
        if joueur in {1, 2}:
            if 1 <= position[0] <= 9 or 1 <= position[1] <= 9:
                if position in list(self.graphe.successors(self.joueurs[joueur - 1]['pos'])):
                    self.joueurs[joueur - 1]['pos'] = position
                else:
                    raise QuoridorError("Tu ne peux pas aller là!")
            else:
                raise QuoridorError("Cette position n'existe pas!")
        else:
            raise QuoridorError("Le numéro du joueur doit être 1 ou 2.")
        
        
    def état_partie(self):
        '''Pour produire le dictionnaire d'état de jeu'''
        return {'joueurs': self.joueurs, 'murs': self.murs}

    def jouer_coup(self, joueur):
        '''Pour jouer le meilleur coup d'un joueur
        (manoeuvre automatisée pas très smat, sans murs)'''
        if joueur in {1, 2}:
            chemin = nx.shortest_path(self.graphe, self.joueurs[joueur - 1]['pos'], f'B{joueur}')
            if self.partie_terminée() is False:
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
            if tuple(position[0] + 1, position[1] - 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(position[0] + 1, position[1]) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif position in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(position[0] - 1, position[1]) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')    
            else:
                self.murs['horizontaux'].append(position)
                
                
        #Placement d'un mur vertical    
        elif orientation == 'vertical':
            #S'assurer que le mur peut être placé d'après les dimensions du board
            if not 2 <= position[0] <= 9 or not 1 <= position[1] <= 8:
                raise QuoridorError('Tu ne peux pas placer un mur à cet endroit')
            
            #S'assurer que ce nouveau mur vertical ne croise pas un autre mur
            if tuple(position[0] - 1, position[1] + 1) in self.murs['horizontaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(position[0], position[1] - 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif position in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            elif tuple(position[0], position[1] + 1) in self.murs['verticaux']:
                raise QuoridorError('Un mur déjà placé bloque cet endroit')
            else:
                self.murs['verticaux'].append(position)
