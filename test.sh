#!/bin/sh

sh build.sh
ERR=$?
if [[ $ERR -eq 0 ]]; then

node test-battle.js $@;

fi
