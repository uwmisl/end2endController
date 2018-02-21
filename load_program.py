from __future__ import print_function
from time import sleep
from synthesis import Dispenser
import hamiltonPSD.PSD8 as PSD8
import sys

import serial


selectorValve = 11 #on for dry side
load_NP = 14
load_air_nSyr =13 #valve for loading air.
vent = 15
#fluids = {"wash":[0,selectorValve], "act":[5,selectorValve],
#          "A":[1,selectorValve], "T":[3,selectorValve],
#          "C":[2,selectorValve], "G":[4,selectorValve],
#          "wetwash":[6], "ox":[7], "deblock":[8], "cleave":[9]}
fluids = {"wash":[0], "A":[1], "C":[2], "T":[3], "G":[4], "act":[5],
          "wetwash":[6], "ox":[7], "deblock":[8], "cleave":[9] }

s = Dispenser(fluidMap = fluids, verbose=True, debug=False)
s.valves.close(load_air_nSyr)
s.valves.close(load_NP)
s.valves.open(vent)

ser = serial.Serial("COM4", timeout=1)

pump = PSD8.PSD8(port="COM5")
pump.set_speed(14) #go slow
pump.set_valve("output")

sleep(1)

try:
  pump.dispense(225) #750ul
  sleep(3)
  s.valves.open(load_air_nSyr) #select air
  s.valves.open(load_NP)
  s.valves.close(vent)
  sleep(1)


  ser.reset_input_buffer()
  light = int(ser.readline())
  print (light)
  while light>1300:
    
    ser.reset_input_buffer()
    light = int(ser.readline())
    print(light)
  s.valves.close(load_air_nSyr)
  s.valves.close(load_NP)


  print(light)
finally:
  s.valves.close(load_air_nSyr)
  s.valves.close(load_NP)
  s.valves.close(vent)


