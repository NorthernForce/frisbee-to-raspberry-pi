# Here's a basic robot loop to drive a robot using the left analog stick of
# an Xbox controller.  The robot left and right drive motors are assumed
# to be connected to channels 0 and 1 of a Maestro controller.

import maestro
import xbox
import drivetrain
import time

m = maestro.Controller()
motors = [
    {
        "channel": 0,
        "side": 0,
        "direction": 1
    },
    {
        "channel": 1,
        "side": 0,
        "direction": -1
    },
    {
        "channel": 2,
        "side": 1,
        "direction": -1
    },
    {
        "channel": 3,
        "side": 1,
        "direction": 1
    },
]
dt = drivetrain.DriveTrain(m, motors)
j = xbox.Joystick()

# Wrapping the robot loop in a try/finally structure makes sure that the robot stops
# moving if your code errors out or the robot loop completes. 
try:
    enabled = True
    print "Robot loop started"
    while enabled:
        # As long as the joystick is connected, drive the robot, otherwise stop the motors
        if j.connected():
            # Joystick inputs are sent to the drive train in Arcade Drive mode
            # If controls are backwards, simply negate the respective input
            dt.drive(j.leftX(), j.leftY())
            # Pressing the Xbox back button will disable the robot loop
            if j.Back():
                enabled = False
        else:
            dt.stop()
        time.sleep(0.02)  #Throttle robot loop to around 50hz
except:
    j.close();
    dt.stop();
finally:
    print "stopping robot"
    j.close();
    dt.stop()  #stop on error or loop completion
    
