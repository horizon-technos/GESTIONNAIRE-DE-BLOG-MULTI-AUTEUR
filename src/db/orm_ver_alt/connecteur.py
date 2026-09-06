# connecteur SGBD
import sqlite3
from types_donnees import db_type

class DriverSGBD:
    dialecte: db_type
    est_connecte: bool = False
    connecteur: any
    curseur: any

    @classmethod
    def __init__(self,dialecte: db_type):
        self.dialecte = dialecte
        if dialecte == 'SQLite':
            try:
                self.connecteur = sqlite3.connect('db_blog.db')
                self.curseur = self.connecteur.cursor()
            except:
                raise FileNotFoundError("Fichier BD introuvable.")

    @classmethod
    def connexionSGBD(self):
        if self.dialecte == "SQLite":
            pass
    
    @classmethod
    def executer_sql(self,requete_sql: str) -> dict[str. str]:
        reponse = {}
        if self.dialecte == "SQLite":
            self.curseur.execute(requete_sql)
            reponse['reponse_sql']=self.curseur.fetchall()
            return reponse

    @classmethod
    def deconnexionSGBD(self):
        if self.dialecte == "SQLite":
            self.connecteur.close()