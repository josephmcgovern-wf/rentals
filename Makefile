FORMAT_FILES ?= ./

.PHONY: deps
deps:
	pip3 install -r requirements.txt
	pre-commit install

.PHONY: format
format:
	black ${FORMAT_FILES}
