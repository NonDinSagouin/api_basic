# Makefile pour le projet api_basic
echo: help

# Variables
DOCKER_DIR = docker
DOCKER_COMPOSE = docker-compose
COMPOSE_DEV = docker-compose.yml
COMPOSE_PROD = docker-compose.prod.yml

.PHONY: help build start stop restart logs clean ssl dev prod test test-redis test-containers

check-docker: ## Vérifie si Docker et Docker Compose sont installés
	@which docker > /dev/null || (echo "❌ Docker n'est pas installé" && exit 1)
	@which docker-compose > /dev/null || (echo "❌ Docker Compose n'est pas installé" && exit 1)

help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev-build: check-docker ## Construit l'environnement de développement
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_DEV) build

dev-up: check-docker ## Lance le développement sans rebuild
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_DEV) up

dev-down: ## Arrête l'environnement de développement
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_DEV) down

dev-restart: ## Redémarre les conteneurs
	$(MAKE) dev-down
	$(MAKE) dev-up

prod: ## Lance l'environnement de production
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) up --build -d

up: ## Démarre les conteneurs de production
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) up -d

down: ## Arrête les conteneurs de production
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) down

restart: ## Redémarre les conteneurs de production
	$(MAKE) down
	$(MAKE) up

logs: ## Affiche les logs
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) logs -f

logs-api: ## Affiche les logs de l'API uniquement
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) logs api_basic-flask-api -f

logs-nginx: ## Affiche les logs de Nginx uniquement
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) logs api_basic-nginx -f

status: ## Affiche le statut des conteneurs
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) ps

clean: ## Nettoie les conteneurs et images
	cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) down -v --rmi all

clean-redis: ## Nettoie les données Redis
	@echo "-- 🧹 Nettoyage des données Redis..."
	@cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) exec redis redis-cli FLUSHALL > /dev/null 2>&1 && echo "✅ Redis data cleared" || echo "❌ Failed to clear Redis data"

ssl: ## Configure SSL avec Let's Encrypt
	@echo "Usage: make ssl DOMAIN=votre-domaine.com"
	@if [ -z "$(DOMAIN)" ]; then \
		echo "Erreur: Veuillez spécifier DOMAIN=votre-domaine.com"; \
		exit 1; \
	fi
	./scripts/setup-ssl.sh $(DOMAIN)

tests: test-containers test-health test-redis ## Exécute tous les tests

test-containers: ## Vérifie que les conteneurs sont en cours d'exécution
	@echo "-- 🔍 Vérification des conteneurs..."
	@if [ -z "$$(cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) ps -q)" ]; then \
		echo "❌ Aucun conteneur en cours d'exécution. Veuillez démarrer les conteneurs avec 'make up'."; \
		exit 1; \
	else \
		echo "✅ Conteneurs en cours d'exécution:"; \
		cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) ps; \
	fi

test-health: ## Teste la santé de l'API
	@echo "-- 🔍 Test de santé de l'API..."
	@curl -f -s http://localhost/health/check > /dev/null && echo "✅ API is healthy" || (echo "❌ API is not responding" && exit 1)

test-redis: ## Teste la connexion à Redis
	@echo "-- 🔍 Test de connexion à Redis..."
	@cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) exec redis redis-cli ping > /dev/null 2>&1 && echo "✅ Redis is responding" || (echo "❌ Redis is not responding" && exit 1)
	@echo "🔍 Test d'écriture/lecture Redis..."
	@cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) exec redis redis-cli set test_key "test_value" > /dev/null 2>&1
	@cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) exec redis redis-cli get test_key | grep -q "test_value" && echo "✅ Redis write/read test passed" || (echo "❌ Redis write/read test failed" && exit 1)
	@cd $(DOCKER_DIR) && $(DOCKER_COMPOSE) -f $(COMPOSE_PROD) exec redis redis-cli del test_key > /dev/null 2>&1
	@echo "✅ All Redis tests passed"
