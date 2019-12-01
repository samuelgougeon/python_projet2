
positionM = (4, 3)
A = {'horizontaux': [(4, 5), (5, 6)], 'verticaux': [(4, 3), (7, 6)]}


if positionM not in (A['horizontaux'] + A['verticaux']):
    print(positionM)
else:
    raise ValueError('Il y a déjà un mur à cet endroit')
