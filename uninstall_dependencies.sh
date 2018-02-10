#!usr/bin/env bash
sudo add-apt-repository -r ppa:deadsnakes/ppa
sudo apt-get remove -yq software-properties-common realpath
pip3 uninstall virtualenv
sudo apt-get remove  -yq python3.6 python3-pip


