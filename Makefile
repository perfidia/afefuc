all: generate run

generate:
		make -C resources generate

run:
		cd src; python afefuc.py
