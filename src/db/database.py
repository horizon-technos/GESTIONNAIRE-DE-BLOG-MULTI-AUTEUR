# connecteur bd POSTGRESQL
import psycopg2
import inspect
from typing import get_type_hints, Any


# mappage des types de donnees
TYPE_DONNEES = {
    int: "INTEGER",
    str: "TEXT",
    float: "REAL",
    bool: "INTEGER",
    bytes: "BLOB"
}

# creation de la table de base
class Modele:
    """
    classe de base pour tous les modeles qui analyse les annotations de types pour creer la table 
    et fournit les methodes CRUD securisees.
    """
    __nomtable__ = None
    _connexion = None

    @classmethod
    def _get_connexion(connecteur):
        if connecteur._connexion is None:
            raise RuntimeError("Aucune connexion definie vers la bd.")
        return connecteur._connexion
    
    @classmethod
    def _set_connexion(connecteur, objetConnexion):
        connecteur._connexion = objetConnexion

    @classmethod
    def _get_nomtable(connecteur):
        return connecteur.__nomtable__ or connecteur.__nomtable__.lower()
    
    @classmethod
    def _get_colones(connecteur):
        hints = get_type_hints(connecteur)
        parametres_initialisation = inspect.signature(connecteur.__init__).parameters
        print(hints)
        print(parametres_initialisation)
        parametres_ordonnes = [p for p in parametres_initialisation if p != 'self']
        print(parametres_ordonnes)

        colones = {}
        for param in parametres_ordonnes:
            if param.startswith('_'):
                continue

            typ = hints.get(param, str)
            colones[param] = typ
        return colones

    @classmethod
    def creer_table(connecteur):
        colones = connecteur._get_colones()
        if not colones:
            raise ValueError(f"Aucune colone trouvee pour la classe {connecteur.__name__}")
        
        colones_definies = []
        for nom, typ in colones.items():
            type_sql = TYPE_DONNEES.get(typ, "TEXT")
            if nom == "id":
                colones_definies.append(f"{nom} {type_sql} PRIMARY KEY AUTOINCREMENT")
            else:
                colones_definies.append(f"{nom} {type_sql}")
        commande = f"CREATE TABLE IF NOT EXISTS {connecteur._get_nomtable()} (\n " + ",\n ".join(colones_definies) + "\n);"

        connexion = connecteur._get_connexion()
        curseur = connexion.cursor()
        curseur.execute(commande)
        connexion.commit()
        print(f"Table {connecteur._get_nomtable()} cree ou deja existante.")

    @classmethod
    def inserer(connecteur, **kwargs):
        colones = connecteur._get_colones()

        donnees = {k: v for k, v in kwargs.items() if k in colones}
        if not donnees:
            raise ValueError("Aucune donnees valide a inserer")
        
        parsing_donnees = ", ".join(["?"] * len(donnees))
        noms_colones = ", ".join(donnees.keys())
        sql = f"INSERT INTO {connecteur._get_nomtable()} ({noms_colones}) VALUES ({parsing_donnees})"

        connexion = connecteur._get_connexion()
        curseur = connexion.cursor()
        curseur.execute(sql, list(donnees.values()))
        connexion.commit()
        return curseur.lastrowid

    @classmethod
    def get(connecteur, **conditions):
        if not conditions:
            raise ValueError("Il faut au moins une condition.")
        where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        sql = f"SELECT * FROM {connecteur._get_nomtable()} WHERE {where_clause}"
        conn = connecteur._get_connexion()
        cursor = conn.cursor()
        cursor.execute(sql, list(conditions.values()))
        row = cursor.fetchone()
        if row:
            # Récupérer les noms de colonnes
            col_names = [description[0] for description in cursor.description]
            return dict(zip(col_names, row))
        return None

    @classmethod
    def get_tout(connecteur, **conditions):
        connexion = connecteur._get_connexion()
        curseur = connexion.cursor()
        if conditions:
            where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
            sql = f"SELECT * FROM {connecteur._get_nomtable()} WHERE {where_clause}"
            curseur.execute(sql, list(conditions.values()))
        else:
            sql = f"SELECT * FROM {connecteur._get_nomtable()}"
            curseur.execute(sql)
        rows = curseur.fetchall()
        col_names = [description[0] for description in curseur.description]
        return [dict(zip(col_names, row)) for row in rows]

    @classmethod
    def update(connecteur, nouvelles_valeurs, **conditions):
        if not conditions:
            raise ValueError("Il faut au moins une condition pour la mise a jour")
        clause_update = ", ".join([f"{k} = ?" for k in nouvelles_valeurs.keys()])
        clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        sql = f"UPDATE {connecteur._get_nomtable()} SET {clause_update} WHERE {clause}"
        params = list(nouvelles_valeurs.values()) + list(conditions.values())
        connexion = connecteur._get_connection()
        curseur = connexion.cursor()
        curseur.execute(sql, params)
        connexion.commit()
        return curseur.rowcount

    @classmethod
    def delete(connecteur, **conditions):
        if not conditions:
            raise ValueError("Il faut au moins une condition pour la suppression")
        clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        sql = f"DELETE FROM {connecteur._get_nomtable()} WHERE {clause}"
        connexion = connecteur._get_connexion()
        curseur = connexion.cursor()
        curseur.execute(sql, list(conditions.values()))
        connexion.commit()
        return curseur.rowcount




# connecteur bd
conn = psycopg2.connect(
   host='localhost',
    database='blog_bd',
    user='admin',
    password='admin2026' 
)

