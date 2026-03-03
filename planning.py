from connexion import Database
from datetime import datetime

class Planning:
    def __init__(self):
        self.db = Database()
    
    def vue_globale(self, date):
        requete = """
        SELECT c.heure_debut, c.heure_fin, 
               COALESCE(g.nom, '[LIBRE]') as groupe
        FROM creneau c
        LEFT JOIN reservation r ON c.id = r.id_creneau AND r.date = %s
        LEFT JOIN groupe g ON r.id_groupe = g.id
        ORDER BY c.heure_debut
        """
        return self.db.recuperer_tous(requete, (date,))
    
    def vue_disponibilites(self, date):
        requete = """
        SELECT c.* FROM creneau c
        WHERE c.id NOT IN (
            SELECT id_creneau FROM reservation WHERE date = %s
        )
        ORDER BY c.heure_debut
        """
        return self.db.recuperer_tous(requete, (date,))
    
    def reserver(self, id_groupe, id_creneau, date):
        try:
            date_reservation = datetime.strptime(date, "%Y-%m-%d").date()
            if date_reservation < datetime.now().date():
                return False, "Vous ne pouvez pas réserver à une date passée."
        except ValueError:
            return False, "Format de date invalide. Utilisez YYYY-MM-DD."

        infos_creneau = self.db.recuperer_un("SELECT heure_debut, heure_fin FROM creneau WHERE id = %s", (id_creneau,))
        if not infos_creneau:
            return False, "Erreur : ID de créneau inexistant."

        requete_conflit = """
            SELECT r.id FROM reservation r
            JOIN creneau c ON r.id_creneau = c.id
            WHERE r.date = %s
            AND c.heure_debut < %s AND c.heure_fin > %s
        """
        conflit = self.db.recuperer_un(requete_conflit, (date, infos_creneau['heure_fin'], infos_creneau['heure_debut']))
        
        if conflit:
            return False, "Impossible : Une réservation existante."
        
        try:
            self.db.executer_maj(
                "INSERT INTO reservation (id_groupe, id_creneau, date) VALUES (%s, %s, %s)",
                (id_groupe, id_creneau, date)
            )
            return True, "Réservation effectuée"
        except Exception:
            return False, "Erreur : Impossible de réserver. Vérifiez que les IDs du groupe et du créneau existent."
    
    def recuperer_reservations_pour_date(self, date):
        requete = """
        SELECT r.id, c.heure_debut, c.heure_fin, g.nom, g.responsable
        FROM reservation r
        JOIN creneau c ON r.id_creneau = c.id
        JOIN groupe g ON r.id_groupe = g.id
        WHERE r.date = %s
        ORDER BY c.heure_debut
        """
        return self.db.recuperer_tous(requete, (date,))

    def annuler(self, id_reservation):
        verif = self.db.recuperer_un(
            "SELECT id FROM reservation WHERE id = %s", (id_reservation,)
        )
        if not verif:
            return False, "Aucune réservation trouvée avec cet ID."
        
        self.db.executer_maj(
            "DELETE FROM reservation WHERE id = %s", (id_reservation,)
        )
        return True, "Réservation annulée avec succès."

    def ajouter_groupe(self, nom, responsable, motif):
        if not nom or not responsable or not motif:
            return False, "Tous les champs sont obligatoires."
        try:
            self.db.executer_maj(
                "INSERT INTO groupe (nom, responsable, motif) VALUES (%s, %s, %s)",
                (nom, responsable, motif)
            )
            return True, "Groupe ajouté avec succès."
        except Exception:
            return False, "Erreur : le nom existe peut-être déjà."

    def ajouter_creneau(self, heure_debut, heure_fin):
        try:
            self.db.executer_maj(
                "INSERT INTO creneau (heure_debut, heure_fin) VALUES (%s, %s)",
                (heure_debut, heure_fin)
            )
            return True, "Créneau ajouté avec succès."
        except Exception:
            return False, "Erreur : Le créneau existe déjà."

    def recuperer_groupes(self):
        return self.db.recuperer_tous("SELECT * FROM groupe ORDER BY nom")
    
    def recuperer_creneaux(self):
        return self.db.recuperer_tous("SELECT * FROM creneau ORDER BY heure_debut")