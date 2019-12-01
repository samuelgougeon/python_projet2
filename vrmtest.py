'''On fait nos tests ici'''
import quoridor2



def jouer_jeu(joueur1, robot):
    partie = quoridor2.Quoridor((f'{joueur1}', f'{robot}'))
    partie.__str__()
    i = True
    while i:
        type_coup = input('Quel est ton type de coup?')
        if type_coup == 'D':
            position = tuple(input('Vers quelle position veux-tu aller?'))
            pos = ((int(position[1]), int(position[4])))
            partie.déplacer_jeton(1, pos)
            partie.jouer_coup(2)
        elif type_coup == 'MH':
            position = tuple(input('À quelle position veux-tu placer un mur horizontal?'))
            pos = ((int(position[1]), int(position[4])))
            partie.placer_mur(1, pos, 'horizontal')
            partie.jouer_coup(2)
        elif type_coup == 'MV':
            position = tuple(input('À quelle position veux-tu placer un mur vertical?'))
            pos = ((int(position[1]), int(position[4])))
            partie.placer_mur(1, pos, 'vertical')
            partie.jouer_coup(2)
        partie.__str__()
        partie.partie_terminée()
jouer_jeu('Samu-kun', 'Baka-kun')
