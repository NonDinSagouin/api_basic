# Utilise l'image Python officielle
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de requirements
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code de l'application
COPY . .

# Expose le port 5000
EXPOSE 5000

# Commande par défaut
CMD ["python", "main.py"]
