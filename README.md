Assignemnt 3 - Final Assignment
==================================

This is the third and final assignment of the course Research Track 1, provided by Università Degli Studi di Genova, Robotics Engineering degree.
The simulation includes a robot equipped with a leser scanner placed inside an environent in which there are obstacles. 
The objective of the project is to develop an architecture that is able to get the user request, and let the robot execute one of the following behaviors:
* Autonomusly reach a (x,y) coordinate inserted by the user
* Let the user drive the robot with the keyboard
* Let the user drive the robot with the keyboard by assisting him to avoid collisions

The simulation environment seen in Gazebo is the following:
![simulation_environment](https://github.com/FraFerrazzi/final_assignment/blob/noetic/images/Schermata%202022-02-01%20alle%2020.54.15.png)
It can can be seen the same simulation environment in Rviz, which is the following:
![rviz_environment](https://github.com/FraFerrazzi/final_assignment/blob/noetic/images/Schermata%202022-02-01%20alle%2021.35.05.png)
This solution is developed by: Francesco Ferrazzi 5262829.

Table of Contents
----------------------


Installing and running
----------------------

The simulator requires a [ROS Noetic](http://wiki.ros.org/noetic/Installation) installation and the following packages, if they are not already installed:

* install teleop twist keyboard package by typing on terminal:
```bash
$ sudo apt-get install ros-noetic-teleop-twist-keyboard
```
* install the ros navigation stack by typing on terminal:
```bash
$ sudo apt-get install ros-noetic-navigation
```
* install xterm package by typing on terminal:
```bash
$ sudo apt-get install xterm
```
* to run the program is sufficient to clone the GitHub repository using the following commands:
```bash
$ git clone https://github.com/CarmineD8/slam_gmapping.git
```
```bash
$ git clone https://github.com/FraFerrazzi/final_assignment.git
```
Remember to switch on the correct branch (noetic) for both projects using:
```bash
$ git checkout noetic
```
* RUN THE PROGRAM typing on terminal:
```bash
$ roslaunch final_assignment final_assignment.launch
```

Project Description
-------------------

The objective of the assignment is to make the robot go around the environment allowing the user to choose between the driving modality specified in the introduction of the project.
In addition to allow the robot to drive autonomusly towards the goal, drive it manually with and without driving assistance, i implemented the following behaviors:
* cancel the goal whenever the user wants
* reset the position of the robot in the environment 
* shout down the program 

To implement the solution, the node `main_ui` was implemented.
Th structure of the code is the following:
![code_structure](https://github.com/FraFerrazzi/final_assignment/blob/noetic/images/Schermata%202022-02-01%20alle%2022.16.38.png)
