# Mapper SQL < - > PYTHON
# Permet le mappage de type de colone et nom SQL python et vice versa

from typing import Type, Optional

class MapperType:

    _PYTHON_A_SQL = {
        int: "INTEGER",
        float: "REAL",
        str: "TEXT",
        bool: "BOOLEAN"
    }

    @classmethod
    def type_sql_correspondant(cls, type_python: Optional[Type], nom_colone: str) -> str:
        nom = nom_colone.lower()

        # expressions et regles regex(expressions reglieres)
        if nom == "id":
            return "INTEGER"
        
        if nom.endswith("_at") or nom.endswith("_date") or nom.endswith("_time"):
            return "DATETIME"
        
        if nom.startswith("is_") or nom.startswith("has_") or nom.startswith("can_"):
            return "BOOLEAN"
        
        if nom.endswith("_url") or nom.endswith("_slug") or nom == "slug":
            return "TEXT"
        
        if type_python in cls._PYTHON_A_SQL:
            return cls._PYTHON_A_SQL[type_python]
        