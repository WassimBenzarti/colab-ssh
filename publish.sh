rm -Rf ./dist/*
./build.sh
python -m twine upload dist/*
