class Creneau:
    def __init__(self, id, heure_debut, heure_fin):
        self._id = id
        self._heure_debut = heure_debut
        self._heure_fin = heure_fin
    
    @property
    def id(self): 
        return self._id
    
    @property
    def heure_debut(self): 
        return self._heure_debut
    
    @property
    def heure_fin(self): 
        return self._heure_fin