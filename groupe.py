class Groupe:
    def __init__(self, id, nom, responsable, motif):
        self._id = id
        self._nom = nom
        self._responsable = responsable
        self._motif = motif
    
    @property
    def id(self): return self._id
    
    @property
    def nom(self): return self._nom
    
    @property
    def responsable(self): return self._responsable
    
    @property
    def motif(self): return self._motif