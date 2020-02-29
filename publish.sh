rm -R ./dist/*
./build.sh
python -m twine upload dist/*
