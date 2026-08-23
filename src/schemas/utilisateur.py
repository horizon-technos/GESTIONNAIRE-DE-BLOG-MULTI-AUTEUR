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
