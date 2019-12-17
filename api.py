'''S'occupe des requêtes au serveur'''
import requests


URL_BASE = 'https://python.gel.ulaval.ca/quoridor/api/'


#fonction 4
def débuter_partie(idul):
    '''Demande au serveur le dictionnaire d'une nouvelle partie'''

    rep = requests.post(URL_BASE+'débuter/', data={'idul': idul})
    rep2 = rep.json()
    if rep.status_code == 200:
        if 'message' in rep2:
            raise RuntimeError(rep2['message'])
        else:
            return rep2['id'], rep2['état']
    else:
        raise ConnectionError(rep.status_code)

#fonction 5
def jouer_coup(id_partie, type_coup, position):
    '''Demande au serveur le dictionnaire après un coup joué'''

    rep = requests.post(
        URL_BASE+'jouer/',
        data={'id': id_partie, 'type': type_coup, 'pos': position}
    )
    rep2 = rep.json()
    if rep.status_code == 200:
        if 'gagnant' in rep2:
            raise StopIteration(rep2['gagnant'])
        elif 'message' in rep2:
            raise RuntimeError(rep2['message'])
        else:
            return rep2['état']
    else:
        raise ConnectionError(rep.status_code)
    
