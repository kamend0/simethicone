build:
	@docker-compose up -d --build

start:
	@docker-compose up -d

stop:
ifeq ($(DEL),true)
	@echo "Stopping app and destroying database..."
else
	@echo "Stopping app..."
endif
	@docker-compose down $(if $(DEL),-v,)

kill:
	@$(MAKE) stop DEL=true