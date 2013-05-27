all: generate run

generate:
		make -C resources generate

run:
		cd src; python afefuc.py

clean:
		rm -rf dist
		for file in `find src -iname *.pyc`; do rm $$file; done

dist: clean generate
		mkdir -p dist/app
		cp -r src/* dist/app
		rm -rf dist/private
		make -C doc html
		cp -r doc/_build/html dist
		mv dist/html dist/doc
		cp resources/call/afefuc.sh dist
