'''On fait nos tests ici'''
position = (4, 3)
A = {'horizontaux': [(4, 5), (5, 6)], 'verticaux': [(4, 3), (7, 6)]}


if position not in A['horizontaux'] + A['verticaux']:
    print(position)
else:
    raise ValueError('Il y a déjà un mur à cet endroit')
