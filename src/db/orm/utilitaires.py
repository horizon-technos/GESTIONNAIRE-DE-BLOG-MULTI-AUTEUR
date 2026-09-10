# fonctions utilitaires de l'ORM 
# ROLE    : Moteur central de l'ORM.
#           - Classe Modele pour héritage.
#           - Extraction du schéma des classes.
#           - Comparaison avec la base réelle.
#           - Exécution des migrations (ALTER TABLE).

import inspect
from typing import Dict, Type, Optional, List
from orm.connecteur_sgbd import DriverSGBD
from orm.generateur_sql import GenerateurSQL

class Modele:
    _db: Optional[DriverSGBD] = None
    _generateur_sql: Optional[GenerateurSQL] = None

    @classmethod
    def connecter(self, instance_driver: DriverSGBD):
        if self._db is not None:
            raise RuntimeError("Une connexion est déjà définie. Utilisez deconnecter() d'abord.")
        self._db = instance_driver
        self._generateur_sql = GenerateurSQL(dialecte=self._db.dialecte)

    @classmethod
    def deconnecter(self) -> None:
        if self._db:
            try:
                self._db.deconnecterSGBD()
            finally:
                self._db = None
                self._generateur_sql = None

    @classmethod
    def _recuperer_bd(self):
        if self._db is None:
            raise RuntimeError("Connexion BD non existante")
        return self._db
    
    @classmethod
    def recuperer_colones(self) -> Dict[str, str]:
        return extraire_colones(self)
    
    # Gestion des migrations
    def _compare_schema():
        pass
    
# extraire les colones completes d'une table
def extraire_colones(classe: Type[Modele]) -> Dict[str, str]:
    annotations = classe.__annotations__
    signature = inspect.signature(classe.__init__)
    parametres = list(signature.parameters.keys())
    if 'self' in parametres:
        parametres.remove('self')
    
    colones = {}
    from orm.types_donnees import MapperType
    for nom in parametres:
        type_python = annotations.get(nom, None)
        type_sql = MapperType.type_sql_correspondant(type_python, nom)
        colones[nom] = type_sql
    
    return colones