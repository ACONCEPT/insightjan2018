# How to Run
1. clone the repository, 
2. run run.sh or insight_testsuite/run_tests.sh you have to cd into insight_testsuite to run the tests doesn't work to call it from somewhere else 

all necessary dependency installation and setup should be automatic on an ubuntu 16.04 system

#Unit Tests
execute bash script run.sh as follows to run the unit tests:
`run.sh unit_tests`

FYI:
default mode for the `run.sh` will be to run the included compiled version of the python script from bash that is included in this repository.
alternatively, if run run the script like this: 
`run.sh script` 
it will cause bash to setup and activate an environment before calling the main program from a python interpreter

The main program takes three command line arguments, which are the filenames of input and output files, *output file must be last*
run.sh will provide good default arguments for all of those though, so you do not need to change anything
