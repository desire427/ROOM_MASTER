import bcrypt
from connexion import Database
import getpass

def create_admin():
    db = Database()
    
    login = input("Entrez le login: ").strip()
    mot_de_passe = getpass.getpass("Entrez le mot de passe: ").strip()
    
    if not login or not mot_de_passe:
        print("Le login et le mot de passe ne peuvent pas être vides.")
        return

    utilisateur_existe = db.recuperer_un("SELECT id FROM utilisateur WHERE login = %s", (login,))
    if utilisateur_existe:
        print(f"L'utilisateur '{login}' existe déjà.")
        return

    mot_de_passe_hache = bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db.executer_maj(
        "INSERT INTO utilisateur (login, mot_de_passe) VALUES (%s, %s)",
        (login, mot_de_passe_hache)
    )
    print(f"Utilisateur '{login}' créé avec succès.")


print("--- Création de l'Administrateur ---")
create_admin()