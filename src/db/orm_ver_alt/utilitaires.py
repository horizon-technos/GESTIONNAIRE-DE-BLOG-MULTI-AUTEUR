from typing import Literal, get_args

types = Literal[
    # PostgreSQL
    'INTEGER',
    'BIGINT',
    'SERIAL',
    'BOOLEAN',
    'TEXT',
    'NUMERIC',
    'TIMESTAMP',

    # MySQL
    'INT',
    'FLOAT',
    'DOUBLE',
    'VARCHAR',
    'DATE',
    'DATETIME',

    # SQLite
    'REAL',
    'BLOB'
]

# classe pour spécifier l'option clé étrangère dans les atttributs des tables
class Foreign_key:
  def __init__(self,table:str,attribut:str):
    self.table=table
    self.attribut=attribut

# classe pour gérer les options en plus des attributs des tables tels que:
#                                                                   - les clés primaires
#                                                                   - les clés étrangères
#                                                                   - etc
#
class Colonne:
  def __init__(self,type_:types,foreign_key:Foreign_key=None,primary=False):

    if(type_ not in get_args(types)):
      raise ValueError(f"le type **{type_}** ne fait partie d'aucune entrée de type SQL")
    
    self.type=type_
    self.primary=primary
    self.foreign_key=foreign_key

  def __str__(self,):
    return f"nom:{self.type}\nclé primaire:{self.primary}\nclé étrangère:{self.foreign_key}"    
  