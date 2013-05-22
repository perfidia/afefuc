all: generate run

generate:
		make -C resources generate
		./src/utils/mm2xml.py ./resources/testcases/eng.mm ./src/generated/testcases/en.xml

run:
		cd src; python afefuc.py
