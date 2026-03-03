class Reservation:
    def __init__(self, id, id_groupe, id_creneau, date):
        self._id = id
        self._id_groupe = id_groupe
        self._id_creneau = id_creneau
        self._date = date
    
    @property
    def id(self): 
        return self._id
    
    @property
    def id_groupe(self): 
        return self._id_groupe
    
    @property
    def id_creneau(self): 
        return self._id_creneau
    
    @property
    def date(self): 
        return self._date