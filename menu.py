from authentification import Authentification
from planning import Planning
from datetime import datetime

class Menu:
    def __init__(self):
        self.auth = Authentification()
        self.planning = Planning()
    
    def afficher_menu_principal(self):
        print("\n=== ROOM MASTER ===")
        print("1. Se connecter")
        print("2. Quitter")
    
    def afficher_menu_admin(self):
        print("\n=== MENU ADMIN ===")
        print("1. Voir planning journalier (global)")
        print("2. Voir disponibilités")
        print("3. Réserver un créneau")
        print("4. Exporter planning CSV (bonus)")
        print("5. Annuler une réservation")
        print("6. Ajouter un groupe")
        print("7. Ajouter un créneau")
        print("8. Déconnexion")
    
    def afficher_planning_global(self):
        date = input("Date (YYYY-MM-DD): ")
        creneaux = self.planning.vue_globale(date)
        
        print(f"\n--- PLANNING DU {date} ---")
        for c in creneaux:
            print(f"{c['heure_debut']} - {c['heure_fin']} : {c['groupe']}")
    
    def afficher_disponibilites(self):
        date = input("Date (YYYY-MM-DD): ")
        dispos = self.planning.vue_disponibilites(date)
        
        print(f"\n--- CRENEAUX LIBRES LE {date} ---")
        for d in dispos:
            print(f"{d['id']}. {d['heure_debut']} - {d['heure_fin']}")
    
    def reserver_creneau(self):
        groupes = self.planning.recuperer_groupes()
        print("\n--- GROUPES ---")
        for g in groupes:
            print(f"{g['id']}. {g['nom']} ({g['responsable']}) - {g['motif']}")
        
        try:
            id_groupe = int(input("\nID du groupe: "))
        except ValueError:
            print("Erreur : L'ID du groupe doit être un nombre entier.")
            return
        
        creneaux = self.planning.recuperer_creneaux()
        print("\n--- CRENEAUX ---")
        for c in creneaux:
            print(f"{c['id']}. {c['heure_debut']} - {c['heure_fin']}")
        
        try:
            id_creneau = int(input("ID du créneau: "))
        except ValueError:
            print("Erreur : L'ID du créneau doit être un nombre entier.")
            return
            
        date = input("Date (YYYY-MM-DD): ")
        
        succes, message = self.planning.reserver(id_groupe, id_creneau, date)
        print(message)

    def annuler_reservation(self):
        date = input("Date de la réservation à annuler (YYYY-MM-DD): ")
        reservations = self.planning.recuperer_reservations_pour_date(date)

        if not reservations:
            print(f"Aucune réservation trouvée pour le {date}.")
            return

        print(f"\n--- RESERVATIONS POUR LE {date} ---")
        for r in reservations:
            print(f"ID: {r['id']} | {r['heure_debut']}-{r['heure_fin']} | Groupe: {r['nom']} ({r['responsable']})")

        try:
            id_reservation = int(input("\nEntrez l'ID de la réservation à annuler: "))
            succes, message = self.planning.annuler(id_reservation)
            print(message)
        except ValueError:
            print("ID invalide. Veuillez entrer un nombre.")

    def ajouter_nouveau_groupe(self):
        print("\n--- Ajout d'un nouveau groupe ---")
        nom = input("Nom du groupe: ").strip()
        responsable = input("Nom du responsable: ").strip()
        motif = input("Motif de la réservation (ex: Réunion, Cours...): ").strip()
        
        succes, message = self.planning.ajouter_groupe(nom, responsable, motif)
        print(message)

    def ajouter_nouveau_creneau(self):
        print("\n--- Ajout d'un nouveau créneau ---")
        heure_debut = input("Heure de début (HH:MM): ").strip()
        heure_fin = input("Heure de fin (HH:MM): ").strip()

        try:
            heure_debut_obj = datetime.strptime(heure_debut, '%H:%M')
            heure_fin_obj = datetime.strptime(heure_fin, '%H:%M')

            if heure_fin_obj <= heure_debut_obj:
                print("Erreur: L'heure de fin doit être strictement après l'heure de début.")
                return
        except ValueError:
            print("Erreur: Format d'heure invalide. Utilisez HH:MM.")
            return

        succes, message = self.planning.ajouter_creneau(heure_debut, heure_fin)
        print(message)