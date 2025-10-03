build_db:
	@docker-compose up -d --build

make start_db:
	@docker-compose up -d
	
load_db:
	@uv run python3 -m database.scripts.init_db
	@uv run python3 -m etl.load

stop_db:
ifeq ($(DEL),true)
	@echo "Stopping app and destroying database..."
else
	@echo "Stopping app..."
endif

	@docker-compose down $(if $(DEL),-v,)

kill_db:
	@$(MAKE) stop_db DEL=true