.PHONY: doc

all: generate run

generate:
		make -C resources generate

run:
		cd src; python afefuc.py

clean:
		rm -rf dist
		for file in `find src -iname *.pyc`; do rm $$file; done

doc:
		make -C doc html

dist: clean generate doc
		mkdir -p dist/app
		cp -r src/* dist/app
		rm -rf dist/private
		cp -r doc/_build/html dist
		mv dist/html dist/doc
		cp resources/call/afefuc.sh dist
		cp resources/call/afefuc.bat dist
		-rm dist.zip
		zip dist.zip -r dist/*
