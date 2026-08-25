-- creer les parametres d'initialisation de la bd --
CREATE USER admin WITH PASSWORD 'admin2026'
CREATE DATABASE blog_bd OWNER admin
GRANT ALL PRIVILEGES ON DATABASE blog_bd TO admin