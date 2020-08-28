#!/bin/sh

python -m transcrypt -p .none -bmn hero.py
npx rollup __target__/hero.js -o hero.js -f cjs


python -m transcrypt -p .none -bmn helpers.py
npx rollup __target__/helpers.js -o helpers.js -f cjs
