#!usr/bin/env bash
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python3-pip
sudo apt-get install realpath
pip3 install virtualenv
sudo apt-get install git
python3 -m virtualenv env
source env/bin/activate
