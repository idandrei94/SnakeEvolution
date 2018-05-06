import n_net

class Snake():
    def __init__(self, maxHealth, brain = None):
        self.brain = n_net.neuralNetwork(100,200,3,0.3) if  brain == None else brain
        self.snakeSegments = []
        self.init = False
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.direction = Direction.South()

    def initHead(self, x, y):
        self.snakeSegments = [ Segment(x, y) ]
        self.init = True

class Direction():
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def __eq__(self, other):
    return type(self) is type(other) and self.x == other.x and self.y == other.y
    
  def __add__(self, other : int):
      if other < 0:
          return self
      other = other % 3
      if other == 0:
          return self
      if self == Direction.North():
          return Direction.East() if other == 1 else Direction.West()

      if self == Direction.South():
          return Direction.West() if other == 1 else Direction.East()

      if self == Direction.East():
          return Direction.South() if other == 1 else Direction.North()

      if self == Direction.West():
          return Direction.North() if other == 1 else Direction.East()

  def __sub__(self, other):
        for i in range(3):
           if self + i == other:
              return i
        return -1

  directions = [None, None, None, None]

  def North():
    if Direction.directions[0] == None:
      Direction.directions[0] = Direction(-1,0)
    return Direction.directions[0]
    
  def South():
    if Direction.directions[1] == None:
      Direction.directions[1] = Direction(1,0)
    return Direction.directions[1]
    
  def East():
    if Direction.directions[2] == None:
      Direction.directions[2] = Direction(0,1)
    return Direction.directions[2]
    
  def West():
    if Direction.directions[3] == None:
      Direction.directions[3] = Direction(0,-1)
    return Direction.directions[3]

class Segment():
  def __init__(self, x:int, y:int):
    self.x = x
    self.y = y
    
  def __eq__(self, other):
  
    return type(self) is type(other) and (
    self.x == other.x) and (
    self.y == other.y)
