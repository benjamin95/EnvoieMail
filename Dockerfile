# Utiliser une image Python x86_64 (pour Ubuntu)
FROM --platform=linux/amd64 python:3.10-slim

# Installer les dépendances système pour PyInstaller
RUN apt-get update && apt-get install -y build-essential \
    && apt-get install -y curl git

# Créer un répertoire pour l'application
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source dans le conteneur
COPY . .

# Commande pour créer l'exécutable avec PyInstaller
# Remplace 'main.py' par le nom de ton fichier Python principal si besoin
RUN pyinstaller --onefile main.py

# Exposer un répertoire pour récupérer l'exécutable
# Les fichiers créés se trouvent dans le dossier /app/dist
VOLUME /app/dist

# Définir le comportement par défaut
CMD ["ls", "/app/dist"]
