import win32ui
import dde

class BFS(object):
  """
    A wrapper class for the DDE transactions between python and FlowDDE server.
  """
  def __init__(self,server="FlowDDE",topic="C(1)",capacity = 3.0):
    """
      server (srting): DDE server name (FlowDDE or FlowDDE2)
      topic (string): topic associated with the devece on flow bus. 

    """
    self.server = dde.CreateServer()
    self.server.Create("BFS_client")
    self.conversation = dde.CreateConversation(self.server)
    self.conversation.ConnectTo(server,topic)
    #This seems to be the parameter that defines full scale reading for fMeas
    self.capacity_max = float(self.conversation.Request("P(248)"))
    self.capacity = capacity


  def __del__(self):
    self.server.Destroy()

  def get_meas(self):
    """
      returns: mass flow rate in units of full capacity.
    """
    return float(self.conversation.Request("P(205)"))/self.capacity_max

  def get_mass_flow_rate(self):
    """
      returns: mass flow rate in g/min (assuming I guessed the calibration const correct)
    """
    #(sold as 3ml/min full scale)
    # this gives sane numbers, but who knows if they're right
    return self.get_meas()*self.capacity
 
  def get_density(self):
    """
      returns: the density in kg/m^3 = g/l
    """
    return float(self.conversation.Request("P(270)"))

  def get_flow_rate(self):
    """
      returns: flow rate in ml/min
    """
    density = self.get_density()
    if density < 100: #not a liquid
      return 0.0
    return 1000.0*self.get_mass_flow_rate()/density
