from menu import Menu
from export import exporter_planning_csv

def main():
    menu = Menu()
    
    while True:
        if not menu.auth.est_connecte():
            menu.afficher_menu_principal()
            choix = input("Choix: ")
            
            if choix == "1":
                login = input("Login: ").strip()
                mdp = input("Mot de passe: ").strip()
                if menu.auth.connecter(login, mdp):
                    print("Connexion réussie")
                else:
                    print("Login/mot de passe incorrect")
            elif choix == "2":
                print("Au revoir")
                break
        else:
            menu.afficher_menu_admin()
            choix = input("Choix: ")
            
            if choix == "1":
                menu.afficher_planning_global()
            elif choix == "2":
                menu.afficher_disponibilites()
            elif choix == "3":
                menu.reserver_creneau()
            elif choix == "4":
                exporter_planning_csv()
            elif choix == "5":
                menu.annuler_reservation()
            elif choix == "6":
                menu.ajouter_nouveau_groupe()
            elif choix == "7":
                menu.ajouter_nouveau_creneau()
            elif choix == "8":
                menu.auth.deconnecter()
                print("Déconnecté")


main()