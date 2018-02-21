from __future__ import print_function
from time import sleep
from synthesis import Dispenser



selectorValve = 11 #on for dry side
#fluids = {"wash":[0,selectorValve], "act":[5,selectorValve],
#          "A":[1,selectorValve], "T":[3,selectorValve],
#          "C":[2,selectorValve], "G":[4,selectorValve],
#          "wetwash":[6], "ox":[7], "deblock":[8], "cleave":[9]}
fluids = {"wash":[0], "A":[1], "C":[2], "T":[3], "G":[4], "B":[4], "act":[5],
          "wetwash":[6], "ox":[7], "deblock":[8], "cleave":[9]}
#id27_bichlien 5'-3'
sequence = "BCCCCCCCCCCCCCCCBAAAAAAAAAAAAAAA"
sequence = "BCCCCCCCCCCCCBTTTTTTTTTTTTTTT"
sequence = "BAAAAAAAAABTTTTTTTTTTTTTTT"
sequence = "BCCCCCCBTTTTTTTTTTTTTTT"

s = Dispenser(fluidMap = fluids, verbose=True, debug=False)

#init
s.pump(1000,"wetwash")

#start on wet side
s.valves.close(11)
#deblock
for nt in sequence[::-1]:  #note reversing sequence to synthesize 3'-5'
  s.pump(450,"deblock")
  sleep(25)
  for _ in range(5): #spread that last 450 over time. This is pretty conservative
    s.pump(450/5,"deblock")
    sleep(25/5)

  #couple
  s.pump(100,"wetwash")
  s.valves.open(11) #dry side
  s.pump(100,"act")
  #s.pump(350,nt) #mix in manifold, must mix in fluids defn
  s.mix(350,[nt,"act"])
  print("adding "+nt)
  if nt.upper() == "B":
    print("coupling biotin")
    for _ in range(15):
      sleep(120)
      s.pump(10,"wash")
  else:
    sleep(47)
    s.pump(35,"wash")
    sleep(47)
    s.pump(1000,"wash")
  s.valves.close(11) #wetside
  #ox
  s.pump(750,"ox")
  s.pump(2000,"wetwash")


while True:
  sleep(10)