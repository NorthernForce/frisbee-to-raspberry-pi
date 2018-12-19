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


class SimpleServo:

    # Pass the maestro controller object and the maestro channel numbers being used
    # for the left and right motor controllers.  See maestro.py on how to instantiate maestro.
    def __init__(self, maestro, channel):
        self.maestro = maestro
        self.channel = channel

        # Init motor accel/speed params
        self.maestro.setAccel(self.channel, 0)
        self.maestro.setSpeed(self.channel, RESPONSIVENESS)

        # Motor min/center/max values
        self.min = MIN
        self.center = CENTER
        self.max = MAX

    # speed is -1.0 to 1.0
    def drive(self, amount):
        # convert to servo units
        if (speed >= 0):
            target = int(self.center + (self.max - self.center) * speed)
        else:
            target = int(self.center + (self.center - self.min) * speed)

        self.maestro.setTarget(self.channel, target)

    # Set both motors to stopped (center) position
    def stop(self):
        self.maestro.setAccel(self.channel, self.center)

    # Close should be used when shutting down Drive object
    def close(self):
        self.stop()
