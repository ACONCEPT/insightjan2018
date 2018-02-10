#!usr/bin/env bash
sudo rm -rf dist
rm run
source ../env/bin/activate
pyinstaller run.py 
ln -s dist/run/run run
