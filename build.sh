#!/bin/sh


check_exit() {
ERR=$?
if [[ $ERR -eq 0 ]];
	then
		echo "Safe";
	else
		exit $ERR;
fi;
}

python3 hero.py # To check syntax in a happy way
check_exit
python3 helpers.py # To check syntax in a happy way
check_exit

python -m transcrypt -p .none -bmn hero.py;
check_exit	
npx rollup __target__/hero.js -o hero.js -f cjs;
check_exit	


python -m transcrypt -p .none -bmn helpers.py;
check_exit	
npx rollup __target__/helpers.js -o helpers.js -f cjs;
check_exit	

