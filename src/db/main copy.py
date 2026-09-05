from modeles import Utilisateur
from orm.generateur_sql import GenerateurSQL

gen = GenerateurSQL()

utilisateur = Utilisateur
utilisateur.__nom_table__ = utilisateur.__name__

utilisateur.id = 1
utilisateur.nom = "Polo"
utilisateur.hashpass = "rtywrgydtyqwefg"
utilisateur.role = "admin"
utilisateur.url_photo_profil = "/yfgyfweuf/"
utilisateur.created_at = "1387236"
utilisateur.recreer_token_refresh = "Polo"

colones = utilisateur.recuperer_colones()

print(gen.creer_table(nom_table=utilisateur.__nom_table__,colones=colones))