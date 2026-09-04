from orm.utilitaires import Modele

# ------------------------------------------------------------
# 1. UTILISATEUR
# ------------------------------------------------------------
class Utilisateur(Modele):
    id: int
    nom: str
    hashpass: str
    role: str
    url_photo_profil: str
    created_at: str
    refresh_token: str
    
    def __init__(
        self,
        id: int,
        nom: str,
        hashpass: str,
        role: str,
        url_photo_profil: str,
        created_at: str,
        refresh_token: str
    ):
        self.id = id
        self.nom = nom
        self.hashpass = hashpass
        self.role = role
        self.url_photo_profil = url_photo_profil
        self.created_at = created_at
        self.refresh_token = refresh_token

    def enregistrer(self):
        pass

    def connexion(self):
        pass

    def recupere_infos(self):
        pass

    def recreer_token_refresh(self):
        pass


# ------------------------------------------------------------
# 2. TAG
# ------------------------------------------------------------
class Tag(Modele):
    def __init__(
        self,
        id: int,
        nom: str,
        slug: str,
        description: str
    ):
        self.id = id
        self.nom = nom
        self.slug = slug
        self.description = description

    def recupérer_tous(self):
        pass

    def enregistrer_tags(self):
        pass

    def recuperer_posts_tags(self, id):
        pass

    def delete_tag(self, id):
        pass


# ------------------------------------------------------------
# 3. POST
# ------------------------------------------------------------
class Post(Modele):
    def __init__(
        self,
        id: int,
        slug: str,
        contenu: str,
        statut: str,
        views: int,
        tags: str,
        titre: str,
        id_auteur: int,
        created_at: str
    ):
        self.id = id
        self.slug = slug
        self.contenu = contenu
        self.statut = statut
        self.views = views
        self.tags = tags
        self.titre = titre
        self.id_auteur = id_auteur
        self.created_at = created_at

    def recuperer_tous(self):
        pass

    def recupere_post(self, id):
        pass

    def enregistrer(self):
        pass

    def update_post(self, id):
        pass

    def supprime_post(self, id):
        pass


# ------------------------------------------------------------
# 4. COMMENTAIRE
# ------------------------------------------------------------
class Commentaire(Modele):
    def __init__(
        self,
        id: int,
        contenu: str,
        id_post: int,
        id_auteur: int,
        id_parent: int,
        created_at: str
    ):
        self.id = id
        self.contenu = contenu
        self.id_post = id_post
        self.id_auteur = id_auteur
        self.id_parent = id_parent
        self.created_at = created_at

    def delete_comment(self, id):
        pass

    def enregistrer_commentaire(self, id_post, id):
        pass

    def recuperer_commentaire(self, id_post):
        pass