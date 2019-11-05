# wheelygood
This repo is designed for the prototype of the EasyLink project to be run on a raspberry pi or similar. This is an automated wheelchair system designed to get a person in and out of a normal (ish) car without paying a fortune. Currently it is put together in a as-is, where-is state with many coffees over several weekends.

## Overview
A basic state machine to step through the wheelchair states 1-9 in a circular manner. This is the basic cycle of getting the chair in and out of the car, with and without a person on it.
1. In car (no person)
2. Out of car (no person)
3. Locate - COMPUTER VISION
4. Successfully located
5. Pick up wheelchair
6. Go into car
7. Out of car (with person)
8. Down (with person)

0. Stop

These states can be transitioned via mouse clicks, forward and backwards. In addition, at any point the stop button can be pressed to immediately to kill the motors. 

