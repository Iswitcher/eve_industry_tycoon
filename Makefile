.PHONY: lint
lint:
	pylint ./lib

.PHONY: format
format:
	black --line-length 80 ./lib

.PHONY: freeze
freeze:
	pip freeze > ./requirements.txt

.PHONY: deps
deps:
	pip install -r ./requirements.txt
