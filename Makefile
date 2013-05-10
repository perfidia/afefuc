all: generate run

generate:
		make -C ui generate

run:
		cd src; python afefuc.py


