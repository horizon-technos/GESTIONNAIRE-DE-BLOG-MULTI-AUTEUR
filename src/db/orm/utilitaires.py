# fonctions utilitaires de l'ORM 
# ROLE    : Moteur central de l'ORM.
#           - Classe Modele pour héritage.
#           - Extraction du schéma des classes.
#           - Comparaison avec la base réelle.
#           - Exécution des migrations (ALTER TABLE).

import inspect
import sqlite3
import datetime
from typing import Dict, List, Type, Any, Optional, Set

class Modele:
    __nom_table__: Optional[str] = None

    @classmethod
    def recupere_nom_table(cls) -> str:
        if cls.__nom_table__:
            return cls.__nom_table__
        return cls.__name__.lower()
    
    @classmethod
    def recuperer_colones(cls) -> Dict[str, str]:
        return extraire_colones(cls)
    
# extraire les colones completes d'une table
def extraire_colones(classe: Type[Modele]) -> Dict[str, str]:
    annotations = classe.__annotations__
    signature = inspect.signature(classe.__init__)
    parametres = list(signature.parameters.keys())
    print(parametres)
    if 'self' in parametres:
        parametres.remove('self')
    
    colones = {}
    from orm.types_donnees import MapperType
    for nom in parametres:
        type_python = annotations.get(nom, None)
        type_sql = MapperType.type_sql_correspondant(type_python, nom)
        colones[nom] = type_sql
    
    return colones