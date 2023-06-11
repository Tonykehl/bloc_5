# Utilisez une image Python de base
FROM python:3.9-alpine

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE $PORT

# Définir la variable d'environnement pour l'exécution de l'application Flask
ENV PORT=$PORT

# Exécuter l'application Flask lorsque le conteneur démarre
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:$PORT"]
