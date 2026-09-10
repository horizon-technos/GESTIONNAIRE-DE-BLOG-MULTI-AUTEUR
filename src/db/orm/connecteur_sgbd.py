import sqlite3
import psycopg2
import pymysql
from typing import Literal

DIALECTE = Literal['SQLITE','MYSQL','POSTGRES']

# Driver SGBD
class DriverSGBD:
    dialecte: DIALECTE
    est_connecte: bool = False
    connecteur: any
    curseur: any

    @classmethod
    def __init__(self, dialecte: DIALECTE):
        self.dialecte = dialecte

    @classmethod
    def connexionSGBD(self, host=None, db=None, password=None, utilisateur=None):
        match self.dialecte:
            case 'SQLITE':
                try:
                    self.connecteur = sqlite3.connect("../blog.db")
                    self.est_connecte = True
                    self.curseur = self.connecteur.cursor()
                except Exception as e:
                    raise FileNotFoundError("Fichier BD introuvable ou invalide.")
            case 'POSTGRES':
                try:
                    self.connecteur = psycopg2.connect(host=host,dbname=db,user=utilisateur,password=password)
                    self.est_connecte = True
                    self.curseur = self.connecteur.cursor()
                except Exception as e:
                    raise ConnectionError("Impossible de se connecter a la base de donnees:", e)
            case 'MYSQL':
                try:
                    self.connecteur = pymysql.connect(host=host,database=db,user=utilisateur,password=password)
                    self.est_connecte = True
                    self.curseur = self.connecteur.cursor()
                except Exception as e:
                    raise ConnectionError("Impossible de se connecter a la base de donnees:", e)
            case _:
                raise ValueError("Dialecte ",self.dialecte," non pris en charge.") 

    @classmethod
    def executerRequete(self, requetesql: str):
        if self.dialecte not in ['SQLITE','MYSQL','POSTGRES']:
            raise ValueError("Dialecte ",self.dialecte," non pris en charge.")
        else:
            self.curseur.execute(requetesql)
            try:
                self.connecteur.commit()
            except Exception as e:
                self.connecteur.rollback()
                raise RuntimeError("Echec de l'execution de la requete, donc rollback.")

    @classmethod
    def deconnecterSGBD(self):
        if self.dialecte in ['POSTGRES','MYSQL']:
            self.curseur.close()
        self.connecteur.close()
        self.est_connecte = False