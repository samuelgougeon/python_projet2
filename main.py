'''Pour exécuter le jeu'''
import argparse


#Fonction du jeu
def analyser_commande():
    '''Pour gérer les arguments de la commande dans le terminal'''
    parser = argparse.ArgumentParser(description='Jeu Quoridor - phase 3')
    parser.add_argument('idul', help='IDUL du joueur')
    parser.add_argument('-a', '--automatique', help='Activer le mode automatique.', action='store_true')
    parser.add_argument('-x', '--graphique', help='Activer le mode graphique.', action='store_true')
    args = parser.parse_args()
    return args

analyser_commande()
