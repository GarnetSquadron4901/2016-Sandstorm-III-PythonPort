import wpilib
from mode_Init import InitRobot

import time

class Autonomous:

    STATE_INIT = 'Initialize Autonomous'
    STATE_GO_FORWARD_3250_MS = 'Moving forward 3.25 seconds @ 90% power'
    STATE_FINISHED = 'Autonomous Finished'
    START_STATE_GO_FORWARD_3250_MS = 'Starting autonomous'

    GO_FORWARD_SPEED = 0.9

    def __init__(self, robot_objects):
        """
        @type robot_objects: InitRobot
        """

        self.robot_objects = robot_objects
        self.start_time = None
        self.state = None
        self.last_state = None
        self.state_go_forward_3250_ms_start_time = None

        self.disable_motors = self.robot_objects.subsystems.drive_base.do_disabled
        self.set_motors = self.robot_objects.subsystems.drive_base.do_command

    def auto_init(self):
        """ Used right before autonomous. Might be a good place to grab the time or reset encoders. """
        self.state = self.STATE_INIT
        self.start_time = time.time()
        self.last_state = self.STATE_INIT

    def periodic_update(self):
        self.robot_objects.devices.motors.grip.set(-0.2)

        self.check_mode()

        if self.state is self.STATE_INIT:
            self.state = self.START_STATE_GO_FORWARD_3250_MS

        elif self.state is self.START_STATE_GO_FORWARD_3250_MS:
            self.set_motors(0, 0)
            self.state_go_forward_3250_ms_start_time = time.time()
            self.state = self.STATE_GO_FORWARD_3250_MS

        elif self.state is self.STATE_GO_FORWARD_3250_MS:
            self.set_motors(self.GO_FORWARD_SPEED, self.GO_FORWARD_SPEED)
            if (time.time() - self.state_go_forward_3250_ms_start_time) >= 3.250:
                self.state = self.STATE_FINISHED

        elif self.state is self.STATE_FINISHED:
            self.disable_motors()

    def check_mode(self):
        if self.state != self.last_state:
            msg = 'State Change: '
            msg += 'New State: %s' % self.state
            if self.last_state is not None:
                msg += '; Old State: %s' % self.last_state
            self.last_state = self.state
            self.print_autonomous(msg)

    def print_autonomous(self, msg):
        print('Autonomous:', msg)

    def get_auto_time(self):
        return time.time() - self.start_time
