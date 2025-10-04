build:
	@docker-compose up -d --build

start:
	@docker-compose up -d
	
load_db:
	@uv run python3 -m src.database.scripts.init_db
	@uv run python3 -m src.etl.load

stop:
ifeq ($(DEL),true)
	@echo "Stopping app and destroying database..."
else
	@echo "Stopping app..."
endif

	@docker-compose down $(if $(DEL),-v,)

kill:
	@$(MAKE) stop DEL=true