set -xe

if [ -z "$1" ]; then
    echo "Variable is empty"
    exit 1
fi

cd projects/$1

rm -rf dist

poetry build-project 

cd dist

tar -xvf *.tar.gz

cd $1-*

zip -r ../$1.zip *