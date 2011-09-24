#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/home/scott/school/capstone/Task-Organizer/src/task/
export PYTHONPATH=$PYTHONPATH:/home/scott/school/capstone/Task-Organizer/src/examples/


coverage erase

echo "TestTask:"
coverage run -a test/test_task.py $1
echo

echo "TestCLIParser:"
coverage run -a test/test_cliparser.py $1
echo

echo "TestTaskStorage:"
coverage run -a test/test_taskstorage.py $1
echo

echo "TestTaskController:"
coverage run -a test/test_taskcontroller.py $1
echo


echo

coverage report -m
#coverage report -m --omit=test*

source .clean_cmd
