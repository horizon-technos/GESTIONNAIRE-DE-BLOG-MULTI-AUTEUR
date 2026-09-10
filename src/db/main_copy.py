# test de l'orm
from orm.connecteur_sgbd import DriverSGBD
from orm.utilitaires import Modele
from modeles import *

# creation du driver
driver = DriverSGBD('SQLITE')
driver.connexionSGBD()

# initialisation du modele globale
Modele.connecter(driver)

requete = Utilisateur._generateur_sql.creer_table(Utilisateur.__name__,Utilisateur.recuperer_colones())
Utilisateur._db.executerRequete(requete)
requete = Post._generateur_sql.creer_table(Post.__name__,Post.recuperer_colones())
Post._db.executerRequete(requete)
requete = Commentaire._generateur_sql.creer_table(Commentaire.__name__,Commentaire.recuperer_colones())
Commentaire._db.executerRequete(requete)
requete = Tag._generateur_sql.creer_table(Tag.__name__,Tag.recuperer_colones())
Tag._db.executerRequete(requete)

# Deconnexion du modele
Modele.deconnecter()
