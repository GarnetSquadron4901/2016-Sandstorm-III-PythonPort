from networktables import NetworkTable
from networktables2.type import BooleanArray, NumberArray


class GarnetControls:

    LED_OUTPUTS = 16
    PWM_OUTPUTS = 11
    ANALOG_INPUTS = 16
    SWITCH_INPUTS = 16

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

        self.reset_table()

    def reset_table(self, ):
        self.sw_vals_out.clear()
        self.led_vals_in.clear()
        self.ana_vals_out.clear()
        self.pwm_vals_in.clear()

        self.sw_vals_out.extend([False] * self.SWITCH_INPUTS)
        self.led_vals_in.extend([False] * self.LED_OUTPUTS)
        self.ana_vals_out.extend([0] * self.ANALOG_INPUTS)
        self.pwm_vals_in.extend([0] * self.PWM_OUTPUTS)

        self.nt.putValue(self.SWITCH_OUT, self.sw_vals_out)
        self.nt.putValue(self.LED_IN, self.led_vals_in)
        self.nt.putValue(self.ANALOG_OUT, self.ana_vals_out)
        self.nt.putValue(self.PWM_IN, self.pwm_vals_in)




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
