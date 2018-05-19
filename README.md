# Pedestrian Car Project
Autonomous RC Car Project of ME384 Term Project at Bilkent University,
Group: CULT OF MECHATRONICUS

## Getting Started
This repo consists last version of codes of Pedestrian Slayer car which is for school mechatronic term project. However, it still needs heavily development and fixing the bugs in the code. The system is designed for interection between both Raspberry Pi 3 B+ and Arduino Uno.
The car simply has two modes: Manuel and autonomous. In manuel mode, the user will interact with the car and perform basic steering function. Besides, in autonomous mode, using OpenCV library and the neural network algorithm that is developed will steer the car. In this mode, the camera will detect only two white line which is requirement of the project. The system will communicate with Arduino board for motor and servo controlling over USB port. It also performs data acqusitions comes from sensors for controlling tasks.
(Ps:To run LaneDetector.py it is necessary to define the path of the video.)

### Prerequisites
#### Hardware:
Following hardwares were used for this project but alternative ones could be used.
```
Reedy RC car chasis
Raspberry Pi 3 B+
Arduino Uno
Raspberry Pi Camera v2.1
MPU 6050
HC-SR04 Ultrasonic Sensor
Speed Sensor
Servo Motor
HIMOTO RC540 Brushed Motor
Axial AE-2 ESC
```
#### Software:
Following dependicies should be installed before running the code.
```
OpenCV
numpy
scipy
```
### Installing
Write following command to setup the algorithm on Raspberry Pi:
```
git clone https://github.com/Viriliter/PedestrianSlayer/
```
## Project
Diagram shows an overview of schematic of the main code:
![alt text](https://raw.githubusercontent.com/Viriliter/PedestrianSlayer/branch/path/to/img.png)
## Goals
The goal of the project is establish a RC car that follows the lines on the road. Additionally, it is requested to detect the obstacle on road and avoid them creating new route. In the meantime, it will detect the stop sign and stop within 10cm distance.
## Running the tests

## Contributing

## Versioning

## Authors
Mert Limoncuoğlu

## Acknowledgments
Some parts of the lane detection algorithm are adopted by darienmt. For more details,
visit the link: https://github.com/darienmt/CarND-Advanced-Lane-Lines-P4

