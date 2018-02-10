#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python

#python ./src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

runfolder=$(pwd)
echo $PWD

runas=${1:-executable}
#runas=${1:-script}
environment=${2:-env/bin/activate}
 
## to install dependent bash tools
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update -yq
sudo apt-get install -yq software-properties-common realpath

#export SCRIPTPATH=$HOME'/repos/donation-analytics'
export arg1=$(realpath input/itcont.txt)
export arg2=$(realpath input/percentile.txt)
export arg3=$(realpath output/repeat_donors.txt)

if [ $runas = script ]; then	
	##to run as script from vi@rtualenv use this commad
	echo 'running program as script from env'
	script=${3:-src/run.py}

	sudo apt-get install -yq python3.6 python3-pip

	if [ $(command -v virtualenv) = "" ]; then
		echo 'installing virtulenv '$(command -v virtualenv)
		pip3 install virtualenv
	fi
	
	if [ ! -d env/ ]; then
		echo 'creating virutal env '$(-d env/)
		python3 -m virtualenv env
	fi

	echo 'activating environment '${environment}
	source $environment

	echo 'calling script '${script}

	python $script $arg1 $arg2 $arg3 
fi

if [ $runas = executable ]; then
	##to run as compiled python outside of virtualenv use this command echo 'running program from compiled'
	exec=${3:-src/run}
	echo 'executing executable '${exec}
	$exec $arg1 $arg2 $arg3 
fi
