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