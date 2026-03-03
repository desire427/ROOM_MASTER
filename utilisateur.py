class Utilisateur:
    def __init__(self, id, login, mot_de_passe):
        self._id = id
        self._login = login
        self._mot_de_passe = mot_de_passe
    
    @property
    def id(self): 
        return self._id
    
    @property
    def login(self):  
        return self._login
    
    @property
    def mot_de_passe(self): 
        return self._mot_de_passe