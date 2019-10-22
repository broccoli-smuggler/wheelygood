# wheelygood
This repo is designed for the prototype of the EasyLink project to be run on a raspberry pi or similar.

It consists of a basic state machine to step through the states 1-9 in a circular manner:
1. In car (no person)
2. Out of car (no person)
3. Locate
4. Successfully located
5. Pick up wheelchair
6. Go into car
7. Out of car (with person)
8. Down (with person)

0. Stop

These states can be transitioned via mouse clicks, forward and backwards. In addition, at any point the stop button can be pressed to immediately to kill the motors. 
