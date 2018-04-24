#!/usr/bin/env python2
#^Above for windows python launcher (and other os's)
from __future__ import print_function
from time import sleep
from synthesis import Dispenser



selectorValve = 11 #on for dry side
#fluids = {"wash":[0,selectorValve], "act":[1,selectorValve],
#          "A":[2,selectorValve], "T":[3,selectorValve],
#          "C":[4,selectorValve], "G":[5,selectorValve],
#          "X":[6,selectorValve],
#          "wetwash":[6], "ox":[7], "deblock":[8], "cleave":[9]}
fluids = {"wash":[0], "A":[2], "C":[3], "T":[4], "G":[5], "X":[6], "act":[1],
          "wetwash":[7], "ox":[8], "deblock":[9], "cleave":[10]}

sequence = "XTTCCGCAAGACTTATTGGCATAGTCACAGATGCAGCACGTATAGTATATATGTGTACTGTCGCATAGCAGCTAGCTAGCTTCCATTTAACGCAAGCAGGA"

s = Dispenser(fluidMap = fluids, verbose=True, debug=False)

#start on wet side
s.valves.close(selectorValve)

#init
s.pump(1000,"wetwash")
sleep(30)

#deblock
for nt in sequence[::-1]:  #note reversing sequence to synthesize 3'-5'
  s.pump(450,"deblock")
  sleep(25)
  for _ in range(3): #spread that last 450 over time. This is pretty conservative
    s.pump(450/5,"deblock")
    sleep(25/5)
  for _ in range(2):
    s.pump(450/5,"wetwash")
    sleep(25/5)

  #couple
  s.pump(200,"wetwash")
  s.valves.open(selectorValve) #dry side
  s.pump(100,"act")
  #s.pump(350,nt) #mix in manifold, must mix in fluids defn
  s.mix(350,[nt,"act"])
  print("adding "+nt)
  if nt.upper() == "X":
    print("coupling X")
    for _ in range(15):
      sleep(60)
      s.pump(10,"wash")
  else:
    for _ in range(12):
      sleep(10)
      s.pump(10,"wash")
  s.pump(1000,"wash")
  s.valves.close(selectorValve) #wetside
  #ox
  s.pump(750,"ox")
  s.pump(2000,"wetwash")

#final deblock
s.pump(450,"deblock")
sleep(25)
for _ in range(3): #spread that last 450 over time. This is pretty conservative
  s.pump(450/5,"deblock")
  sleep(25/5)
for _ in range(2):
  s.pump(450/5,"wetwash")
  sleep(25/5)
s.pump(1000, "wetwash")

while True:
  sleep(10)
