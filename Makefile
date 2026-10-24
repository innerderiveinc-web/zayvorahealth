# ============================================================
# ZAYVORA Health OS™ — Developer Makefile
# ============================================================

.PHONY: run test-all quality apk package up down logs restart build migrate test lint clean sync \
        helm-install helm-upgrade shell-identity shell-clinical

# ---------------------------------------------------------------
# Canonical Platform Runners
# ---------------------------------------------------------------
run:
	./start.sh

test-all:
	python3 -m unittest discover -s tests

quality:
	python3 scripts/quality_gate.py

apk:
	./scripts/build_mobile_apk.sh --cloud

package:
	python3 scripts/package_production_release.py

sync:
	./scripts/sync_platform_mirrors.sh

# ---------------------------------------------------------------
# Local dev stack
# ---------------------------------------------------------------
up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose down && docker compose up -d

# ---------------------------------------------------------------
# Alembic migrations
# ---------------------------------------------------------------
migrate:
	docker compose exec identity alembic upgrade head
	docker compose exec clinical alembic upgrade head
	docker compose exec therapeutic alembic upgrade head
	docker compose exec ai alembic upgrade head
	docker compose exec gateway alembic upgrade head
	@echo "✅ All migrations applied"

migrate-create:
	@read -p "Service (identity/clinical/therapeutic/ai/gateway): " svc; \
	read -p "Migration name: " name; \
	docker compose exec $$svc alembic revision --autogenerate -m "$$name"

migrate-downgrade:
	@read -p "Service: " svc; \
	docker compose exec $$svc alembic downgrade -1

# ---------------------------------------------------------------
# Build
# ---------------------------------------------------------------
build:
	docker compose build

build-web:
	docker compose build web

# ---------------------------------------------------------------
# Testing
# ---------------------------------------------------------------
test:
	@echo "Running identity tests…"
	docker compose exec identity python -m pytest tests/ -v
	@echo "Running clinical tests…"
	docker compose exec clinical python -m pytest tests/ -v
	@echo "Running web linting…"
	cd apps/web && npm run lint

test-service:
	@read -p "Service to test: " svc; \
	docker compose exec $$svc python -m pytest tests/ -v

lint:
	cd apps/web && npm run lint
	cd apps/mobile && npx expo-doctor

# ---------------------------------------------------------------
# Shells
# ---------------------------------------------------------------
shell-identity:
	docker compose exec identity bash

shell-clinical:
	docker compose exec clinical bash

shell-postgres:
	docker compose exec postgres psql -U zayvora -d zayvora

# ---------------------------------------------------------------
# Data migration
# ---------------------------------------------------------------
export-sqlite:
	python3 scripts/export_sqlite_to_csv.py

import-postgres:
	python3 scripts/import_csv_to_postgres.py

validate-migration:
	python3 scripts/validate_migration.py

# ---------------------------------------------------------------
# Kubernetes / Helm
# ---------------------------------------------------------------
helm-install:
	helm install zayvora infrastructure/helm/zayvora -f infrastructure/helm/zayvora/values.yaml

helm-upgrade:
	helm upgrade zayvora infrastructure/helm/zayvora -f infrastructure/helm/zayvora/values.yaml

helm-dry-run:
	helm install zayvora infrastructure/helm/zayvora --dry-run --debug

helm-uninstall:
	helm uninstall zayvora

# ---------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------
clean:
	docker compose down -v --remove-orphans
	@echo "✅ All containers and volumes removed"

clean-cache:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null; \
	find . -name "*.pyc" -delete 2>/dev/null; \
	echo "✅ Python cache cleaned"

# ---------------------------------------------------------------
# Help
# ---------------------------------------------------------------
help:
	@echo "ZAYVORA Health OS™ — Available Make Targets:"
	@echo ""
	@echo "  Stack:       make up | make down | make logs | make restart | make build"
	@echo "  Migrations:  make migrate | make migrate-create | make migrate-downgrade"
	@echo "  Testing:     make test | make test-service | make lint"
	@echo "  Data:        make export-sqlite | make import-postgres | make validate-migration"
	@echo "  Shells:      make shell-identity | make shell-clinical | make shell-postgres"
	@echo "  Kubernetes:  make helm-install | make helm-upgrade | make helm-dry-run"
	@echo "  Cleanup:     make clean | make clean-cache"
