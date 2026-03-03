import bcrypt
from connexion import Database
from utilisateur import Utilisateur

class Authentification:
    def __init__(self):
        self.db = Database()
        self.utilisateur_connecte = None
    
    def connecter(self, login, mot_de_passe):
        requete = "SELECT * FROM utilisateur WHERE login = %s"
        donnees_utilisateur = self.db.recuperer_un(requete, (login,))
        
        if donnees_utilisateur:
            hash_stocke = donnees_utilisateur['mot_de_passe'].encode('utf-8')
            if bcrypt.checkpw(mot_de_passe.encode('utf-8'), hash_stocke):
                self.utilisateur_connecte = Utilisateur(
                    donnees_utilisateur['id'],
                    donnees_utilisateur['login'],
                    donnees_utilisateur['mot_de_passe']
                )
                return True
        return False
    
    def est_connecte(self):
        return self.utilisateur_connecte is not None
    
    def deconnecter(self):
        self.utilisateur_connecte = None