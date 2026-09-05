from orm_ver_alt.utilitaires import Colonne
from typing import Literal

arbre={}



types_postgres={'INTEGER', 'BIGINT', 'SERIAL', 'BOOLEAN', 'TEXT', 'NUMERIC', 'TIMESTAMP'}
types_mysql= {'INT', 'BIGINT', 'FLOAT', 'DOUBLE', 'VARCHAR', 'DATE', 'DATETIME'}
types_sqlite={'INTEGER', 'REAL', 'TEXT', 'BLOB', 'NUMERIC', 'BOOLEAN', 'DATETIME'}


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

  # récupérer les colonnes de la classe fille puis les mets dans un dictionnaire
  @classmethod
  def recuperer_colonne(self) -> dict[str,str] :
    parametres=self.__annotations__
    colonne={}

    for cle,valeur in self.__dict__.items():
      if isinstance(valeur,Colonne):
        colonne[cle]=valeur

    for k,v in parametres.items():
      colonne[k]=v.__name__
    return colonne

  # permet de convertir les types python en type mysql
  @classmethod
  def type_mysql_correspondant(self,colonne:dict[str,str]):
    correspondance={}
    sql={
  "int":"INT",
  'float':"FLOAT",
  'str':'TEXT',
  'bool':"ENUM('True','False')",
  }
    
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

  # permet de convertir les types python en type postgres
  @classmethod
  def type_postgres_correspondant(self,colonne:dict[str,str]) -> dict[str,str]:
    correspondance={}
    sql={
      "int":"INTEGER",
      'float':"FLOAT",
      'str':'TEXT',
      'bool':'BOOLEAN',
      }
    
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
        elif value.primary==True and value.foreign_key!=None:
          correspondance[key]=f"{value.type} PRIMARY KEY"
          correspondance[f"FOREIGN KEY ({key})"]=f" REFERENCES {value.foreign_key.table}({value.foreign_key.attribut})"   
        elif value.primary==True:
          correspondance[key]=f"{value.type} PRIMARY KEY"
        elif value.foreign_key!=None:
          correspondance[key]=value.type
          correspondance[f"FOREIGN KEY ({key})"]=f" REFERENCES {value.foreign_key.table}({value.foreign_key.attribut})"  
       
      if value in sql.keys():
        correspondance[key]=sql.get(value)

    return correspondance

  # permet de convertir les types python en type sqlite
  def type_sqlite_correspondant(colonne:dict[str,str]):
    correspondance={}
    sql={
          "int":"INTEGER",
          'float':"REAL",
          'str':'TEXT',
          'bool':'BOOLEAN',      
          }
    for key,value in colonne.items():
      if value in sql.keys():
        correspondance[key]=sql.get(value)

    return correspondance

  # permet de spécifier quel type de correspondance sql à effectué sur les colonnes des tables selon le type de BD
  @classmethod
  def correspondance_sql(self) -> dict[str,str]:
    if self._dbtype=='MySQL':
      return self.type_mysql_correspondant(self.recuperer_colonne()) 
    elif self._dbtype=='POSTGRES':
      return self.type_postgres_correspondant(self.recuperer_colonne()) 
    elif self._dbtype=='SQLite':
      return self.type_sqlite_correspondant(self.recuperer_colonne()) 
    else:
      raise TypeError('TYPE DE BD INCORRECTE')

  #permet de créer la table peut importe le type de BD
  @classmethod
  def create_table(self):
    if self._dbtype=='MySQL':
      self.__create_mysql(self.correspondance_sql()) 
    elif self._dbtype=='POSTGRES':
      self.__create_postgres(self.correspondance_sql()) 
    elif self._dbtype=='SQLite':
      self.__create_sqlite(self.correspondance_sql()) 
    else:
      raise TypeError('TYPE DE BD INCORRECTE')  

  # génère la requête qui crée la table Postgresql
  @classmethod
  def __create_postgres(self,colonne:dict[str,str]):
    definitions=[]
    for key,value in colonne.items():
      definitions.append(f"{key} {value}")

    jointure=', '.join(definitions)
    print(f'CREATE TABLE IF NOT EXISTS {self.name()} ({jointure});')

  # génère la requête qui crée la table mysql
  @classmethod
  def __create_mysql(self,colonne:dict[str,str]):
    definitions=[]
    for key,value in colonne.items():
      definitions.append(f"{key} {value}")

    jointure=', '.join(definitions)
    print(f'CREATE TABLE {self.name()} ({jointure});')    

  # génère la requête qui crée la table sqlite
  @classmethod
  def __create_sqlite(self,colonne:dict[str,str]):
    definitions=[]
    for key,value in colonne.items():
      definitions.append(f"{key} {value}")

    jointure=', '.join(definitions)
    print(f'CREATE TABLE IF NOT EXISTS {self.name()} ({jointure});')
      

