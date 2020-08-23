#!/bin/sh

python -m transcrypt -p .none -bmn hero.py
npx rollup __target__/hero.js -o hero.js -f cjs
