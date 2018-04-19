from __future__ import print_function
import Tkinter as tk

from time import sleep
from synthesis import Dispenser
import hamiltonPSD.PSD8 as PSD8
import sys
import threading
import Queue

import serial
print(sys.version_info)


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




class gui(object):
  n_buttons = 16
  pump_max = 4000 #TODO: fix this with correct number

  def __init__(self,q):
    self.cmdq=q
    self.master = tk.Tk()
    self.default_color =self.master.cget('bg')
    self.master.title("testgui")
    self.button_frame = tk.Frame()
    self.button_frame.pack()

    self.valve_state = [0]*16

    self.valve_buttons = []
    for ii in range(self.n_buttons):
      _c = self.toggle_valve_callback_gen(ii)
      _b = tk.Button(self.button_frame,text="Valve {} is off".format(ii), command=_c)
      _b.config(width=10)
      _b.grid(row=ii/4,column=ii%4)
      self.valve_buttons.append(_b)



    self.pump_slider = tk.Scale(self.master, from_=0, to=self.pump_max, orient=tk.HORIZONTAL)
    self.pump_slider.pack(fill = "x")

    _b = tk.Button(self.master,text="Execute pump move",command=lambda: print(self.pump_slider.get()) )
    _b.pack()


  def run(self):
    self.master.mainloop()

  def toggle_valve_callback_gen(self,number):
    x = number
    def toggle_valve():
      if self.valve_state[x] == 0:
        self.valve_state[x] = 1 
        self.cmdq.put( ("valve_open",x) )
        self.valve_buttons[x]["text"]="Valve {} is on".format(x)
        self.valve_buttons[x]["bg"]= "red"
      else:
        self.valve_state[x] = 0
        self.cmdq.put( ("valve_close",x) )
        self.valve_buttons[x]["text"]="Valve {} is off".format(x)
        self.valve_buttons[x]["bg"]= self.default_color

      #stub
      print ("toggle {}".format(x))
    return toggle_valve


if __name__ == '__main__':
  cmd_queue = Queue.Queue()
  s = Dispenser(fluidMap = fluids, verbose=True, debug=False)

  commands = {"valve_open"  : lambda x:s.valves.open(x),
              "valve_close" : lambda x:s.valves.close(x)}
  g = gui(cmd_queue)

  t1 = threading.Thread(target=lambda:g.run())
  t1.start()
  print("started")
  while (t1.isAlive()):
    while cmd_queue.qsize()>0:
      c = cmd_queue.get()
      commands[c[0]](*c[1:])
    sleep(0.25)

  t1.join()

  #don't know why but without this it crashes.  has something to do with 
  #phidgets and or the PSD8.
  sleep(1)