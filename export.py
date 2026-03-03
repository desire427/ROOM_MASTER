import csv
from connexion import Database
from datetime import datetime

def exporter_planning_csv():
    db = Database()
    
    date_export = input("Date à exporter : ").strip()
    
    query = """
    SELECT c.heure_debut, c.heure_fin, g.nom, g.motif, g.responsable
    FROM reservation r
    JOIN creneau c ON r.id_creneau = c.id
    JOIN groupe g ON r.id_groupe = g.id
    WHERE r.date = %s
    ORDER BY c.heure_debut
    """
    
    reservations = db.recuperer_tous(query, (date_export,))
    
    if not reservations:
        print(f"Aucune réservation trouvée pour le {date_export}.")
        return
    
    nom_fichier = f"planning_{date_export.replace('-', '')}.csv"
    
    with open(nom_fichier, 'w', newline='', encoding='utf-8') as f:
        ecrivain = csv.writer(f)
        ecrivain.writerow(['Heure début', 'Heure fin', 'Groupe', 'Motif', 'Responsable'])
        ecrivain.writerows([[r['heure_debut'], r['heure_fin'], r['nom'], r['motif'], r['responsable']] for r in reservations])
    
    print(f"Exporté dans {nom_fichier}")