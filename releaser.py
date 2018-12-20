import simpleservo

class Releaser():
    def __init__(self, maestro, settings):
        self.maestro = maestro
        self.settings = settings
        self.servo = simpleservo.SimpleServo(self.maestro, self.settings["channel"])

    def drive(self, amount):
        self.servo.drive(amount * self.settings["direction"])

    # Set both motors to stopped (center) position
    def stop(self):
        self.servo.close()

    # Close should be used when shutting down Drive object
    def close(self):
        self.stop()