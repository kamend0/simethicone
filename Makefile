start_db:
	@docker-compose up -d --build

init_db:
	@uv run python3 -m database.scripts.init_db

load_db:
	@uv run python3 -m etl.load

stop:
ifeq ($(DEL),true)
	@echo "Stopping app and destroying database..."
else
	@echo "Stopping app..."
endif

	@docker-compose down $(if $(DEL),-v,)

kill:
	@$(MAKE) stop DEL=true