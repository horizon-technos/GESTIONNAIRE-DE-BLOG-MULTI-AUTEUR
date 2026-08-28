

types =['INTEGER','FLOAT','TEXT','VARCHAR','SERIAL','DATETIME']
sql={
  "int":"INTEGER",
  'float':"FLOAT",
  'str':'TEXT',
  'bool':'BOOLEAN',
}

arbre={}

class Eleve(type):
  def __new__(cls, name, bases, namespace):
    namespace['nom_table']=name.lower()
    colonne={}
    for key,value in namespace.items():
      if key=="__annotations__":
        for k,v in value.items():
         # print(f"{k}: {v}")
        #  print(f"{k}: {v.__name__}")
          if (v.__name__ in sql.keys()):
            colonne[k]=sql[v.__name__]
      if isinstance(value,Colonne):
        #print(value.foreign_key==None)
        if value.foreign_key==None and value.primary==False:
          colonne[key]=value.type
        elif value.foreign_key is not None and value.primary==False:
          #if value.foreign_key.table==name.lower():
           # raise ValueError("La clé étrangère ne doit pas référencé sa propre table")
          print("ok")
          colonne[key]=value.type
          colonne[f"FOREIGN_KEY+{key}"]=f"FOREIGN KEY({key}) REFERENCES {value.foreign_key.table}({value.foreign_key.attribut})"
        else:
          colonne[key]=value 
        print(f"key: {key} value:{value.type}")
    print(colonne.items())
    arbre[name.lower()]=list(colonne.keys())
    namespace['table_colonne']=colonne
    print(f"TABLES :{arbre}")
    return super().__new__(cls,name, bases, namespace)

  def create_table(cls):
    a=[]
  #  print(a.split(''))
    print(cls.table_colonne.items())
    for k,v in cls.table_colonne.items():
      if not k.startswith('FOREIGN_KEY'):
        if isinstance(v,Colonne) and v.primary==True:
          a.append(f'{k} {v.type} PRIMARY KEY')
        elif isinstance(v,Colonne):
          a.append(f'{k} {v.type}')
        else:
          a.append(f'{k} {v}')
    cle=[v for k,v in cls.table_colonne.items() if k.startswith('FOREIGN_KEY')]
    a.extend(cle)
    #     a.append(f"")
    print(",".join(a))
    print(f"CREATE TABLE IF NOT EXISTS {cls.nom_table}({",".join(a) });")

class Foreign_key:
  def __init__(self,table:str,attribut:str):
    self.table=table
    self.attribut=attribut
  
class Colonne:
  def __init__(self,type_:str,foreign_key:Foreign_key=None,primary=False):
    if(type_.upper() in types ):
      pass
    elif (type_.upper().startswith("VARCHAR(") and type_.upper().endswith(")")):
      pass
    else:
      raise ValueError("ce type ne fait pas partie POSTGRES")
    
    self.type=type_.upper()
    self.primary=primary
    if foreign_key!=None and foreign_key.table in arbre.keys() and foreign_key.attribut in sum(arbre.values(),[]) :
       print("c'est bon")
    elif foreign_key==None:
      pass
    else:
      raise TypeError("la clé étrangère est mal configuré")
    self.foreign_key=foreign_key
  def __str__(self,):
    return f"nom:{self.type}\nclé primaire:{self.primary}\nclé étrangère:{self.foreign_key}"    
  
class Student(metaclass=Eleve):
  id=Colonne('serial')
  matricule=Colonne("text")
  def __init__(self):
    pass

class User(metaclass=Eleve):
  id=Colonne("integer",primary=True)
  nom=Colonne('varchar(100)',foreign_key=Foreign_key(table="student",attribut='matricule'))
  age=Colonne("float")
 
  def __init__(self):
    pass

class Post(metaclass=Eleve):
    id=Colonne("serial",primary=True)
    slug=Colonne('text')
    contenu=Colonne('text')
    statut=Colonne('text')
    tags=Colonne('text')
    
    titre=Colonne('text')
    id_auteur=Colonne('varchar(100)')
    created_at=Colonne('datetime')
    nom:str

    def __init__(self, id, slug, contenu, statut, views, tags, titre, id_auteur, created_at):
        self.id = id
        self.slug = slug
        self.contenu = contenu
        self.statut = statut
        self.views = views
        self.tags = tags
        self.titre = titre
        self.id_auteur = id_auteur
        self.created_at = created_at 

Post.create_table()

class Personne(metaclass=Eleve):
  nom : str
  age : int
  l:bool
  id=Colonne("integer",primary=True)

class Utilisateur(metaclass=Eleve):
    id:int
    nom:str
    role:str
    url_photo_profil:str
    created_at:str
    refresh_token:bool
   


hugo = Personne()
hugo.nom="Hugo"
hugo.age=13
#print(hugo.typ(hugo.nom)) 

print(type("12").__name__)

Personne.create_table()
Utilisateur.create_table()