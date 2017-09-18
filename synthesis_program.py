from __future__ import print_function
from time import sleep
from synthesis import Dispenser



selectorValve = 11 #on for dry side
fluids = {"wash":[0,selectorValve], "act":[5,selectorValve],
          "A":[1,selectorValve], "T":[3,selectorValve],
          "C":[2,selectorValve], "G":[4,selectorValve],
          "wetwash":[6], "ox":[7], "deblock":[8], "cleave":[9]}
#id27_bichlien 5'-3'
sequence = "TTAATCGGTAACACCTGCGGAGCTAGCTAGCTGCTATCTGTGTGACAGCTATCATGTGTCACGCACGTCTAGACGTCTCTCTCGCTGTAGTCACTACGCTATAGCACTATACAGATCTCGTGCTCATGCTTGGCACCGATTCGTAACAAT"

s = Dispenser(fluidMap = fluids, verbose=True, debug=True)

#init
s.pump(1000,"wash")

#deblock
for nt in sequence[::-1]:  #note reversing sequence to synthesize 3'-5'
  s.pump(500,"deblock")
  sleep(25)
  s.pump(500,"deblock")
  sleep(25)

  #couple
  s.pump(100,"wash")
  s.pump(100,"act")
  #s.pump(350,nt)
  s.mix(350,[nt,"act"])
  sleep(47)
  s.pump(35,"wash")
  sleep(47)
  s.pump(1000,"wash")
  #ox
  s.pump(1000,"ox")
  s.pump(2000,"wash")


while True:
  sleep(10)