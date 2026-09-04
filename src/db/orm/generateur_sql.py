# generateur de code SQL en fonction du dialecte BD
from typing import Optional, Dict

class GenerateurSQL:
    def __init__(self, dialecte: str = "sqlite"):
        dialecte = dialecte.lower()
        if dialecte not in ("sqlite","postgres","mysql"):
            raise ValueError(f"Dialecte '{dialecte}' non supporté. Choisissez sqlite, postgres ou mysql.")
        
        self.dialecte = dialecte
        
        self._guillemets_en_fonction_sgbd = {
            "sqlite": '"',
            "postgres": '"',
            "mysql": '`'
        }

        self._templates_modification_colone_table_en_fonction_sgbd = {
            "mysql": 'ALTER TABLE {table} MODIFY COLUMN {colone} {type};',
            "postgres": 'ALTER TABLE {table} ALTER COLUMN {colone} TYPE {type} USING {colone}::{type};'
        }

    # encadre avec les bons guillemets un code sql en fonction du sgbd
    def _guillemet_sgbd(self, nom: str):
        guillemets = self._guillemets_en_fonction_sgbd[self.dialecte]
        return f"{guillemets}{nom}{guillemets}"
    
    # creer une table
    def creer_table(self, nom_table: str, colones: Dict[str, str]) -> str:
        definitions = []

        for nom, type_colone in colones.items():
            type_majuscule = type_colone.upper()

            if nom == "id" and ("INT" in type_majuscule or "SERIAL" in type_majuscule):
                if self.dialecte == "postgres":
                    definitions.append(f"{nom} SERIAL PRIMARY KEY")
                elif self.dialecte == "sqlite":
                    definitions.append(f"{nom} {type_colone} PRIMARY KEY AUTOINCREMENT")
                elif self.dialecte == "mysql":
                    definitions.append(f"{nom} {type_colone} AUTO_INCREMENT PRIMARY KEY")
                else:
                    definitions.append(f"{nom} {type_colone} PRIMARY KEY")
            else:
                definitions.append(f"{nom} {type_colone}")

        # jointure en une seule fois pas dans la boucle pour une meilleure optimisation
        jointure_complete = ", ".join(definitions)
        return f"CREATE TABLE IF NOT EXISTS {nom_table} ({jointure_complete});"
    
    # ajouter une colone
    def ajouter_colone(self, nom_table: str, type_colone: str, nom_colone: str) -> str:
        return f"ALTER TABLE {self._guillemet_sgbd(nom_table)} ADD COLUMN {self._guillemet_sgbd(nom_colone)} {type_colone};"
    
    # retirer une colone
    def retirer_colone(self, nom_table: str, nom_colone: str) -> str:
        return f"ALTER TABLE {self._guillemet_sgbd(nom_table)} DROP COLUMN {self._guillemet_sgbd(nom_colone)};"
    
    # modifier une colone
    def modifier_colone(self, nom_table: str, nom_colone: str, nouveau_type: str) -> str:
        if self.dialecte == "sqlite":
            raise NotImplementedError(
                f"SQLite ne supporte pas MODIFY COLUMN."
                f"Pour modifier '{nom_colone}', il faut recreer la table completement."
                f"Utilisez plutot drop_column + add_column, ou creez une nouvelle table."
            )
        
        if self.dialecte not in self._templates_modification_colone_table_en_fonction_sgbd:
            raise ValueError(f"Dialecte '{self.dialecte}' non supporté pour MODIFY.")
        
        return self._templates_modification_colone_table_en_fonction_sgbd[self.dialecte].format(
            table=self._guillemet_sgbd(nom_table),
            colone=self._guillemet_sgbd(nom_colone),
            type=nouveau_type
        )
    
    #renommer une colone
    def renommer_colone(self,nom_table: str, nom_ancien: str, nouveau_nom: str) -> str:
        if self.dialecte == "mysql":
            raise NotImplementedError(
                f"MySQL ne supporte pas RENAME COLUMN directement."
                f"Utilisez ALTER TABLE ... CHANGE COLUMN (qui nécessite de retapper le type)."
            )
        return f"ALTER TABLE {self._guillemet_sgbd(nom_table)} RENAME COLUMN {self._guillemet_sgbd(nom_ancien)} TO {self._guillemet_sgbd(nouveau_nom)};"

    # supprimer la table
    def retirer_table(self, nom_table: str) -> str:
        return f"DROP TABLE IF EXISTS {self._guillemet_sgbd(nom_table)};"