from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import DigitalOutput
#import Phidget22.Phidget.DigitalOutput as DigitalOutput


class Valves(object):
  def __init__(self,vintport=0,nvalves=16, LUT=None):
    """
      vintport (int): vint port the SS relays are on
      nvalves (int): number of valves connected (16 max)
      LUT (dict): key-> (string) valve name; value-> (int)relay number
    """ 
    assert (nvalves > 0) and (nvalves <=16)
    self.relays = []
    self.LUT = LUT
    for ch in range(nvalves):
      _rly = DigitalOutput()
      _rly.setHubPort(vintport)
      _rly.setChannel(ch)
      _rly.openWaitForAttachment(5000)
      self.relays.append(_rly)

  def _lookup(self,x):
    if isinstance(x,int):
      return self.relays[x]
    else:
      return self.relays[self.LUT[x]]

  def open(self,n):
    self._lookup(n).setState(True)

  def close(self,n):
    self._lookup(n).setState(False)


if __name__ == '__main__':
  from time import sleep
  v = Valves()
  v.open(0)
  sleep(1)
  v.close(0)


