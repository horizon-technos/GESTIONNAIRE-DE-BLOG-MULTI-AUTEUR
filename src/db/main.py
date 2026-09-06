from orm_ver_alt.utilitaires import Foreign_key
from orm_ver_alt.types_donnees import Colonne, Table
from orm_ver_alt.connecteur import DriverSGBD

class Student(Table):
  nom:str
  age:int
  note:float


class Utilisateur(Table):
    id: int
    nom: str
    hashpass: str
    role: str
    url_photo_profil: str
    created_at= Colonne('TIMESTAMP')
    refresh_token: str
    
class USer(Table):
  user_nom:str
  user_age:int
  user_note:float


class Eleve(Table):
  echec:bool
  id=Colonne("INT",primary=True)
  auteur_id=Colonne('BIGINT',foreign_key=Foreign_key(table='poste',attribut='id'))

e=Eleve('MySQL')

u=Student('MySQL')
u3=USer()
u2=USer("SQLite")
# u.recuperer_colonne()
# u2.recuperer_colonne()


print(u._dbtype)
print(u2._dbtype)
#print(Table._dbtype)
print(u.name())
print(u2.name())

print(u3.correspondance_sql())
print(u2.correspondance_sql())
print(u.correspondance_sql())

print(u2._dbtype)
print(u._dbtype)
#u2.create_table()
#u.create_table()

#print(e.recuperer_colonne())
print(e.create_table())


# initialisation du driver sgbd
driver_sgbd = DriverSGBD(dialecte='POSTGRES')
driver_sgbd.connexionSGBD(user="loic",password='loic',database="data_base",host='localhost')

requeteSQL = USer('POSTGRES').create_table()

print(driver_sgbd.executer_sql(requeteSQL))
driver_sgbd.deconnexionSGBD()

