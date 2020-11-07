#!/bin/sh
deactivate
git checkout master
git pull
rm -r backtickbot-venv
python3 -m venv backtickbot-venv
