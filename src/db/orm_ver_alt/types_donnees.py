from orm_ver_alt.utilitaires import Colonne
from typing import Literal

arbre={}

types_postgres={'INTEGER', 'BIGINT', 'SERIAL', 'BOOLEAN', 'TEXT', 'NUMERIC', 'TIMESTAMP'}
types_mysql= {'INT', 'BIGINT', 'FLOAT', 'DOUBLE', 'VARCHAR', 'DATE', 'DATETIME'}
types_sqlite={'INTEGER', 'REAL', 'TEXT', 'BLOB', 'NUMERIC', 'BOOLEAN', 'DATETIME'}

dictionnaire_postgresql_correspondant={
      "int":"INTEGER",
      'float':"FLOAT",
      'str':'TEXT',
      'bool':'BOOLEAN',
      }

dictionnaire_mysql_correspondant={
  "int":"INT",
  'float':"FLOAT",
  'str':'TEXT',
  'bool':"ENUM('True','False')",
  }

dictionnaire_sqlite_correspondant={
          "int":"INTEGER",
          'float':"REAL",
          'str':'TEXT',
          'bool':'BOOLEAN',      
          }

# permet de spécifier les types
db_type=Literal['MySQL','POSTGRES','SQLite']

class Table:
  _dbtype:db_type

  # permet de définir le type de BD suivant ['MySQL','POSTGRES','SQLite'] par défaut c'est 'POSTGRES'
  @classmethod
  def __init__(self,typedb:db_type='POSTGRES'):
    self._dbtype=typedb

  # récupère le nom de la classe fille ou la table
  @classmethod
  def name(self):
    return self.__name__.lower()

  # récupérer les colonnes de la classe enfant puis les mets dans un dictionnaire
  @classmethod
  def recuperer_colonne(self) -> dict[str,str] :
    parametres=self.__annotations__
    colonne={}

    for k,v in parametres.items():
      colonne[k]=v.__name__

    for cle,valeur in self.__dict__.items():
      if isinstance(valeur,Colonne):
        colonne[cle]=valeur

    return colonne

  # permet de convertir les types python en type SQL 
  @classmethod
  def type_sql_correspondant(self,colonne:dict[str,str],sql:dict) -> dict[str,str]:
    correspondance={}
    
    for key,value in colonne.items():
      if isinstance(value,Colonne):

        if self._dbtype=='MySQL':
          if value.type not in types_mysql:
            raise TypeError(f"Le type **{value.type}** ne fait pas partie de MySQL")
        elif self._dbtype=='POSTGRES':
          if value.type not in types_postgres:
            raise TypeError(f"Le type **{value.type}** ne fait pas partie de POSTGRES") 
        elif self._dbtype=='SQLite':
          if value.type not in types_sqlite:
            raise TypeError(f"Le type **{value.type}** ne fait pas partie de SQLite")

        if not value.primary and not value.foreign_key:
          correspondance[key]=value.type
        elif value.primary==True:
          correspondance[key]=f"{value.type} PRIMARY KEY"
        elif value.foreign_key!=None:
          correspondance[key]=value.type
          correspondance[f"FOREIGN KEY ({key})"]=f" REFERENCES {value.foreign_key.table}({value.foreign_key.attribut})"  

      if value in sql.keys():
        correspondance[key]=sql.get(value)
    return correspondance
 
  # permet de spécifier quel type de correspondance sql à effectué sur les colonnes des tables selon le type de BD
  @classmethod
  def correspondance_sql(self) -> dict[str,str]:
    if self._dbtype=='MySQL':
      return self.type_sql_correspondant(self.recuperer_colonne(),dictionnaire_mysql_correspondant) 
    elif self._dbtype=='POSTGRES':
      return self.type_sql_correspondant(self.recuperer_colonne(),dictionnaire_postgresql_correspondant) 
    elif self._dbtype=='SQLite':
      return self.type_sql_correspondant(self.recuperer_colonne(),dictionnaire_sqlite_correspondant) 
    else:
      raise TypeError('TYPE DE BD INCORRECTE')

  # appelle juste la fonction pour créer la table SQL
  @classmethod
  def create_table(self):
    return self.__creation_de_la_commande_create_table(self.correspondance_sql()) 

  # génère la requête qui crée la table SQL
  @classmethod
  def __creation_de_la_commande_create_table(self,colonne:dict[str,str]):
    definitions=[]
    arbre[self.name()]=set(self.recuperer_colonne().keys())
#    print(set().union(*arbre.values()))
    for key,value in colonne.items():
      definitions.append(f"{key} {value}")

    jointure=', '.join(definitions)
    if self._dbtype=='POSTGRES':
      return (f'CREATE TABLE "{self.name()}" ({jointure});')
    return (f'CREATE TABLE {self.name()} ({jointure});')
