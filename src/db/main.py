from modeles import Utilisateur

print("hello world")
user = Utilisateur(
    id=13,
    nom="Polo",
    hashpass="weyfgkefhjaef",
    role='admin',
    url_photo_profil="eyfyuwefkiweugf",
    created_at="12/2/2026",
    refresh_token="twgfjeghifhwkqjhkequgf"
)

print(user._get_colones())