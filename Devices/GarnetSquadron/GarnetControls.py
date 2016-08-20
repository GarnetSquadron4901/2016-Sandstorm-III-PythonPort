from networktables import NetworkTable
from networktables2.type import BooleanArray, NumberArray


class GarnetControls:
    SWITCH_OUT = 'Switch'
    ANALOG_OUT = 'Analog'
    PWM_IN = 'PWM'
    LED_IN = 'LED'

    def __init__(self, address='localhost', flush_period=20e-3):
        self.nt = NetworkTable.getTable('GarnetControls')

        self.sw_vals_out = BooleanArray()
        self.led_vals_in = BooleanArray()
        self.ana_vals_out = NumberArray()
        self.pwm_vals_in = NumberArray()

    def getAnalog(self, ch):
        self.nt.getValue(self.ANALOG_OUT, self.ana_vals_out)
        return self.ana_vals_out[ch]

    def getSwitch(self, ch):
        self.nt.getValue(self.SWITCH_OUT, self.sw_vals_out)
        return self.sw_vals_out[ch]

    def putPWM(self, ch, val):
        self.pwm_vals_in[ch] = val
        self.nt.putValue(self.PWM_IN, self.pwm_vals_in)

    def putLED(self, ch, val):
        self.led_vals_in[ch] = val
        self.nt.putValue(self.LED_IN, self.led_vals_in)
