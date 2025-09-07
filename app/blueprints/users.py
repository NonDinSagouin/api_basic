from flask import Blueprint, jsonify, request

# Création du blueprint pour les routes des utilisateurs
users_bp = Blueprint('users', __name__, url_prefix='/users')

# Simulation d'une base de données en mémoire
users_db = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@users_bp.route('/get', methods=['GET'])
def get_users():
    """Récupère la liste de tous les utilisateurs"""
    return jsonify(users_db)
