#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This module contains classes for synthesis.  Right now just the dispenser stuff.
"""
from __future__ import print_function
from time import sleep, time

from hardware import BFS, Valves

class dummy_BFS(object):
  def __init__(self):
    pass
  def get_flow_rate(self):
    return 3.0

class Dispenser(object):
  """
    valve and manifold dispenser for synthesis
  """
  def __init__(self, fluidMap=None, verbose=False, debug=False):
    """
      fluidMap (dict): key-> (string) valve name; value-> (array int)relay number
      debug (bool): if true does not check flow sensor.
    """
    if debug:
      self.flow_sens = dummy_BFS()
    else:
      self.flow_sens = BFS()
    self.valves = Valves(LUT=fluidMap,hold_duty=([0.3]*12+[1.0]*4))
    self.verbose = verbose
    self.debug = debug

  def pump(self, volume, fluid):
    """
      pump volume ul of fluid.

      Integrates volume dispensed and closes valve once reached.
      This will casue fluid to be over dispensed.
    """
    if self.verbose:
      print("pumping, {} ul {} ...".format(volume,fluid),end=" ")
    flow_ulps_n0 = self.flow_sens.get_flow_rate()*1000.0/60.0
    t_n0 = time()
    pumped = 0
    self.valves.open(fluid)
    #trapizoidal integration
    while pumped < volume:
      flow_ulps_n1 = self.flow_sens.get_flow_rate()*1000.0/60.0
      t_n1 = time()
      pumped += ((flow_ulps_n1+flow_ulps_n0)/2.0)*(t_n1-t_n0)
      #update
      t_n0 = t_n1
      flow_ulps_n0 = flow_ulps_n1
      sleep(0.1)
    self.valves.close(fluid)
    if self.verbose:
      print("done")

  def mix(self, volume, fluids, time_interval=0.5):
    """
      pumps a total of volume ul of fluids.

      volume (int): number of ul to pump in total
      fluids (list): list of fluid names or indexes
      time_interval(float): number of seconds to pump each fluid
                          before moving to the next.
    """
    if self.verbose:
      print("mixing {} + {} ...".format(*fluids),end=" ")
    flow_ulps_n0 = self.flow_sens.get_flow_rate()*1000.0/60.0
    t_n0 = time()
    t_change = time()
    pumped = 0
    fluid_index = 0
    self.valves.open(fluids[fluid_index])
    #trapizoidal integration
    while pumped < volume:
      flow_ulps_n1 = self.flow_sens.get_flow_rate()*1000.0/60.0
      t_n1 = time()
      pumped += ((flow_ulps_n1+flow_ulps_n0)/2.0)*(t_n1-t_n0)
      #update
      t_n0 = t_n1
      flow_ulps_n0 = flow_ulps_n1
      sleep(0.1)
      if (time() - t_change) > time_interval:
        self.valves.close(fluids[fluid_index])
        fluid_index = (fluid_index+1)%len(fluids)
        self.valves.open(fluids[fluid_index])
        t_change = time()

    self.valves.close(fluids[fluid_index])
    if self.verbose:
      print("done")
