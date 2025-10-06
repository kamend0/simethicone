build:
	@docker-compose up -d --build

start:
	@docker-compose up -d

load_db:
	@echo "Running ETL process (takes about a minute)..."
	@docker exec simethicone-api-1 python3 -m src.etl.run

stop:
ifeq ($(DEL),true)
	@echo "Stopping app and destroying database..."
else
	@echo "Stopping app..."
endif
	@docker-compose down $(if $(DEL),-v,)

kill:
	@$(MAKE) stop DEL=true