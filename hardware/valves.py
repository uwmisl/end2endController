from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import DigitalOutput
#import Phidget22.Phidget.DigitalOutput as DigitalOutput

from threading import Timer, Lock

class PhidgetRelay(object):
  def __init__(self,vintport,channel,hold_duty=1.0,hit_delay=0.2):
    self.rly = DigitalOutput()
    self.rly.setHubPort(vintport)
    self.rly.setChannel(channel)
    self.rly.openWaitForAttachment(5000)
    self.lock = Lock()
    self.state = False #false -> closed, true->open, or duty>0%
    self.hit_delay = hit_delay
    self.hold_duty = hold_duty

  def open(self):
    def _hold():
      with self.lock:
        #double check it hasn't been closed in the mean time!
        if self.state == True:
          self.rly.setDutyCycle(self.hold_duty)

    with self.lock:
      self.rly.setDutyCycle(1.0)
      self.state = True

    # set hold_duty after hit_delay seconds
    t = Timer(self.hit_delay,_hold)
    t.start()

  def close(self):
    with self.lock:
      self.rly.setDutyCycle(0.0)
      self.rly.state = False


class Valves(object):
  def __init__(self,vintport=0,nvalves=16, LUT=None, hold_duty=None):
    """
      vintport (int): vint port the SS relays are on
      nvalves (int): number of valves connected (16 max)
      LUT (dict): key-> (string) valve name; value-> (int)relay number
    """
    assert (nvalves > 0) and (nvalves <=16)
    self.relays = []
    self.LUT = LUT
    if hold_duty and len(hold_duty)==nvalves:
      pass
    else:
      hold_duty = [1.0]*nvalves  #default don't lower duty

    for ch in range(nvalves):
      _rly = PhidgetRelay(vintport, ch, hold_duty = hold_duty[len(self.relays)])
      self.relays.append(_rly)

  def _lookup(self,x):
    if isinstance(x,int):
      return [self.relays[x]]
    else:
      return [self.relays[q] for q in self.LUT[x]]

  def open(self,n):
    for v in self._lookup(n):
      v.open()

  def close(self,n):
    for v in self._lookup(n):
      v.close()


if __name__ == '__main__':
  from time import sleep
  mylut = {"test": [0,11]}
  v = Valves(LUT=mylut)
  v.open("test")
  sleep(1)
  v.close("test")
  print ("done")

  sleep(4)


