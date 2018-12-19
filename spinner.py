import simpleservo

class Spinner():
    def __init__(self, m, settings)
        self.settings = settings
        self.servo = simpleservo.SimpleServo(self, m, self.settings["channel"])

    def drive(amount)
        self.servo.drive(amount * self.settings["direction"])

    # Set both motors to stopped (center) position
    def stop(self):
        self.servo.close()

    # Close should be used when shutting down Drive object
    def close(self):
        self.stop()