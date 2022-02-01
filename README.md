Assignemnt 3 - Final Assignment
==================================

This is the third and final assignment of the course Research Track 1, provided by Università Degli Studi di Genova, Robotics Engineering degree.
The simulation includes a robot equipped with a leser scanner placed inside an environent in which there are obstacles. 
The objective of the project is to develop an architecture that is able to get the user request, and let the robot execute one of the following behaviors:
* Autonomusly reach a (x,y) coordinate inserted by the user
* Let the user drive the robot with the keyboard
* Let the user drive the robot with the keyboard by assisting him to avoid collisions

The simulation environment seen in Gazebo is the following:

It can can be seen the same simulation in Rviz, which is the following:

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