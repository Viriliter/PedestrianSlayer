# Pedestrian Car Project
This repo consists last version of codes of Pedestrian Slayer car which is for school mechatronic term project. However, it still needs heavily development and fixing the bugs in the code. The system is designed for interection between both Raspberry Pi 3 B+ and Arduino Uno.
The car simply has two modes: Manuel and autonomous. In manuel mode, the user will interact with the car and perform basic steering function. Besides, in autonomous mode, using OpenCV library and the neural network algorithm that is developed will steer the car. In this mode, the camera will detect only two white line which is requirement of the project. The system will communicate with arduino board for motor and servo controlling over serial port. It also performs data acqusitions comes from sensors for controlling tasks.
(Ps:To run LaneDetector.py it is necessary to define the path of the video.)
## Getting Started

### Prerequisites
#### Hardware:
```
Raspberry Pi 3 B+
Arduino Uno
Raspberry Pi Camera v2.1
MPU 6050
Ultrasonic Sensor
Servo Motor
DC Brushed Motor
ESC
```
#### Software:
```
OpenCV
```
### Installing

## Running the tests

## Contributing

## Versioning

## Authors

## Acknowledgments
Some parts of the lane detection algorithm are adopted by darienmt. For more details,
visit the link: https://github.com/darienmt/CarND-Advanced-Lane-Lines-P4

