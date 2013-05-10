generate:
		for input in *.ui; do\
			filename=`basename $$input .ui`;\
			pyuic4 $$input > ../src-ui/ui/$$filename.py;\
		done;
