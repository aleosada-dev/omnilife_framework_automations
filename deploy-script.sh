#! /usr/bin/env zsh

declare PROJECT_NAME=$1

set -xe
setopt EXTENDED_GLOB

if [ -z "$PROJECT_NAME" ]; then
    echo "Variable is empty"
    exit 1
fi

cd projects/$PROJECT_NAME

rm -rf dist

poetry build-project 

cd dist

tar -xvf *.tar.gz

cd $PROJECT_NAME-0.1.0

poetry install

cp -r .venv/lib/python3.11/site-packages/*~*info(/) .

rm -rf __pycache__ .venv

zip -r ../$PROJECT_NAME.zip *