# connecteur SGBD
import sqlite3
import psycopg2
from orm_ver_alt.types_donnees import db_type

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
            except Exception as e:
                raise FileNotFoundError("Fichier BD introuvable: ",e)
           

    @classmethod
    def connexionSGBD(self,host=None,database=None,password=None,user=None):
        if self.dialecte == "SQLite":
            pass
        elif self.dialecte =="POSTGRES":
            try:
                self.connecteur=psycopg2.connect(dbname=database, user=user, password=password,host=host)
                self.curseur=self.connecteur.cursor()
                # self.curseur.execute(f"CREATE USER {user} WITH PASSWORD '{password}';")
                # self.curseur.execute(f"CREATE DATABASE {database} OWNER {user};")
                # self.curseur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {database} TO {user};")
                # self.connecteur.commit()

            except Exception as e:
                raise ConnectionError('Connexion à la Base de donnée POSTGRES impossible: ',e)
    
    @classmethod
    def executer_sql(self,requete_sql: str) :
        reponse = {}
        if self.dialecte == "SQLite":
            self.curseur.execute(requete_sql)
            reponse['reponse_sql']=self.curseur.fetchall()
            return reponse
        elif self.dialecte=="POSTGRES":
            self.curseur.execute(requete_sql)
            self.connecteur.commit()
            reponse['reponse_sql']=self.curseur.lastrowid
            return reponse
        

    @classmethod
    def deconnexionSGBD(self):
        if self.dialecte == "SQLite":
            self.connecteur.close()
        elif self.dialecte == "POSTGRES":
            self.curseur.close()
            self.connecteur.close()    