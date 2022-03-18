from europi import *
from time import ticks_diff, ticks_ms
from math import fabs, floor
from attractor import lorenz, rossler

'''
Strange Attractor
author: Sean Bechhofer (github.com/seanbechhofer)
date: 2022-03-15
labels: gates, triggers, randomness

Strange Attractor is a source of chaotic modulation. It can use a variety of different implementations.

Outputs 1, 2 and 3 are based on the x, y and z values generated by the attractor.

Outputs 4, 5 and 6 are gates based on the values of x, y and z and relationships between them. 

digital_in: Pause motion when HIGH
analog_in: 

knob_1: Adjust speed
knob_2: Adjust threshold for triggers

button_1: Decrease output voltage range
button_2: Increase output voltage range

output_1: x 
output_2: y
output_3: z
output_4: triggers/gates
output_5: triggers/gates
output_6: triggers/gates

'''

# Overclock the Pico for improved performance.
machine.freq(250_000_000)

# Maximum voltage output. Cranking this up may cause issues with some modules. 
MAX_OUTPUT = 5

class StrangeAttractor:
    def __init__(self):
        # create the attractor and initialise.
        # This will take around 30 seconds.
        # Use Lorenz
        self.a = lorenz()
        self.initialise_message()
        self.a.estimate_ranges()
            
        # Initialize variables
        self.checkpoint = 0
        # time before update
        self.period = 100
        # output range.
        self.range = MAX_OUTPUT
        # initial threshold for gates
        self.threshold = 20
        # freeze motion
        self.freeze = False

        # Triggered when button 1 is released
        # Short press: decrease range
        # Long press: 
        @b1.handler_falling
        def b1Pressed():
            if ticks_diff(ticks_ms(), b1.last_pressed()) >  300:
                # long press
                pass
            else:
                # short press
                self.range -= 1
                if self.range < 1:
                    self.range = 1

        # Triggered when button 2 is released.
        # Short press: increase range
        # Long press: 
        @b2.handler_falling
        def b2Pressed():
            
            if ticks_diff(ticks_ms(), b2.last_pressed()) >  300:
                # long press
                pass
            else:
                # short press
                self.range += 1
                if self.range > MAX_OUTPUT:
                    self.range = MAX_OUTPUT

        # Freeze is triggered when din goes HIGH.
        @din.handler
        def dinTrigger():
            # Pause
            self.freeze = True

        @din.handler_falling
        def dinTriggerEnd():
            # Start agin
            self.freeze = False

    def update_values(self):
        if not self.freeze:
            self.a.step()
        
    def get_speed(self):
        # Set speed based on the knob.
        # The range is piecewise linear from fully CCW to noon and noon to fully CW.
        val = k1.read_position()
        low = 1000 # CCW
        mid = 100 # noon
        high = 10 # CW
        if val == 0:
            self.period = low
        elif val < 50:
            self.period = low - ((low-mid) * (val/50))
        else:
            self.period = mid - ((mid-high) * (val-50)/50)

    def get_threshold(self):
        val = k2.read_position()
        self.threshold = (40 * val)/100
        

    def update(self):
        # Change the values and output
        self.update_values()
        cv1.voltage((self.range * self.a.x_scaled()) / 100)
        cv2.voltage((self.range * self.a.y_scaled()) / 100)
        cv3.voltage((self.range * self.a.z_scaled()) / 100)
        # Calculate gates
        # gate 1 fires if x is divisible by 2 when considered an int
        self.gate4 = floor(self.a.x_scaled()) % 2 == 0
        # gates 2 and 3 look at the differences between the outputs. 
        self.gate5 = fabs(self.a.y_scaled() + self.a.z_scaled() - 2*self.a.x_scaled()) > self.threshold
        self.gate6 = fabs(self.a.z_scaled() + self.a.x_scaled() - 2*self.a.y_scaled()) > self.threshold
        if self.gate4:    
            cv4.on()
        else:
            cv4.off()
        if self.gate5:
            cv5.on()
        else:
            cv5.off()
        if self.gate6:
            cv6.on()
        else:
            cv6.off()
        
        self.checkpoint = ticks_ms()
        self.update_screen()

    def main(self):
        while True:
            self.get_speed()
            self.get_threshold()
            if ticks_diff(ticks_ms(), self.checkpoint) > self.period:
                self.update()

    def initialise_message(self):
        oled.fill(0)
        oled.text('Initialising...',0,0,1)
        oled.show()
        
    def update_screen(self):
        #oled.clear() - dont use this, it causes the screen to flicker!
        oled.fill(0)
        oled.text('1:' + str(int(self.a.x_scaled())),0,0,1)
        oled.text('2:' + str(int(self.a.y_scaled())),0,8,1)
        oled.text('3:' + str(int(self.a.z_scaled())),0,16,1)
        oled.text('S:' + str(int(self.period)),40,0,1)
        oled.text('T:' + str(int(self.threshold)),40,8,1)
        oled.text('R:' + str(int(self.range)),40,16,1)
        if self.gate4:
            oled.text('4',100,0,1)
        if self.gate5:
            oled.text('5',100,8,1)
        if self.gate6:
            oled.text('6',100,16,1)
        if self.freeze:
            oled.text('FREEZE',0,24,1)
            
        oled.text(self.a.name,80,24,1)
            
        oled.show()

# Reset module display state.
reset_state()
att = StrangeAttractor()
att.main()

