# Makefile pour le projet api_basic

.PHONY: help build start stop restart logs clean ssl dev prod test

help: ## Affiche l'aide
	@echo "Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construit les images Docker
	cd docker && docker-compose build

dev: ## Lance l'environnement de développement
	cd docker && docker-compose up --build

prod: ## Lance l'environnement de production
	cd docker && docker-compose -f docker-compose.prod.yml up --build -d

start: ## Démarre les conteneurs
	cd docker && docker-compose -f docker-compose.prod.yml up -d

stop: ## Arrête les conteneurs
	cd docker && docker-compose -f docker-compose.prod.yml down

restart: ## Redémarre les conteneurs
	$(MAKE) stop
	$(MAKE) start

logs: ## Affiche les logs
	cd docker && docker-compose -f docker-compose.prod.yml logs -f

logs-api: ## Affiche les logs de l'API uniquement
	docker logs api_basic-flask-api -f

logs-nginx: ## Affiche les logs de Nginx uniquement
	docker logs api_basic-nginx -f

status: ## Affiche le statut des conteneurs
	cd docker && docker-compose -f docker-compose.prod.yml ps

clean: ## Nettoie les conteneurs et images
	cd docker && docker-compose -f docker-compose.prod.yml down -v --rmi all

ssl: ## Configure SSL avec Let's Encrypt
	@echo "Usage: make ssl DOMAIN=votre-domaine.com"
	@if [ -z "$(DOMAIN)" ]; then \
		echo "Erreur: Veuillez spécifier DOMAIN=votre-domaine.com"; \
		exit 1; \
	fi
	./scripts/setup-ssl.sh $(DOMAIN)

test: ## Teste l'API
	@echo "Test de l'API..."
	@curl -s http://localhost/health/check | grep -q "healthy" && echo "✅ API is healthy" || echo "❌ API is not responding"
