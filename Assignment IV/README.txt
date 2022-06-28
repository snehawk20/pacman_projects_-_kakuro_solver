README

Welcome to the Pacman Project.

The aim of this project is to design an intelligent Pacman agent that moves optimally through the Pacman world and eats all the food dots in as few steps as possible. For this part of the project the ghosts are neglected. The first section involves implementing graph search algorithms such as DFS, BFS, UCS, A* search. The second section involves writing a state space representation for the corners problem and designing and implementing consistent heuristics for the corners problem and the food search problem.
This part of the lab has been adopted from Berkeley Pacman projects.

This project is compatible with python 3.6.
The folder code contains several .py files, of which the ones which have been edited due course of this project are:
inference.py
factorOperations.py

In this project, we design Pacman agents that use sensors to locate and eat invisible ghosts.

In this of Ghostbusters, the goal is to hunt down scared but invisible ghosts. Pacman, ever resourceful, is equipped with sonar (ears) that provides noisy readings of the Manhattan distance to each ghost. The game ends when Pacman has eaten all the ghosts.

To evaluate all the questions at once, use 
>>> python autograder.py

To run the test cases one at a time, use the -t flag with the autograder. For example if you only want to run the first test of question 1, use:
>>> python autograder.py -t test_cases/q1/1-ObsProb

In general, all test cases can be found inside test_cases/q*.

For this project, it is possible sometimes for the autograder to time out if running the tests with graphics. 
To accurately determine whether or not your code is efficient enough, you should run the tests with the --no-graphics flag.