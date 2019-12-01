'''Pour utiliser la fonction construire_graphe si gentiment fournie'''
import networkx as nx
import matplotlib.pyplot as plt


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
                # ajouter les liens en diagonal
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

dico = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 6]},
        {"nom": "automate", "murs": 3, "pos": [5, 7]}
    ],
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
    }
}



graphe1 = construire_graphe(
    [joueur['pos'] for joueur in dico['joueurs']], 
    dico['murs']['horizontaux'],
    dico['murs']['verticaux'])



positions = {'B1': (5, 10), 'B2': (5, 0)}
colors = {
    'B1': 'red', 'B2': 'green', 
    tuple(dico['joueurs'][0]['pos']): 'red', 
    tuple(dico['joueurs'][1]['pos']): 'green',
}
sizes = {
    tuple(dico['joueurs'][0]['pos']): 300, 
    tuple(dico['joueurs'][1]['pos']): 300
}

nx.draw(
    graphe, 
    pos={node: positions.get(node, node) for node in graphe},
    node_size=[sizes.get(node, 100) for node in graphe],
    node_color=[colors.get(node, 'gray') for node in graphe],
)
plt.show() 
    