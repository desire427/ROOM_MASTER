import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """Gère la connexion à la base de données."""
    def __init__(self):
        """Initialise la connexion à la base de données."""
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Erreur : Nom d'utilisateur ou mot de passe de la base de données incorrect.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Erreur : La base de données '{os.getenv('DB_NAME')}' n'existe pas.")
            else:
                print(f"Erreur de connexion à la base de données : {err}")
            exit(1)

    def recuperer_tous(self, requete, params=None):
        self.cursor.execute(requete, params or ())
        return self.cursor.fetchall()

    def recuperer_un(self, requete, params=None):
        self.cursor.execute(requete, params or ())
        return self.cursor.fetchone()

    def executer_maj(self, requete, params=None):
        self.cursor.execute(requete, params or ())
        self.conn.commit()
        return self.cursor.lastrowid

    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()