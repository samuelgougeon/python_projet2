'''Vrm vrm pour faire des tests'''
import quoridor


test = quoridor.Quoridor([
        {"nom": "idul", "murs": 7, "pos": (6, 4)},
        {"nom": "automate", "murs": 2, "pos": (5, 2)}
    ], {
        "horizontaux": [(4, 4), (2, 6), (3, 9), (5, 8), (7, 8)],
        "verticaux": [(6, 2), (2, 5), (7, 5), (7, 2), (7, 7), (4, 7)]
    })

test.placer_mur(2, (8, 9), 'horizontal')
print(test.__str__())