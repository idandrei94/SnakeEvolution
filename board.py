import random
import os
import time
import n_net
import numpy
from snake import Segment
from snake import Direction
from snake import Snake

    
class Board():
  def __init__(self, height = 10, width = 38, train = False, brain = None):
    self.height = height if height <= 10 and height % 2 == 0 else 10
    self.width = width if width <= 38 and width % 2 == 0 else 38
    self.frameCount = 0
    self.score = 0
    brain = n_net.neuralNetwork.load('brain') if brain == None else brain
    snake = Snake(50, brain)
    snake.initHead(height/2, width/2)
    self.snake = snake
    self.brain = brain
    self.train = train
    self.food = None
    
  def resetBoard(self):
      self.score = 0
      self.frameCount = 0
      self.snake.initHead(self.height/2, self.width/2)
      self.food = None

  def __genFood(self):
    self.food = Segment(random.randint(0, self.height-1), random.randint(0, self.width-1))
    while self.food in self.snake.snakeSegments:
      self.food = Segment(random.randint(0, self.height-1), random.randint(0, self.width-1))
  
  def __think(self):
    matrix = numpy.zeros((10,10))
    matrix.fill(0.1)
    for seg in self.snake.snakeSegments:
      matrix[int(seg.x)][int(seg.y)] = 0.5
    matrix[int(self.food.x)][int(self.food.y)] = 0.99
    brain_input = []
    for lst in matrix.tolist():
      brain_input = brain_input + lst

    if self.train:
        print("training")
        prev_dir = self.snake.direction
        head = self.snake.snakeSegments[0]
        if head.x == 0:
            if head.y == self.width - 1:
                self.snake.direction = Direction.South()
            else:
                self.snake.direction = Direction.East()
        elif head.y == self.width - 1:
            if head.x == self.height - 1:
                self.snake.direction = Direction.West()
            else:
                self.snake.direction = Direction.South()
        elif head.y == 0:
            self.snake.direction = Direction.North()
        elif head.x in [1, self.height - 1]:
            if self.snake.direction in [Direction.North(), Direction.South()]:
                self.snake.direction = Direction.West()
            else:
                self.snake.direction = Direction.South() if head.x == 1 else Direction.North()
        difference = prev_dir - self.snake.direction
        self.brain.train(brain_input, [
            0.99 if difference == 0 else 0.1,
            0.99 if difference == 1 else 0.1,
            0.99 if difference == 2 else 0.1,
    ])

    output = self.brain.query(brain_input)
    self.snake.direction = self.snake.direction + output.tolist().index(max(output)) 
  
  def __move(self):
    head = self.snake.snakeSegments[0]
    tail = self.snake.snakeSegments.pop()
    self.snake.snakeSegments.insert(0, Segment(head.x + self.snake.direction.x, head.y + self.snake.direction.y))
    if self.food in self.snake.snakeSegments:
      self.snake.snakeSegments.append(tail)
      self.__genFood()
      self.snake.health = self.snake.maxHealth
      self.score += 50
    self.snake.health = self.snake.health - 1
    self.score = self.score + len(self.snake.snakeSegments)
  
  def state(self):
    result =  (
    	(self.snake.snakeSegments[0].x in range(0, self.height)) and (
    		self.snake.snakeSegments[0].y in range(0, self.width))) and (
    		len(self.snake.snakeSegments) < self.width * self.height - 1) and (
    		self.snake.health > 0)
    return result
  
  def __genBoardMatrix(self):
    # add 2 for the board padding
    matrix = [ [' ' for i in range(self.width+2)] for j in range(self.height+2)]
    # add the vertical padding
    for i in range(self.width+2):
      matrix[0][i] = '#'
      matrix[self.height+1][i] = '#'
    # add the horizontal padding
    for i in range(self.height+1):
      matrix[i][0] = '#'
      matrix[i][self.width+1] = '#'
    # food
    matrix[self.food.x+1][self.food.y+1] = 'O'
    # snake
    for seg in self.snake.snakeSegments:
      matrix[int(seg.x+1)][int(seg.y+1)] = 'X'
    return matrix
  
  def __draw(self):
    for i in self.__genBoardMatrix():
      for j in i:
        print(j, end='')
      print()
    #time.sleep(1/50)
  
  def frame(self, display = True):
    if self.food == None:
      self.__genFood()
    self.__think()
    self.__move()
    self.frameCount = self.frameCount + 1
    #self.snake.health = self.snake.health - (1 if self.frameCount % 10 == 0 else 0)
    #self.score = self.score - (1 if self.frameCount % 10 == 0 else 0)
    #os.system('clear')
    if display:
      os.system('cls')
      print('Current frame: ', self.frameCount, '   ')
      print('Score: ', self.score, '    ')
      print('Health: ', self.snake.health)
      self.__draw()
      time.sleep(1/25)
    return self.state()