include .env

ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

setup:
	pipenv install

build:
	docker build . -t leonpatmore2/wiki-search

run:
	docker run -P -v ${ROOT_DIR}/entire_docs:/app/entire_docs -v ${ROOT_DIR}/docs:/app/docs -e OPENAI_API_KEY=${OPENAI_API_KEY} leonpatmore2/wiki-search

push:
	docker push leonpatmore2/wiki-search
