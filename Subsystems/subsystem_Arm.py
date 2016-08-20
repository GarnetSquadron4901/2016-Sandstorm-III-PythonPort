import wpilib
from wpilib.command import Command
import mode_Init
from Algorithms.PID import PID_Position


class Arm(Command):

    MODE_DISABLED = 'Disabled'
    MODE_MANUAL = 'Manual'
    MODE_PRESET = 'Preset'
    MODE_COMMAND = 'Command'

    PRESET_SHOOT_BATTER = {'Name':'Shoot Batter', 'Angle':158}
    PRESET_SHOOT_CLOSE = {'Name':'Shoot Close', 'Angle':152}
    PRESET_CROSS_DEFENSE = {'Name':'Cross Defense', 'Angle':121}
    PRESET_HUMAN_PLAYER_LOAD = {'Name':'Human Player Load', 'Angle':188}
    PRESET_LOW_BAR_GOAL = {'Name':'Low Bar / Low Goal', 'Angle':88}

    MIN_ANGLE = PRESET_LOW_BAR_GOAL['Angle']
    MAX_ANGLE = PRESET_HUMAN_PLAYER_LOAD['Angle']

    # PID Contants
    PID_KP = 1.0
    PID_KI = 0.0
    PID_KD = 0.0
    PID_OUT_MAX = 1
    PID_OUT_MIN = -1
    PID_I_MAX = 1
    PID_I_MIN = -1


    def start(self, devices):
        """
        :param devices: mode_Init:Devices
        """
        self.devices = devices
        super().start()

    def initialize(self):
        self.mode = self.MODE_DISABLED
        self.last_mode = None

        self.calc_manual_conversion()

        self.pid = PID_Position(Kp=self.PID_KP,
                                Ki=self.PID_KI,
                                Kd=self.PID_KD,
                                integrator_max=self.PID_I_MAX,
                                integrator_min=self.PID_I_MIN,
                                output_max=self.PID_OUT_MAX,
                                output_min=self.PID_OUT_MIN)


    def do_mode_disabled(self):
        self.mode = self.MODE_DISABLED

    def do_mode_manual(self):
        self.mode = self.MODE_MANUAL

    def do_mode_preset(self, preset):
        self.mode = self.MODE_PRESET
        self.preset = preset

    def calc_manual_conversion(self):
        y2 = self.MAX_ANGLE
        y1 = self.MIN_ANGLE
        x2 = 255
        x1 = 0
        self.manual_scalar = (y2-y1) / (x2-x1)
        self.manual_offset = y2 - (self.manual_scalar * x2)

    def get_manual_angle(self):
        return self.devices.driver_station.control_board.getAnalog(0) * self.manual_scalar + self.manual_offset

    def execute(self):

        self.check_mode()

        try:
            output = 0
            if self.mode is self.MODE_DISABLED:
                output = 0

            elif self.mode is self.MODE_MANUAL:
                self.angle = self.get_manual_angle()
                self.pid.set_setpoint(self.angle)
                self.pid.update(self.devices.sensors.arm_angle_sensor.getAngle())
                output = self.pid.get_output()

            elif self.mode is self.MODE_PRESET:
                self.check_preset()
                self.angle = self.preset['Angle']
                self.pid.set_setpoint(self.angle)
                self.pid.update(self.devices.sensors.arm_angle_sensor.getAngle())
                output = self.pid.get_output()

            self.devices.motors.arm.set(output)

        except Exception as e:
            print('Unhandled exception', e)

    def check_mode(self):
        if self.mode != self.last_mode:
            msg = 'Mode Change: '
            msg += 'New Mode: %s' % self.mode
            if self.last_mode is not None:
                msg += '; Old Mode: %s' % self.last_mode
            self.last_mode = self.mode
            self.print_arm(msg)

    def check_preset(self):
        if self.preset != self.last_preset:
            msg = 'Preset Change: '
            msg += 'New Preset: %s' % self.preset['Name']
            if self.last_preset is not None:
                msg += '; Old Preset: %s' % self.last_preset['Name']
            self.last_preset = self.preset
            self.print_arm(msg)

    def print_arm(self, msg):
        print('Arm:', msg)

    def isFinished(self):
        return False
