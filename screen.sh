#!/bin/bash
python3 -m venv env
source env/bin/activate
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
tar xf geckodriver-v0.29.1-linux64.tar.gz
rm geckodriver-v0.29.1-linux64.tar.gz
mv geckodriver env/bin
screen -S garden_eden -d -m python gui.py
screen -r garden_eden