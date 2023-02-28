up:
	docker compose up -d --build

down:
	docker compose down

run-tests:
	docker compose exec -T api pytest -vv tests/$(path)

gen-migration:
	docker compose exec -T api alembic -c docker.ini revision --autogenerate -m "$(message)"

upgrade-db:
	docker compose exec -T api alembic -c docker.ini upgrade heads

format-code:
	docker compose exec -T api ./scripts/format_code.sh

check-formatting:
	docker compose exec -T api ./scripts/check_formatting.sh
