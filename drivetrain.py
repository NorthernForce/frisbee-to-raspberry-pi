# This class provides a way to drive a robot which has a drive train equipped
# with separate motors powering the left and right sides of a robot.
# Two different drive methods exist:
#   Arcade Drive: combines 2-axes of a joystick to control steering and driving speed.
#   Tank Drive: uses two joysticks to control motor speeds left and right.
# A Pololu Maestro is used to send PWM signals to left and right motor controllers.

import simpleservo

class DriveTrain:

    # Pass the maestro controller object and the maestro channel numbers being used
    # for the left and right motor controllers.  See maestro.py on how to instantiate maestro.
    def __init__(self, maestro, motors):
        self.maestro = maestro
        self.motors = motors
        # Init motor accel/speed params
        for index, motor in enumerate(self.motors):
            self.motors[index]["servo"] = simpleservo(m, self.motors["channel"])

    # Mix steering and speed inputs (-1.0 to 1.0) into motor L/R powers (-1.0 to 1.0).
    def _arcadeMix(self, steer, drive):
        v = (1 - abs(steer)) * drive + drive
        w = (1 - abs(drive)) * steer + steer
        scaleL = (v - w) / 2
        scaleR = -(v + w) / 2
        return (scaleL, scaleR)

    # Drive the robot motors given steering and speed parameters (arcade drive).
    # These typically come from X and Y axes of a joystick.
    # Valid inputs range between -1.0 and 1.0.
    # If steering or speed run in reverse direction, simple negative the respective input.
    def drive(self, steer, speed):
        (scaleL, scaleR) = self._arcadeMix(steer, speed)

        for motor in self.motors:
            if (motor["side"] == 0):
                scale = scaleL * motor["direction"]
            else:
                scale = scaleR * motor["direction"]

            motor["servo"].drive(scale)

    # Drive the robot motors given left and right motor powers (tank drive).
    # These motor powers typically come from the Y axis of 2 analog joysticks.
    # Valid input range is between -1.0 and 1.0.
    #def tankDrive(self, motorL, motorR):
        #(maestroL, maestroR) = self._maestroScale(motorL, motorR)
        #self.maestro.setTarget(self.chLeft, maestroL)
        #self.maestro.setTarget(self.chRight, maestroR)

    # Set both motors to stopped (center) position
    def stop(self):
        for motor in self.motors:
            motor["servo"].close()

    # Close should be used when shutting down Drive object
    def close(self):
        self.stop()
