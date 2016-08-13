import wpilib
from mode_Init import InitRobot

class Teleop:
    def __init__(self, robot_objects):
        """
        @type robot_objects: InitRobot
        """
        self.robot_objects = robot_objects

    def init(self):
        pass

    def periodic_update(self):
        # Set the drive mode to manual mode, arcade split
        self.robot_objects.subsystems.drive_base.do_arcade_split()

        # Grip control
        # Suck in
        if self.robot_objects.devices.driver_station.control_board.getSwitch(7):
            self.robot_objects.devices.motors.grip.set(-0.5)

        # Spit out
        elif self.robot_objects.devices.driver_station.control_board.getSwitch(8):
            self.robot_objects.devices.motors.grip.set(1.0)

        # Idle
        else:
            self.robot_objects.devices.motors.grip.set(-0.2)

