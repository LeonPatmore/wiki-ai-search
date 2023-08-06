include .env

ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
TAG := 0.0.1

setup:
	pipenv install

build:
	docker build . -t leonpatmore2/wiki-search:${TAG}

run:
	docker run -P -v ${ROOT_DIR}/entire_docs:/app/entire_docs -v ${ROOT_DIR}/docs:/app/docs -e OPENAI_API_KEY=${OPENAI_API_KEY} leonpatmore2/wiki-search

push:
	docker push leonpatmore2/wiki-search:${TAG}

install:
	helm upgrade --install wiki-search chart --set tag=${TAG} --set openAiApiKey=${OPENAI_API_KEY} ${INSTALL_PARAMS}
