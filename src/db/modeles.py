# classe liee a un utilisateur
class Utilisateur:
    def __init__(self, id, nom, hashpass, role, url_photo_profil, created_at, refresh_token):
        self.id = id
        self.nom = nom
        self.hashpass = hashpass
        self.role = role
        self.url_photo_profil = url_photo_profil
        self.created_at = created_at
        self.refrsh_token = refresh_token 

    # fonction d'enregistrement dutilisateur
    def enregistrer():
       pass

    # fonction connexion
    def connexion():
       pass

    # fonction de recuperation des infos
    def recupere_infos():
       pass

    # fonction de creation de nouveau token de rafraichissement
    def recreer_token_refresh():
       pass

class Tag:
  def __init__(self,id,nom,slug,description):
    self.id=id
    self.nom=nom
    self.slug=slug
    self.description=description

    #récupérer tous les tags  
    def recupérer_tous():
       pass

    #enregistrer tags
    def enregistrer_tags():
       pass

    #recuperer tous les posts liés à un tag   
    def recuperer_posts_tags(id):
       pass

    #supprimer tags
    def delete_tag(id):
      pass

# classe de gestion des posts
class Post:
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

    # fonction GET posts
    def recuperer_tous():
       pass

    # fonction GET post unique
    def recupere_post(id):
       pass

    # fonction POST enregistrer post
    def enregister():
       pass

    # fonction PUT update post
    def update_post(id):
       pass

    # fonction DELETE supprime post
    def supprime_post(id):
       pass

class Commentaire:
    def __init__(self,id,contenu,id_post,id_auteur,id_parent,created_at):
        self.id=id
        self.contenu=contenu
        self.id_post=id_post
        self.id_auteur=id_auteur
        self.id_parent=id_parent
        self.created_at=created_at

        #supprimer un commentaire d'un post
        def delete_comment(id):
           pass

        #enregistrer un commentaire d'un post
        def enregistrer_commentaire(id_post,id):
           pass

        #récupérer tous les commentaires d'un Post
        def recuperer_commentaire(id_post):
           pass