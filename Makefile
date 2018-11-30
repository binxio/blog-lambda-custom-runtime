.PHONY: help
.DEFAULT_GOAL := help
environment = "example"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

create: dist ## create env
	@sceptre launch-env $(environment)

delete: ## delete env
	@sceptre delete-env $(environment)

dist: ## create lambda.zip
	chmod 755 bootstrap
	chmod 755 function.sh
	zip lambda.zip bootstrap function.sh

clean: ## remove artifacts
	rm lambda.zip

init: ## initializes virtualenv
	pipenv install three --dev

rm: ## removes the virtual env
	pipenv --rm

invoke: ## invoke the lambda
	./call-api-gw.sh