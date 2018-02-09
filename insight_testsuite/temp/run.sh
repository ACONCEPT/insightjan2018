#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python

#python ./src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

runfolder=$(pwd)
echo $PWD

#sudo apt-get install software-properties-common
#sudo add-apt-repository ppa:deadsnakes/ppa
#sudo apt-get update
#sudo apt-get install python3.6
#sudo apt-get install python3-pip
#sudo apt-get install realpath
#pip3 install virtualenv
#sudo apt-get install git
#python3 -m virtualenv env
source env/bin/activate

#echo 'running from '$(pwd)
#echo 'cd1 '$(pwd)
#echo $(dirname $runfolder)
#echo $(basename $runfolder)
#while [[$(pwd) != '/' && $(basename pwd) != 'donation-analytics']]; do cd ..; done
#echo 'cded to '$(pwd)
#source env/bin/activate


#export SCRIPTPATH=$HOME'/repos/donation-analytics'
export arg1=$(realpath input/itcont.txt)
export arg2=$(realpath input/percentile.txt)
export arg3=$(realpath output/repeat_donors.txt)

python src/run.py $arg1 $arg2 $arg3 
