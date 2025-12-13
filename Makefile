.PHONY: start
start:
	docker compose up --build -d
	docker compose logs -f application


.PHONY: lint
lint:
	ruff check --fix
	mypy ./app


.PHONY: logs
logs:
	docker compose logs -f application
