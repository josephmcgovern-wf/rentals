FORMAT_FILES ?= ./

.PHONY: deps
deps:
	pip3 install -r requirements.txt

.PHONY: format
format:
	black ${FORMAT_FILES}
