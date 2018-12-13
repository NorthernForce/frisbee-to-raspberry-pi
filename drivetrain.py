# This class provides a way to drive a robot which has a drive train equipped
# with separate motors powering the left and right sides of a robot.
# Two different drive methods exist:
#   Arcade Drive: combines 2-axes of a joystick to control steering and driving speed.
#   Tank Drive: uses two joysticks to control motor speeds left and right.
# A Pololu Maestro is used to send PWM signals to left and right motor controllers.


# When using motor controllers, the maestro's speed setting can be used to tune the 
# responsiveness of the robot.  Low values dampen acceleration, making for a more
# stable robot. High values increase responsiveness, but can lead to a tippy robot.
# Try values around 50 to 100.
RESPONSIVENESS = 60 # this is also considered "speed"

# These are the motor controller limits, measured in Maestro units.  
# These default values typically work fine and align with maestro's default limits.
# Vaules should be adjusted so that center stops the motors and the min/max values
# limit speed range you want for your robot.
MIN = 4000
CENTER = 6000
MAX = 8000


class DriveTrain:

    # Pass the maestro controller object and the maestro channel numbers being used
    # for the left and right motor controllers.  See maestro.py on how to instantiate maestro.
    def __init__(self, maestro, motors):
        self.maestro = maestro
        self.motors = motors
        # Init motor accel/speed params
        for motor in self.motors:
            self.maestro.setAccel(motor["channel"], 0)
            self.maestro.setSpeed(motor["channel"], RESPONSIVENESS)
        # Motor min/center/max values
        self.min = MIN
        self.center = CENTER
        self.max = MAX

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
                scale = scaleL * motor["direction"];
            else:
                scale = scaleR * motor["direction"];


            if (scale >= 0):
                target = int(self.center + (self.max - self.center) * scale)
            else:
                target = int(self.center + (self.center - self.min) * scale)

            self.maestro.setTarget(motor["channel"], target)

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
            self.maestro.setAccel(motor["channel"], self.center)

    # Close should be used when shutting down Drive object
    def close(self):
        self.stop()
